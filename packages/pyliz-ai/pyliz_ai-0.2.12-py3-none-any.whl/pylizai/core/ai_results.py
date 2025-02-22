import json
import os
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel
from pylizlib.config.pylizdir import PylizDir, PylizDirFoldersTemplate
from pylizlib.data.jsonUtils import JsonUtils
from pylizlib.os.pathutils import check_path


from loguru import logger

from pylizai.core.ai_setting import AiSetting
from pylizai.model.ai_exctps import AiRunnerException
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_runner_log import AiRunnerLog

T = TypeVar('T')


class AiResult:


    def __init__(
            self,
            pyliz_dir: PylizDir,
            setting: AiSetting,
            str_results: str,
    ):
        from pylizai.core.ai_setting import AiSetting, AiQuery
        self.pyliz_dir = pyliz_dir
        self.setting: AiSetting = setting
        self.str_results = str_results
        self.output: T | None = None
        self.__gen_output()
        self.path_results = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.RESULTS, True)

    # def __get_query_result_folder(self) -> str:
    #     folder = os.path.join(self.path_results, self.query.id)
    #     check_path(folder, True)
    #     return str(folder)

    def __get_today_folder_result_path(self) -> str:
        day_str = datetime.now().strftime("%Y%m%d")
        folder = os.path.join(self.path_results, day_str, self.setting.model.value)
        check_path(folder, True)
        return str(folder)

    def __save_str_result(self):
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(self.__get_today_folder_result_path(), file_name)
        with open(file_path, "w") as file:
            file.write(self.str_results)

    def __save_obj_results(self):
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = os.path.join(self.__get_today_folder_result_path(), file_name)
        json = self.output.model_dump_json()
        with open(file_path, "w") as file:
            file.write(json)

    # def __save_setting(self):
    #     filename = "ai_setting.json"
    #     file_path = os.path.join(self.__get_query_result_folder(), filename)


    def __convert_to_object(self):
        logger.trace(f"Converting result to custom object {self.setting.return_type_object.__name__}...")
        assert isinstance(self.setting.return_type_object, type), "Return type object must be a class."
        assert issubclass(self.setting.return_type_object, BaseModel), "Return type object must extend BaseModel."
        cleaned_json = JsonUtils.clean_json_apici(self.str_results)
        data = json.loads(cleaned_json)
        obj = self.setting.return_type_object(**data)
        return obj


    def __gen_output(self):
        try:
            if self.setting.return_type == AiReturnType.OBJECT:
                if self.setting.return_type_object is None:
                    raise ValueError("Return type object is not set in query setting.")
                self.output = self.__convert_to_object()
            else:
                self.output = self.str_results
        except Exception as e:
            raise AiRunnerException(f"Error while handling ai results: {str(e)}")

    def add_results_to_runner_log(self, query_id: str, runner_log: AiRunnerLog):
        runner_log.add_query_result(query_id, self.str_results)

    def save_results(
            self,
            save_str: bool = True,
            save_obj: bool = True,
            save_setting: bool = True
    ):
        try:
            if save_str:
                self.__save_str_result()
            if self.setting.return_type == AiReturnType.OBJECT and save_obj:
                self.__save_obj_results()
        except Exception as e:
            logger.error(f"Error while saving results to disk: {e}")


    def get_output(self):
        return self.output

