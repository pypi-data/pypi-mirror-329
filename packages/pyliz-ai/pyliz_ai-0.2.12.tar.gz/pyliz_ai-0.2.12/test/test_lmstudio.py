import unittest

import sys
import os

from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiQuery
from pylizai.core.ai_source_type import AiSourceType
from pylizai.llm.lmstudio import LmmStudioController
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_prompts import AiPrompt
from test.pylizAiTest import PylizAiTest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestLmStudio(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_set_1 = AiSetting(
            model=AiModelList.LLAVA,
            remote_url=os.getenv("LMSTUDIO_LOCALHOST_URL"),
            source_type=AiSourceType.LMSTUDIO_SERVER,
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo,
        )
        self.query_api_test = AiQuery(self.ai_set_1, AiPrompt.IMAGE_VISION_JSON.value, payload_path=os.getenv("LOCAL_IMAGE_FOR_TEST"))
        self.query_1 = AiQuery(self.ai_set_1, AiPrompt.IMAGE_VISION_JSON.value, payload_path=os.getenv("LOCAL_IMAGE_FOR_TEST"))


    def test_get_models(self):
        liz = LmmStudioController(os.getenv('LMSTUDIO_LOCALHOST_URL'))
        obj = liz.get_loaded_models()
        print(obj.data[0].id)

    def test2(self):
        import http.client
        conn = http.client.HTTPConnection("192.168.0.253", 1234)
        conn.request("GET", "/v1/models")
        response = conn.getresponse()

        print(response.status, response.reason)
        data = response.read()
        print(data)

    def test_query_api(self):
        liz = LmmStudioController(os.getenv('LMSTUDIO_LOCALHOST_URL'))
        result = liz.run(self.query_api_test)
        print(result)

    def test_query(self):
        self.testObj.run_and_handle_result(self, self.query_1)



if __name__ == "__main__":
    unittest.main()