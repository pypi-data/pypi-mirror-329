import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime

from typing import Optional

from loguru import logger
from pylizlib.os.pathutils import check_path

from pylizai.core.ai_setting import AiQuery


@dataclass
class AiRunnerLog:
    enabled: bool = False
    folder_log_path: str = ""
    completion_status: bool = False
    runner_start_string: Optional[str] = None
    runner_end_string: Optional[str] = None
    runner_start_timer: Optional[float] = None
    runner_end_timer: Optional[float] = None
    runner_duration: Optional[float] = None
    queries: Optional[dict[str, AiQuery]] = field(default_factory=dict)
    queries_status: Optional[dict[str, bool]] = field(default_factory=dict)
    queries_start_str: Optional[dict[str, str]] = field(default_factory=dict)
    queries_end_str: Optional[dict[str, str]] = field(default_factory=dict)
    queries_start_timer: Optional[dict[str, float]] = field(default_factory=dict)
    queries_end_timer: Optional[dict[str, float]] = field(default_factory=dict)
    queries_duration: Optional[dict[str, float]] = field(default_factory=dict)
    queries_results_str: Optional[dict[str, str]] = field(default_factory=dict)


    TIMER_FORMAT = "%Y-%m-%d at %H:%M:%S"

    def set_start(self):
        self.runner_start_string = datetime.now().strftime(self.TIMER_FORMAT)
        self.runner_start_timer = time.perf_counter()

    def set_query_start(self, query_id: str):
        self.queries_start_str[query_id] = datetime.now().strftime(self.TIMER_FORMAT)
        self.queries_start_timer[query_id] = time.perf_counter()

    def set_end(self):
        self.runner_end_string = datetime.now().strftime(self.TIMER_FORMAT)
        self.runner_end_timer = time.perf_counter()
        self.runner_duration = self.runner_end_timer - self.runner_start_timer

    def set_query_end(self, query_id: str):
        self.queries_end_str[query_id] = datetime.now().strftime(self.TIMER_FORMAT)
        self.queries_end_timer[query_id] = time.perf_counter()
        self.queries_duration[query_id] = self.queries_end_timer[query_id] - self.queries_start_timer[query_id]

    def set_completion_status(self, status: bool):
        self.completion_status = status

    def add_query_obj(self, query: AiQuery):
        self.queries[query.id] = query

    def add_query_result(self, query_id: str, result: str):
        self.queries_results_str[query_id] = result

    def set_query_status(self, query_id: str, status: bool):
        self.queries_status[query_id] = status

    def __get_queries_data(self):
        data = {}
        for query_id, query in self.queries.items():
            data[query_id] = {
                "start_time": self.queries_start_str.get(query_id),
                "end_time": self.queries_end_str.get(query_id),
                "duration": self.queries_duration.get(query_id),
                "payload_path": query.payload_path,
                "status": self.queries_status.get(query_id),
                "prompt": query.prompt,
                "result": self.queries_results_str.get(query_id)
            }
        return data

    def __get_current_data(self):
        return {
            "time_start": self.runner_start_string,
            "time_end": self.runner_end_string,
            "duration": self.runner_duration,
            "status": self.completion_status,
            "queries": self.__get_queries_data()
        }

    def save_runner_log(self):
        day_str = datetime.now().strftime("%Y%m%d")
        folder = os.path.join(self.folder_log_path, day_str)
        check_path(folder, True)
        current_time = datetime.now().strftime("%H%M%S")
        file_name = f"runner_log_{current_time}.json"
        file_path = os.path.join(folder, file_name)
        try:
            data = self.__get_current_data()
            json_string = json.dumps(data, indent=4)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json_string)
        except Exception as e:
            logger.error(f"Error while saving runner log: {str(e)}")


