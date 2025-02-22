from pylizai.core.ai_source_type import AiSourceType
from pylizai.model.ai_model_list import AiModelList


class AiPyliz:

    @staticmethod
    def is_verified_source_type(source_type: AiSourceType) -> bool:
        blacklist = [AiSourceType.LMSTUDIO_SERVER, AiSourceType.LOCAL_LLAMACPP]
        return source_type not in blacklist

    @staticmethod
    def is_verified_model(model: AiModelList) -> bool:
        blacklist = [AiModelList.LLAMA_3]
        return model not in blacklist

    @staticmethod
    def has_source_type_url(source_type: AiSourceType) -> bool:
        whitelist = [AiSourceType.OLLAMA_SERVER]
        return source_type in whitelist

    @staticmethod
    def has_model_vision(model: AiModelList) -> bool:
        whitelist = [AiModelList.LLAVA, AiModelList.PIXSTRAL, AiModelList.GEMINI]
        return model in whitelist

    @staticmethod
    def has_source_type_api_key(source_type: AiSourceType) -> bool:
        whitelist = [AiSourceType.API_MISTRAL, AiSourceType.API_GEMINI]
        return source_type in whitelist

    @staticmethod
    def get_models_from_source(source_type: AiSourceType, text: bool, vision: bool) -> list[AiModelList]:
        models: list[AiModelList] = []
        if source_type == AiSourceType.OLLAMA_SERVER:
            if text:
                models.append(AiModelList.LLAMA_32)
            if vision:
                models.append(AiModelList.LLAVA)
            models.append(AiModelList.OLlAMA_CUSTOM)
        elif source_type == AiSourceType.API_MISTRAL:
            if text:
                models.append(AiModelList.OPEN_MISTRAL)
            if vision:
                models.append(AiModelList.PIXSTRAL)
        for model in models:
            if not AiPyliz.is_verified_model(model):
                raise ValueError(f"Model {model} is not a verified model.")
        return models

    @staticmethod
    def get_verified_source_types() -> list[AiSourceType]:
        verified_source_types = []
        for source_type in AiSourceType:
            if AiPyliz.is_verified_source_type(source_type):
                verified_source_types.append(source_type)
        return verified_source_types

    @staticmethod
    def source_type_support_custom(source_type: AiSourceType) -> bool:
        return source_type == AiSourceType.OLLAMA_SERVER