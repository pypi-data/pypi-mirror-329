
import os
import unittest

from pylizai.core.ai_setting import AiSetting, AiQuery
from pylizai.core.ai_source_type import AiSourceType
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from pylizai.model.ai_prompts import AiPrompt
from test.pylizAiTest import PylizAiTest


class TestLlamaCPP(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_1 = AiSetting(
            model=AiModelList.LLAMA_3,
            source_type=AiSourceType.LOCAL_LLAMACPP,
            power=AiPower.LOW,
        )
        self.ai_2 = AiSetting(
            model=AiModelList.LLAVA,
            source_type=AiSourceType.LOCAL_LLAMACPP,
            power=AiPower.LOW,
            download_type=AiDownloadType.WEB_FILES
        )
        self.ai_3 = AiSetting(
            model=AiModelList.LLAVA,
            source_type=AiSourceType.LOCAL_LLAMACPP,
            power=AiPower.LOW,
        )


    def test_from_lib(self):
        self.testObj.run_and_handle_result(self, AiQuery(setting=self.ai_1, prompt="Why the sky is blue? make examples.",))

    def test_img_llava_from_lib(self):
        query = AiQuery(setting=self.ai_3, prompt=AiPrompt.IMAGE_VISION_DETAILED_1.value, payload_path=os.getenv('LOCAL_IMAGE_FOR_TEST'))
        self.testObj.run_and_handle_result(self, query)

    def test_img_llava_from_git(self):
        query = AiQuery(setting=self.ai_2, prompt=AiPrompt.IMAGE_VISION_DETAILED_1.value, payload_path=os.getenv('LOCAL_IMAGE_FOR_TEST'))
        self.testObj.run_and_handle_result(self, query)


if __name__ == "__main__":
    unittest.main()