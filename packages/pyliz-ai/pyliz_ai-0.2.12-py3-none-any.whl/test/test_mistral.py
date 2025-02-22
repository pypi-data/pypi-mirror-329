import unittest


import sys
import os

from pylizai.core.ai_setting import AiSetting
from pylizai.core.ai_source_type import AiSourceType
from pylizai.media.ai_image_scanner import AiImageScanningType
from pylizai.media.ai_media_scanner import AiMediaScanner
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from test.pylizAiTest import PylizAiTest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMistral(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_image_gemini_settings = AiSetting(
            model=AiModelList.PIXSTRAL,
            source_type=AiSourceType.API_MISTRAL,
            power=AiPower.LOW,
            api_key=os.getenv('MISTRAL_API_KEY'),
        )

    def test_scan_image(self):
        scanner = AiMediaScanner(self.testObj.pyliz_dir)
        result = scanner.scan_image(
            path=os.getenv("LOCAL_IMAGE_FOR_TEST"),
            scanning_type=AiImageScanningType.SINGLE_QUERY_ONLY_VISION,
            ai_image=self.ai_image_gemini_settings,
        )
        PylizAiTest.handle_result(self, result)



    # def setUp(self):
    #     load_dotenv()
    #     print("Setting up test...")
    #
    #
    # def test1(self):
    #     setting = AiSetting(
    #         model=AiModelList.OPEN_MISTRAL,
    #         source_type=AiSourceType.API_MISTRAL,
    #         power=AiPower.LOW,
    #         api_key=os.getenv('MISTRAL_API_KEY'),
    #     )
    #     inputs = AiInputs(prompt="Why is the sky blue? answer in 20 words or less")
    #     result = AiRunner(setting, inputs).run_with_runner()
    #     print(result.payload)
    #
    #
    # def test2(self):
    #     setting = AiSetting(
    #         model=AiModelList.PIXSTRAL,
    #         source_type=AiSourceType.API_MISTRAL,
    #         power=AiPower.MEDIUM,
    #         api_key=os.getenv('MISTRAL_API_KEY'),
    #     )
    #     inputs = AiInputs(prompt=AiPrompt.VISION_DETAILED.value, file_path=os.getenv('LOCAL_IMAGE_FOR_TEST'))
    #     result = AiRunner(setting, inputs).run_with_runner()
    #     print("Local image for test: ", os.getenv('LOCAL_IMAGE_FOR_TEST'))
    #     print(f"Result status: {result.status}")
    #     print("Result error: ", result.error)
    #     print("Result payload: ", result.payload)




if __name__ == "__main__":
    unittest.main()