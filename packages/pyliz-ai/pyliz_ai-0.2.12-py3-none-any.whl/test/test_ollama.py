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


class TestOllama(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()


    def test_text(self):
        setting = AiSetting(
            model=AiModelList.LLAMA_32,
            source_type=AiSourceType.OLLAMA_SERVER,
            power=AiPower.LOW,
            remote_url=os.getenv('OLLAMA_LOCALHOST'),
        )
        self.testObj.run_and_handle_result(self, AiQuery(setting=setting, prompt="Why the sky is blue?"))


    def test_image(self):
        setting = AiSetting(
            model=AiModelList.LLAVA,
            source_type=AiSourceType.OLLAMA_SERVER,
            power=AiPower.LOW,
            remote_url=os.getenv('OLLAMA_LOCALHOST'),
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo
        )
        self.testObj.run_and_handle_result(self, AiQuery(setting=setting, prompt=AiPrompt.IMAGE_VISION_DETAILED_1.value, payload_path=os.getenv("LOCAL_IMAGE_FOR_TEST")))



if __name__ == "__main__":
    unittest.main()