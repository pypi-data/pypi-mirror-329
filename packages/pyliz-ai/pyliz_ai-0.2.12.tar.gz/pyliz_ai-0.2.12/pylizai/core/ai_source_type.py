from enum import Enum

from pylizai.llm.lmstudio import LMSTUDIO_HTTP_LOCALHOST_URL
from pylizai.llm.ollamaliz import Ollamaliz


class AiSourceType(Enum):
    OLLAMA_SERVER = "Ollama server"
    LMSTUDIO_SERVER = "LMM studio server"
    LOCAL_LLAMACPP = "Local (Llamacpp)"
    LOCAL_WHISPER = "Local (Whisper)"
    API_MISTRAL = "Mistral API"
    API_GEMINI = "Gemini API"

    def get_default_remote_url(self) -> str:
        if self == AiSourceType.OLLAMA_SERVER:
            return Ollamaliz.OLLAMA_HTTP_LOCALHOST_URL
        if self == AiSourceType.LMSTUDIO_SERVER:
            return LMSTUDIO_HTTP_LOCALHOST_URL


