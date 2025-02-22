import json
from typing import Dict, Any, List

from pylizlib.network.netres import NetResponse
from pylizlib.network.netutils import exec_get, exec_post

from pylizai.utils.ai_msg_gen import AiMessageGenerator

LMSTUDIO_PORT = "1234"
LMSTUDIO_HTTP_LOCALHOST_URL = "http://localhost:" + LMSTUDIO_PORT


class LmStudioModel:
    def __init__(self, id: str, object_type: str, owned_by: str):
        self.id = id
        self.object_type = object_type
        self.owned_by = owned_by

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LmStudioModel':
        return cls(
            id=data['id'],
            object_type=data['object'],
            owned_by=data['owned_by']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'object': self.object_type,
            'owned_by': self.owned_by
        }


class LmStudioModelList:
    def __init__(self, data: List[LmStudioModel], object_type: str):
        self.data = data
        self.object_type = object_type

    @classmethod
    def from_json(cls, json_string: str) -> 'LmStudioModelList':
        json_data = json.loads(json_string)
        models = [LmStudioModel.from_dict(item) for item in json_data['data']]
        return cls(data=models, object_type=json_data['object'])

    def to_json(self) -> str:
        return json.dumps({
            'data': [model.to_dict() for model in self.data],
            'object': self.object_type
        })



class LmmStudioController:

    def __init__(self, url: str):
        self.url = url

    def __get_installed_models_api(self) -> NetResponse:
        api_url = self.url + "/v1/models"
        return exec_get(api_url)

    def get_loaded_models(self) -> LmStudioModelList:
        call = self.__get_installed_models_api()
        if call.is_error():
            raise Exception(call.get_error())
        return LmStudioModelList.from_json(call.response.text)

    def has_model_loaded(self, model_id: str) -> bool:
        models = self.get_loaded_models()
        for model in models.data:
            if model.id == model_id:
                return True
        return False



    def run(self, query):
        model_id = query.setting.source.model_name
        open_ai_message = AiMessageGenerator.gen_message_lmstudio(query)
        payload = {
            "model": model_id,
            "messages": open_ai_message,
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        response: NetResponse = exec_post(self.url + "/v1/chat/completions", payload, headers)

        if response.is_error():
            raise Exception(response.get_error())

        output_dict = response.json
        result_dict = output_dict['choices'][0]['message']['content']

        result_str = json.dumps(result_dict, indent=4)

        return result_str
