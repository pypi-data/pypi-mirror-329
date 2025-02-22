import unittest


import sys
import os
from dotenv import load_dotenv
from pylizlib.config.pylizdir import PylizDir
from pylizlib.log import pylizLogging

from pylizai.core.ai_setting import AiSetting, AiQuery
from pylizai.core.ai_source_type import AiSourceType
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from pylizai.runner.ai_runner import AiRunner
from test.pylizAiTest import PylizAiTest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# noinspection DuplicatedCode
class TestWhisper(unittest.TestCase):


    def setUp(self):
        self.testObj = PylizAiTest()

    def test_local_from_web(self):
        setting = AiSetting(
            model=AiModelList.WHISPER,
            source_type=AiSourceType.LOCAL_WHISPER,
            power=AiPower.MEDIUM,
            download_type=AiDownloadType.WEB_FILES
        )
        self.testObj.run_and_handle_result(self, AiQuery(setting=setting, prompt=None, payload_path=os.getenv("LOCAL_VIDEO_2_FOR_TEST")))

    def test_local_from_hg_repo_segments(self):
        setting = AiSetting(
            model=AiModelList.WHISPER,
            source_type=AiSourceType.LOCAL_WHISPER,
            power=AiPower.MEDIUM,
            return_type=AiReturnType.AUDIO_SEGMENTS,
            download_type=AiDownloadType.HG_REPO
        )
        self.testObj.run_and_handle_result(self, AiQuery(setting=setting, prompt=None, payload_path=os.getenv("LOCAL_VIDEO_2_FOR_TEST")))



    # def test1(self):
    #     setting = AiSetting(
    #         model=AiModelList.WHISPER,
    #         source_type=AiSourceType.LOCAL_WHISPER,
    #         power=AiPower.MEDIUM,
    #         download_type=AiDownloadType.WEB_FILES
    #     )
    #     query = AiQuery(setting=setting, prompt=None, payload_path=os.getenv("LOCAL_VIDEO_2_FOR_TEST"))
    #     result = AiRunner(self.pyliz_dir).run(query)
    #     print("result status = " + str(result.status))
    #     print(result.payload)
    #     print("result error = " + result.error if result.error is not None else "No error")
    #
    #
    # def test2(self):
    #     self.pyliz_dir = PylizDir(".pyliztest")
    #     setting = AiSetting(
    #         model=AiModelList.GEMINI,
    #         source_type=AiSourceType.API_GEMINI,
    #         power=AiPower.LOW,
    #         api_key=os.getenv('GEMINI_API_KEY'),
    #     )
    #     query = AiQuery(setting=setting, prompt="Analyze this video and tell what you see", payload_path=os.getenv("LOCAL_VIDEO_FOR_TEST"))
    #     result = AiRunner(self.pyliz_dir, query).run()
    #     print("result status = " + str(result.status))
    #     print(result.payload)
    #     print("result error = \n" + result.error if result.error is not None else "No error")
    #
    #
    # def test3(self):
    #     self.pyliz_dir = PylizDir(".pyliztest")
    #     setting = AiSetting(
    #         model=AiModelList.WHISPER,
    #         source_type=AiSourceType.LOCAL_WHISPER,
    #         power=AiPower.LOW,
    #         download_type=AiDownloadType.HG_REPO,
    #         return_type=AiReturnType.AUDIO_SEGMENTS
    #     )
    #     query = AiQuery(setting=setting, prompt=None, payload_path=os.getenv("LOCAL_VIDEO_FOR_TEST"))
    #     result = AiRunner(self.pyliz_dir).run(query)
    #     print("result status = " + str(result.status))
    #     print(result.payload)
    #     print("result error = \n" + result.error if result.error is not None else "No error")





if __name__ == "__main__":
    unittest.main()