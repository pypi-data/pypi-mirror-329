import os
import time
from dataclasses import dataclass
from queue import Queue, Empty
from threading import Thread
from typing import TypeVar, List

from pylizlib.os import pathutils

from pylizai.core.ai_results import AiResult
from loguru import logger
from pylizlib.config.pylizdir import PylizDir, PylizDirFoldersTemplate
from pylizlib.data import datautils
from pylizlib.model.operation import Operation
from pylizai.core.ai_setting import AiQuery, AiQueries, AiSetting
from pylizai.core.ai_source_type import AiSourceType
from pylizai.llm.gemini import GeminiController
from pylizai.llm.llama_cpp import LlamaCppController
from pylizai.llm.lmstudio import LmmStudioController
from pylizai.llm.mistral import MistralController
from pylizai.llm.whisper import WhisperController
from pylizai.llm.ollamaliz import Ollamaliz
from pylizai.model.ai_exctps import AiRunnerException
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_prompts import attach_prompt_schema_if_required
from pylizai.model.ai_runner_log import AiRunnerLog
from pylizai.utils.ai_chkr import AiRunChecker


# noinspection PyMethodMayBeStatic
class AiRunner:

    def __init__(self, pyliz_dir: PylizDir, enable_log: bool = True):
        self.pyliz_dir = pyliz_dir
        self.app_folder_ai = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.AI)
        self.app_folder_logs = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.LOGS)
        self.app_model_folder = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.MODELS)
        self.app_results_folder = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.RESULTS)
        self.app_temp_folder = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.TEMP)
        if not datautils.all_not_none(self.app_folder_ai, self.app_folder_logs, self.app_model_folder, self.app_temp_folder, self.app_results_folder):
            raise ValueError("Some folders are not set in PylizDir")
        self.pyliz_dir.add_folder("runners", "runners")
        self.runner_log = AiRunnerLog(enable_log, self.pyliz_dir.get_folder_path("runners"))

    # --------------------------------------------------------------

    def __handle_mistral(self, query: AiQuery):
        controller = MistralController(query.setting.api_key)
        return controller.run(query)

    def __handle_lmstudio(self, query: AiQuery):
        controller = LmmStudioController(query.setting.remote_url)
        return controller.run(query)

    def __handle_llama_cpp(self, query: AiQuery):
        controller = LlamaCppController(self.pyliz_dir)
        return controller.run(query)

    def __handle_gemini(self, query: AiQuery):
        controller = GeminiController(query.setting.api_key)
        return controller.run(query)

    def __handle_whisper(self, query: AiQuery):
        logger.debug("Calling whisper controller...")
        controller = WhisperController(self.app_model_folder, self.app_temp_folder)
        return controller.run(query)

    def __handle_ollama_server(self, query: AiQuery):
        ollamaliz = Ollamaliz(query.setting.remote_url, True)
        json_output = query.setting.return_type == AiReturnType.STRING_JSON
        custom_format = query.setting.return_type_object if query.setting.return_type == AiReturnType.OBJECT else None
        return ollamaliz.send_query(query.prompt, query.setting.source.model_name, json_output, query.payload_path, custom_format)

    # --------------------------------------------------------------

    T = TypeVar('T')

    def run_model(self, query: AiQuery) -> str:
        logger.trace("About to run model with payload path: " + query.payload_path) if query.payload_path is not None else None
        self.runner_log.set_query_start(query.id)
        try:
            if query.setting.source_type == AiSourceType.API_MISTRAL:
                return self.__handle_mistral(query)
            if query.setting.source_type == AiSourceType.LOCAL_LLAMACPP:
                return self.__handle_llama_cpp(query)
            if query.setting.source_type == AiSourceType.API_GEMINI:
                return self.__handle_gemini(query)
            if query.setting.source_type == AiSourceType.LOCAL_WHISPER:
                return self.__handle_whisper(query)
            if query.setting.source_type == AiSourceType.OLLAMA_SERVER:
                return self.__handle_ollama_server(query)
            if query.setting.source_type == AiSourceType.LMSTUDIO_SERVER:
                return self.__handle_lmstudio(query)
            raise NotImplementedError("Source type not implemented yet in AiRunner")
        except Exception as e:
            raise AiRunnerException(str(e))
        finally:
            self.runner_log.set_query_end(query.id)

    def check_payload(self, path: str):
        try:
            if path is not None:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Payload path not found: {path}")
                if not os.path.isfile(path):
                    raise ValueError(f"Payload path is not a file: {path}")
                pathutils.check_path_file(path)
        except Exception as e:
            logger.error(f"Error while checking payload path: {e}. Ai query aborted.")
            raise AiRunnerException

    def check_requirements(self, setting: AiSetting):
        try:
            checker = AiRunChecker(setting, self.app_model_folder, self.app_folder_ai)
            checker.check_params()
            checker.check_source()
            logger.info(f"All requirements met for AiQuery with model {setting.model.value} and source type {setting.source_type.value[0]}.")
        except Exception as e:
            logger.error(f"Error while checking requirements: {e}. Ai query aborted.")
            raise AiRunnerException(str(e))

    def check_prompt(self, query: AiQuery):
        if query.prompt is None or len(query.prompt) == 0:
            raise AiRunnerException("Prompt is empty or None.")
        #attach_prompt_schema_if_required(query)


    # --------------------------------------------------------------

    def run(self, query: AiQuery) -> Operation[T]:
        logger.info("Ai runner started with query of type" + query.query_type.value + " with model " + query.setting.model.value + " and source type " + query.setting.source_type.value[0])
        # Set operations log
        self.runner_log.set_start()
        self.runner_log.set_query_start(query.id)
        self.runner_log.add_query_obj(query)
        try:
            # Check requirements
            self.check_requirements(query.setting)
            self.check_payload(query.payload_path)
            self.check_prompt(query)
            # Run model
            str_result = self.run_model(query)
            # handle Results
            result_handler = AiResult(self.pyliz_dir, query.setting, str_result)
            result_handler.save_results(query.save_text_result, query.save_obj_result, query.save_ai_setting)
            result_handler.add_results_to_runner_log(query.id, self.runner_log)
            # Set query status
            self.runner_log.set_query_status(query.id, True)
            return Operation(status=True, payload=result_handler.output)
        except AiRunnerException as e:
            self.runner_log.set_query_status(query.id, False)
            return Operation(status=False, error=str(e))
        finally:
            self.runner_log.set_completion_status(True)
            self.runner_log.set_query_end(query.id)
            self.runner_log.set_end()
            self.runner_log.save_runner_log()

    def run_multiple(self, queries: AiQueries) -> Operation[List[T]]:
        self.runner_log.set_start()
        try:
            pool = AiPoolRunner(self, queries)
            pool.start()
            results = pool.get_results()
            return Operation(status=True, payload=results)
        except AiRunnerException as e:
            return Operation(status=False, error=str(e))
        finally:
            self.runner_log.set_completion_status(True)
            self.runner_log.set_end()
            self.runner_log.save_runner_log()



U = TypeVar('U')


@dataclass
class AiPoolResult:
    result_str: str
    result_obj: U | None
    worker_time: float
    path_used: str
    setting_used: AiSetting
    query_id: str


# noinspection DuplicatedCode
class AiPoolRunner:

    def __init__(self, runner: AiRunner, queries: AiQueries, setting_max_try: int = 2):
        self.settings = queries.settings
        self.setting_max_try = setting_max_try
        self.num_of_settings = len(self.settings)
        self.runner = runner
        self.prompt = queries.prompt
        self.paths = queries.payload_path_list
        self.paths_queue = Queue()
        self.results_temp: List[AiPoolResult] = []
        self.results: List[AiPoolResult] = []
        self.threads: List[Thread] = []
        self.channels: List[AiPoolRunner.SettingChannel] = []

    def __check_paths(self):
        for current_path in self.paths:
            self.runner.check_payload(current_path)

    def __fill_queue(self):
        for current_path in self.paths:
            self.paths_queue.put(current_path)

    def __check_requirements(self):
        if self.settings is None or len(self.settings) == 0:
            raise AiRunnerException("No settings found in scheduler.")
        if self.paths is None or len(self.paths) == 0:
            raise AiRunnerException("No paths found in scheduler.")
        if not all(current.return_type == self.settings[0].return_type  for current in self.settings):
            raise AiRunnerException("All settings must have the same return type.")
        for current_setting in self.settings:
            self.runner.check_requirements(current_setting)


    def __start_threads(self):
        logger.debug(f"Starting {len(self.threads)} threads...")
        for thread in self.threads:
            thread.start()

    def __wait_threads(self):
        # Attendi che tutti i thread finiscano
        logger.debug("Waiting threads to finish...")
        for thread in self.threads:
            thread.join()
        logger.debug("Scheduler threads finished.")

    def __check_channels(self):
        # Controlla se ci sono stati errori critici
        if any(channel.is_in_error for channel in self.channels):
            raise AiRunnerException("All scheduler channels are in error state because they failed for max_try times.")


    def __handle_channels_results(self, pool_results: List[AiPoolResult]):
        setting = self.settings[0]
        for current in pool_results:
            try:
                result_handler = AiResult(self.runner.pyliz_dir, setting, current.result_str)
                result_handler.save_results()
                result_handler.add_results_to_runner_log(current.query_id, self.runner.runner_log)
                current.result_obj = result_handler.output
            except AiRunnerException as e:
                logger.error(f"Error while handling result: {e}")
        return pool_results

    def get_results(self) -> List[AiPoolResult]:
        if len(self.results) == 0:
            raise AiRunnerException("No results found in pool.")
        return self.results

    def start(self,):
        self.__check_requirements()
        self.__check_paths()
        self.__fill_queue()
        self.channels = [AiPoolRunner.SettingChannel(setting, self.setting_max_try) for setting in self.settings]
        self.threads = [Thread(target=AiPoolWorker.worker, args=(self, channel,)) for channel in self.channels]
        self.__start_threads()
        self.__wait_threads()
        self.__check_channels()
        self.results_temp = [result for channel in self.channels for result in channel.results]
        self.results = self.__handle_channels_results(self.results_temp)


    class SettingChannel:
        def __init__(self, setting: AiSetting, max_try: int):
            self.setting = setting
            self.max_try = max_try
            self.fails = 0
            self.is_in_error = False
            self.results: list[AiPoolResult] = []
            self.current_iteration = 0

        def add_result(self, str_result: str,  path_used: str, seconds: float = 0.0, query_id: str = None):
            result = AiPoolResult(str_result, None, seconds, path_used, self.setting, query_id)
            self.results.append(result)



class AiPoolWorker:

    @staticmethod
    def worker(pool_runner: AiPoolRunner, channel: AiPoolRunner.SettingChannel):
        logger.trace("Worker started for channel with setting " + channel.setting.model.value + " and source type " + channel.setting.source_type.value[0])
        while not pool_runner.paths_queue.empty() and channel.fails < channel.max_try:
            try:
                path = pool_runner.paths_queue.get(timeout=0.1)  # Timeout per evitare blocchi indefiniti
                temp_query = AiQuery(channel.setting, pool_runner.prompt, path)
                try:
                    time_start = time.perf_counter()
                    pool_runner.runner.runner_log.add_query_obj(temp_query)
                    pool_runner.runner.check_prompt(temp_query)
                    result = pool_runner.runner.run_model(temp_query)
                    time_end = time.perf_counter()
                    elapsed_time = time_end - time_start
                    pool_runner.runner.runner_log.set_query_status(temp_query.id, True)
                    channel.add_result(result, path, elapsed_time, temp_query.id)
                except AiRunnerException as e:
                    logger.error(f"Error while running model for setting {channel.setting.id}: {e}")
                    pool_runner.runner.runner_log.set_query_status(temp_query.id, False)
                    channel.fails += 1
                    if channel.fails >= channel.max_try:
                        logger.error(f"Setting {channel.setting.id} failed for max_try times.")
                        channel.is_in_error = True
                        break
                finally:
                    pool_runner.paths_queue.task_done()
                    channel.current_iteration += 1
            except Empty:
                break