import unittest
from typing import TypeVar

from dotenv import load_dotenv
from loguru import logger
from pylizlib.config.pylizdir import PylizDir
from pylizlib.log.pylizLogging import LOGGER_PYLIZ_LIB_NAME
from pylizlib.model.operation import Operation
from pylizmedia.log.pylizMediaLogging import LOGGER_PYLIZ_MEDIA_NAME

from pylizai.log.pylizAiLogging import LOGGER_PYLIZ_AI_NAME, pyblizai_log_test
from pylizai.runner.ai_runner import AiRunner

T = TypeVar('T')


class PylizAiTest:

    def __init__(self):
        load_dotenv()
        # logger.enable(LOGGER_PYLIZ_MEDIA_NAME)
        # logger.enable(LOGGER_PYLIZ_LIB_NAME)
        # logger.enable(LOGGER_PYLIZ_AI_NAME)
        self.pyliz_dir = PylizDir(".pyliz")
        self.pyliz_dir.add_all_template_folders()

    def run_and_handle_result(self, test: unittest.TestCase, query ):
        result = AiRunner(self.pyliz_dir).run(query)
        PylizAiTest.handle_result(test, result)


    @staticmethod
    def handle_result(test: unittest.TestCase, result: Operation[T], is_array=False):
        print("result status = " + str(result.status))
        print("----------------------")
        if is_array:
            for item in result.payload:
                print(item)
        else:
            print(result.payload)
        if result.status is False:
            print("result error = " + result.error if result.error is not None else "No error")
        test.assertEqual(result.status, True)
