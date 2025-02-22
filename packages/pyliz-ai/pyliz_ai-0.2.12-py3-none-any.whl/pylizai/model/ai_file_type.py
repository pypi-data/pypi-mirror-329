from enum import Enum

from pylizlib.network import netutils


class AiFileType(Enum):
    HG_MMPROJ = "mmproj"
    HG_GGML = "ggml"
    PT = "pt"


class AiReturnType(Enum):
    STRING = "string"
    AUDIO_SEGMENTS = "audio_segments"
    STRING_JSON = "string_json"
    OBJECT = "object"


class AiFile:
    def __init__(
            self,
            file_name: str,
            url: str,
            file_type: AiFileType
    ):
        self.file_name = file_name
        self.url = url
        self.file_type = file_type
        self.local_path = None

    def get_file_size_byte(self) -> int:
        return netutils.get_file_size_byte(self.url)


class AiHgFile:
    def __init__(
            self,
            repository: str,
            file_name: str | None = None,
    ):
        self.repository = repository
        self.file_name = file_name
        self.local_path: str | None = None


class AiPackage:
    def __init__(
            self,
            url: str,
    ):
        self.url = url