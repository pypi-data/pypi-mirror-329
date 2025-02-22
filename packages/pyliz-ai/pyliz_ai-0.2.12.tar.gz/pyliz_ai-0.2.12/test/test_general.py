import unittest

import sys
import os

from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiQuery, AiSettingEssential
from pylizai.core.ai_source_type import AiSourceType
from pylizai.llm.lmstudio import LmmStudioController
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_prompts import AiPrompt
from test.pylizAiTest import PylizAiTest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGeneral(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_set_1 = AiSetting(
            model=AiModelList.LLAVA,
            remote_url=os.getenv("LMSTUDIO_LOCALHOST_URL"),
            source_type=AiSourceType.LMSTUDIO_SERVER,
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo,
        )
        self.ai_2 = AiSettingEssential(
            model=AiModelList.LLAVA,
            remote_url=os.getenv("LMSTUDIO_LOCALHOST_URL"),
            source_type=AiSourceType.LMSTUDIO_SERVER,
        )


    def test_1(self):
        json = self.ai_2.model_dump_json()
        print(json)
        obj_from_json = AiSettingEssential.model_validate_json(json)
        print(obj_from_json)


if __name__ == "__main__":
    unittest.main()