from enum import Enum


class AiDownloadType(Enum):
    DEFAULT = "Default",
    PYTHON_LIB = "Python library",
    HG_FILES = "Huggingface files",
    HG_REPO = "Huggingface repository",
    WEB_FILES = "WEB files"