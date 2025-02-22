import unittest


import sys
import os
from dotenv import load_dotenv
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiQuery
from pylizai.core.ai_source_type import AiSourceType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from pylizai.model.ai_prompts import AiPrompt
from test.pylizAiTest import PylizAiTest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestLmStudio(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()


    def test_image(self):
        setting = AiSetting(
                    model=AiModelList.GEMINI,
                    source_type=AiSourceType.API_GEMINI,
                    power=AiPower.LOW,
                    api_key=os.getenv('GEMINI_API_KEY'),
                    return_type=AiReturnType.OBJECT,
                    return_type_object=AiPayloadMediaInfo
                )
        self.testObj.run_and_handle_result(self, AiQuery(setting=setting, prompt=AiPrompt.IMAGE_VISION_DETAILED_1.value, payload_path=os.getenv("LOCAL_IMAGE_FOR_TEST")))


    # def test1(self):
    #     self.pyliz_dir = PylizDir(".pyliztest")
    #     setting = AiSetting(
    #         model=AiModelList.GEMINI,
    #         source_type=AiSourceType.API_GEMINI,
    #         power=AiPower.LOW,
    #         api_key=os.getenv('GEMINI_API_KEY'),
    #     )
    #     query = AiQuery(setting=setting, prompt="Analyze this image and tell what you see", payload_path=os.getenv("LOCAL_IMAGE_FOR_TEST"))
    #     result = AiRunner(self.pyliz_dir, query).run()
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





if __name__ == "__main__":
    unittest.main()