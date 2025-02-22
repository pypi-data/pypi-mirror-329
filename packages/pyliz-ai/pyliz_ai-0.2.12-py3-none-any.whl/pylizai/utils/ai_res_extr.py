import json
import re

from pydantic import BaseModel
from pylizlib.data.jsonUtils import JsonUtils
from pylizlib.model.operation import Operation, T
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiQuery
from loguru import logger
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_prompts import AiPrompt


class AiResultExtractor:





    @staticmethod
    def __handle_text_extract_from_vision_1(ai_text_result: str):
        logger.debug(f"Extracting json info from ai_text_result...")
        json_result_text = ai_text_result
        if not JsonUtils.is_valid_json(json_result_text):
            raise ValueError("Ai returned invalid json")
        if not JsonUtils.has_keys(json_result_text, ["text", "tags", "filename"]):
            raise ValueError("Ai returned invalid json keys")
        try:
            data = json.loads(json_result_text)
        except json.JSONDecodeError:
            raise ValueError("Unable to decode json")
        ai_info = AiPayloadMediaInfo(
            text=data['text'],
            tags=data['tags'],
            filename=data['filename'],
            description=ai_text_result,
        )
        return ai_info

    @staticmethod
    def __handle_text_extract_from_multiple_vision(ai_text_result: str):
        logger.debug(f"Extracting json info from ai_text_result...")
        json_result_text = ai_text_result
        if not JsonUtils.is_valid_json(json_result_text):
            raise ValueError("Ai returned invalid json")
        if not JsonUtils.has_keys(json_result_text, ["text", "tags", "filename", "description"]):
            raise ValueError("Ai returned invalid json keys")
        try:
            data = json.loads(json_result_text)
        except json.JSONDecodeError:
            raise ValueError("Unable to decode json")
        ai_info = AiPayloadMediaInfo(
            text=data['text'],
            tags=data['tags'],
            filename=data['filename'],
            description=data['description'],
        )
        return ai_info

    @staticmethod
    def __handle_text_extract_from_image_vision_json(ai_image_json: str):
        logger.debug(f"Extracting json info from ai_image_json...")
        json_result_text = ai_image_json
        if not JsonUtils.is_valid_json(json_result_text):
            raise ValueError("Ai returned invalid json")
        if not JsonUtils.has_keys(json_result_text, ["text", "tags", "filename", "description"]):
            raise ValueError("Ai returned invalid json keys")
        try:
            data = json.loads(json_result_text)
        except json.JSONDecodeError:
            raise ValueError("Unable to decode json")
        ai_info = AiPayloadMediaInfo(
            text=data['text'],
            tags=data['tags'],
            filename=data['filename'],
            description=data['description'],
        )
        return ai_info

    @staticmethod
    def extract(result: str, prompt: AiPrompt):
        if prompt == AiPrompt.TEXT_EXTRACT_FROM_VISION_1:
            return AiResultExtractor.__handle_text_extract_from_vision_1(result)
        elif prompt == AiPrompt.TEXT_EXTRACT_FROM_MULTIPLE_VISION:
            return AiResultExtractor.__handle_text_extract_from_multiple_vision(result)
        elif prompt == AiPrompt.IMAGE_VISION_JSON:
            return AiResultExtractor.__handle_text_extract_from_image_vision_json(result)
        else:
            raise ValueError(f"Prompt not supported: {prompt}")