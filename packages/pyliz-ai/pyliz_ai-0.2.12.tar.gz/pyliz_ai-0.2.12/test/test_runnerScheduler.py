
import os
import unittest

from pylizlib.os import fileutils
from pylizlib.os.pathutils import scan_directory_match_bool
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiQuery, AiQueries
from pylizai.core.ai_source_type import AiSourceType
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from pylizai.model.ai_prompts import AiPrompt
from pylizai.runner.ai_runner import AiRunner, AiPoolRunner
from test.pylizAiTest import PylizAiTest


class TestRunnerScheduler(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_1 = AiSetting(
            model=AiModelList.LLAVA,
            source_type=AiSourceType.OLLAMA_SERVER,
            power=AiPower.LOW,
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo
        )
        self.ai_2 = AiSetting(
            model=AiModelList.GEMINI,
            source_type=AiSourceType.API_GEMINI,
            power=AiPower.LOW,
            api_key=os.getenv("GEMINI_API_KEY"),
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo
        )
        self.ai_3 = AiSetting(
            model=AiModelList.PIXSTRAL,
            source_type=AiSourceType.API_MISTRAL,
            power=AiPower.LOW,
            api_key=os.getenv("MISTRAL_API_KEY"),
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo
        )


    def test1(self):
        runner = AiRunner(self.testObj.pyliz_dir)
        paths = scan_directory_match_bool("/Users/gabliz/Pictures/Test", fileutils.is_image_file)
        queries = AiQueries(AiPrompt.IMAGE_VISION_JSON.value, [self.ai_1, self.ai_3], paths)
        scheduler = AiPoolRunner(runner, queries)
        scheduler.start()
        results = scheduler.results
        print("")

    def test2(self):
        runner = AiRunner(self.testObj.pyliz_dir)
        paths = scan_directory_match_bool(os.getenv("LOCAL_IMAGES_FOLDER_TEST"), fileutils.is_image_file)
        queries = AiQueries(AiPrompt.IMAGE_VISION_JSON.value, [self.ai_1, self.ai_2, self.ai_3], paths)
        results = runner.run_multiple(queries)
        print("")

if __name__ == "__main__":
    unittest.main()