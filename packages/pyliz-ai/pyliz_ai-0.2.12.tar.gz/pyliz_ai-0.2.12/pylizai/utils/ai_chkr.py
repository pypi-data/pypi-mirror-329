import os

from loguru import logger
from pylizlib.network.netutils import is_internet_available, exec_get
from pylizlib.os import pathutils, osutils

from pylizai.core.ai_setting import AiSetting
from pylizai.core.ai_source_type import AiSourceType
from pylizai.llm.lmstudio import LmmStudioController
from pylizai.llm.ollamaliz import Ollamaliz
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_env import AiEnvType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.utils.ai_dwder import AiDownloader


class AiRunChecker:

    def __init__(self, setting: AiSetting, app_model_folder: str, app_folder_ai: str ):
        self.source = setting.source
        self.setting = setting
        self.app_folder_ai = app_folder_ai
        self.app_model_folder = app_model_folder
        self.current_model_folder = os.path.join(self.app_model_folder, self.setting.source.model_name)


    def __check_ai_files(self):
        if self.source.ai_files is not None:
            pathutils.check_path(self.current_model_folder, True)

            for file in self.source.ai_files:
                current_file = os.path.join(self.current_model_folder, file.file_name)
                is_present = os.path.exists(current_file)
                size_web = file.get_file_size_byte()
                size_local = os.path.getsize(current_file) if is_present else 0
                file.local_path = current_file

                if not is_present:
                    logger.debug(f"File \"{file.file_name}\" not found in model folder {self.current_model_folder}.")
                    AiDownloader.download_ai_file(file, self.current_model_folder)
                else:
                    if size_local < size_web:
                        logger.warning(f"File {file.file_name} size mismatch: Web {size_web} bytes, Local {size_local} bytes. Downloading again...")
                        os.remove(current_file)
                        AiDownloader.download_ai_file(file, self.current_model_folder)
                    else:
                        logger.info(f"File {file.file_name} found in model folder {self.current_model_folder}.")

    def __check_hg_files(self):
        if self.source.hg_files is not None:
            pathutils.check_path(self.current_model_folder, True)

            for item in self.source.hg_files:
                current_item = os.path.join(self.current_model_folder, item.file_name)
                is_present = os.path.exists(current_item)
                item.local_path = current_item

                if not is_present:
                    logger.debug(f"Hugging face File {item.file_name} not found in model folder {self.current_model_folder}.")
                    AiDownloader.download_hg_file(item, self.current_model_folder)
                else:
                    logger.info(f"File {item} found in model folder {self.current_model_folder}.")

    def __check_ollama_server(self):
        logger.debug("Checking Ollama Server...")
        ollamaliz = Ollamaliz(self.setting.remote_url, True)
        # check status
        status = ollamaliz.check_ollama()
        if not status.is_successful():
            error = status.get_error()
            raise ValueError(f"Ollama server not available: {error}")
        else:
            logger.debug("Ollama Server is available.")
        # check models
        logger.debug("Checking if model is available in Ollama Server...")
        current_model = self.setting.source.model_name
        ollamaliz.check_model(current_model)

    def __check_lmstudio_server(self):
        logger.debug("Checking LMStudio Server...")
        studio = LmmStudioController(self.setting.remote_url)
        status = exec_get(self.setting.remote_url)
        if not status.is_successful():
            error = status.get_error()
            raise ValueError(f"LmStudio server not available: {error}")
        else:
            logger.debug("LmStudio Server is available.")
        # check models
        model_id = self.setting.source.model_name
        logger.debug(f"Checking if model {model_id} is available in Ollama Server...")
        has_model = studio.has_model_loaded(model_id)
        if not has_model:
            raise ValueError(f"Model {model_id} not found in LmStudio Server.")

    def check_params(self):
        setting = self.setting
        logger.debug(f"Checking parameters for model {setting.model.value}...")
        if setting.source_type == AiSourceType.OLLAMA_SERVER and setting.remote_url is None:
            raise ValueError("Remote URL is required for Ollama Server.")
        if setting.source_type == AiSourceType.LMSTUDIO_SERVER and setting.remote_url is None:
            raise ValueError("Remote URL is required for LM Studio Server.")
        if setting.source_type == AiSourceType.API_MISTRAL and setting.api_key is None:
            raise ValueError("API Key is required for Mistral API.")
        if setting.source_type == AiSourceType.API_MISTRAL and setting.api_key is None:
            raise ValueError("API Key is required for Gemini API.")
        if setting.source_type == AiSourceType.LOCAL_WHISPER and setting.download_type is None:
            raise ValueError("Download type is required for Whisper.")
        if setting.model == AiModelList.OLlAMA_CUSTOM and setting.model_custom is None:
            raise ValueError("Ollama model ID is required for custom model.")
        if setting.return_type is AiReturnType.OBJECT and setting.return_type_object is None:
            raise ValueError("Return type object is required for object return type.")
        if setting.source_type == AiSourceType.LOCAL_LLAMACPP and setting.download_type is AiDownloadType.WEB_FILES:
            if not osutils.is_os_unix():
                raise ValueError("LLamaCpp requires Unix OS. Change download type to DEFAULT.")


    def check_source(self):
        logger.debug(f"Checking source requirements for model {self.source.model_name} of env type {self.source.env}...")
        if self.source.env == AiEnvType.REMOTE:
            if not is_internet_available():
                logger.error("Internet connection is not available on this pc.")
                raise ValueError("Internet connection is not available on this pc.")
            else:
                logger.debug("Internet connection is available on this pc.")
            if self.setting.source_type == AiSourceType.OLLAMA_SERVER:
                self.__check_ollama_server()
            elif self.setting.source_type == AiSourceType.LMSTUDIO_SERVER:
                self.__check_lmstudio_server()
        elif self.source.env == AiEnvType.LOCAL:
            self.__check_ai_files()
            self.__check_hg_files()
        else:
            raise ValueError(f"Environment type not found: {self.source.env}.")

