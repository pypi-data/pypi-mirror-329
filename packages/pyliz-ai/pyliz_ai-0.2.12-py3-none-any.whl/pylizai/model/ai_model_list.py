from enum import Enum


class AiModelList(Enum):
    LLAVA = "llava"
    WHISPER = "whisper"
    PIXSTRAL = "pixstral"
    OPEN_MISTRAL = "open_mistral"
    GEMINI = "gemini"
    LLAMA_3 = "llama3"
    LLAMA_32 = "llama32"
    OLlAMA_CUSTOM = "ollama_custom"


class AiModelType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CUSTOM = "custom"
