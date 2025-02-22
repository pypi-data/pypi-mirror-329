from mistralai import Mistral

from pylizai.core.ai_setting import AiQuery, AiQueryType
from loguru import logger
from pylizai.model.ai_file_type import AiReturnType
from pylizai.utils.ai_msg_gen import AiMessageGenerator


class MistralController:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def run(self, query: AiQuery):
        model_name = query.setting.source.model_name
        json = query.setting.return_type == AiReturnType.STRING_JSON
        client = Mistral(api_key=self.api_key)
        logger.debug(f"Running Mistral with model: {model_name}")
        chat_response = client.chat.complete(
            model=model_name,
            messages=AiMessageGenerator.gen_message_mistral(query),
            response_format={"type": "json_object"} if json else None
        )
        return chat_response.choices[0].message.content
