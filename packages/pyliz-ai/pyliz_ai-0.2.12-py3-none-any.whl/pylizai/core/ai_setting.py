import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Type, Optional, List

from pydantic import BaseModel
from pylizlib.data import datautils
from pylizlib.os import fileutils

from pylizai.core.ai_models import AiModels
from pylizai.core.ai_source import AiSource
from pylizai.core.ai_source_type import AiSourceType
from pylizai.llm.ollamaliz import Ollamaliz
from loguru import logger
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList, AiModelType
from pylizai.model.ai_power import AiPower




@dataclass
class AiSetting:
    model: AiModelList
    source_type: AiSourceType
    power: AiPower = AiPower.LOW
    model_custom: Optional[str] = None
    remote_url: Optional[str] = None
    api_key: Optional[str] = None
    return_type: AiReturnType = AiReturnType.STRING
    return_type_object: Optional[Type[BaseModel]] = None
    download_type: AiDownloadType = AiDownloadType.DEFAULT
    source: Optional[AiSource] = None
    model_runner_path: Optional[str] = None
    id: str = field(default_factory=lambda: datautils.gen_random_string(5))
    name: Optional[str] = None

    def __post_init__(self):
        self.setup_source()
        self.setup_predefined_defaults()

    def get_model_id(self):
        if not self.model_custom:
            return self.model.value
        else:
            return f"{self.model_custom}"

    def setup_source(self):
        if self.model == AiModelList.LLAVA:
            self.source = AiModels.Llava.get_llava(self.power, self.source_type)
        elif self.model == AiModelList.OPEN_MISTRAL:
            self.source = AiModels.Mistral.get_open_mistral()
        elif self.model == AiModelList.PIXSTRAL:
            self.source = AiModels.Mistral.get_pixstral()
        elif self.model == AiModelList.GEMINI:
            self.source = AiModels.Gemini.get_flash()
        elif self.model == AiModelList.WHISPER:
            self.source = AiModels.Whisper.get_whisper(self.download_type, self.power)
        elif self.model == AiModelList.LLAMA_3:
            self.source = AiModels.Llama.get_llama_3(self.source_type)
        elif self.model == AiModelList.LLAMA_32:
            self.source = AiModels.Llama.get_llama_32(self.source_type)
        elif self.model == AiModelList.OLlAMA_CUSTOM:
            self.source = AiModels.get_custom_ollama(self.source_type, self.model_custom)
        else:
            raise ValueError(f"Model not found: {self.model}.")

    def setup_predefined_defaults(self):
        if self.source_type == AiSourceType.OLLAMA_SERVER:
            if self.remote_url is None:
                self.remote_url = Ollamaliz.OLLAMA_HTTP_LOCALHOST_URL

    def set_return_type(self, return_type: AiReturnType, return_type_object: Any | None = None):
        self.return_type = return_type
        self.return_type_object = return_type_object

    def override_return_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        if return_type != self.return_type or self.return_type_object != return_type_object:
            logger.warning(f"Overriding ai_setting return type to {return_type} and return type object to {return_type_object}")
        self.return_type = return_type
        self.return_type_object = return_type_object

    def get_model_local_path(self):
        if self.download_type == AiDownloadType.HG_FILES:
            return self.source.hg_files[0].local_path



class AiSettingEssential(BaseModel):
    model: AiModelList
    source_type: AiSourceType
    power: AiPower = AiPower.LOW
    model_custom: Optional[str] = None
    remote_url: Optional[str] = None
    api_key: Optional[str] = None

    def to_setting(self) -> AiSetting:
        return AiSetting(
            model=self.model,
            source_type=self.source_type,
            power=self.power,
            model_custom=self.model_custom,
            remote_url=self.remote_url,
            api_key=self.api_key
        )



class AiQueryType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"



class AiQuery:
    setting: AiSetting
    prompt: str | None
    payload_path: str | None = None

    def __init__(
            self,
            setting: AiSetting,
            prompt: str | None,
            payload_path: str | None = None,
            save_text_result: bool = True,
            save_obj_result: bool = True,
            save_ai_setting: bool = True
    ):
        self.setting = setting
        self.prompt = prompt
        self.payload_path = payload_path
        self.query_type = None
        self.save_text_result = save_text_result
        self.save_obj_result = save_obj_result
        self.save_ai_setting = save_ai_setting
        self.id = datautils.gen_random_string(10)

        if self.payload_path is not None:
            if fileutils.is_image_file(self.payload_path):
                self.query_type = AiQueryType.IMAGE
            elif fileutils.is_video_file(self.payload_path):
                self.query_type = AiQueryType.VIDEO
            elif fileutils.is_audio_file(self.payload_path):
                self.query_type = AiQueryType.AUDIO
        else:
            self.query_type = AiQueryType.TEXT



class AiQueries:
    settings: list[AiSetting]
    prompt: str | None
    payload_path_list: list[str] | None = None

    def __init__(
            self, prompt: str | None,
            settings: Optional[List[AiSetting]] = None,
            payload_path_list: Optional[List[str]] = None
    ):
        self.settings = settings
        self.prompt = prompt
        self.payload_path_list = payload_path_list
        self.query_type = None

    def add_payload_path(self, payload_path: str):
        if self.payload_path_list is None:
            self.payload_path_list = []
        self.payload_path_list.append(payload_path)

    def add_setting(self, setting: AiSetting):
        if self.settings is None:
            self.settings = []
        self.settings.append(setting)



@dataclass
class AiSettingCombo:
    ai_image: AiSetting
    ai_text: AiSetting
    ai_audio: AiSetting | None = None

    def override_img_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        self.ai_image.override_return_type(return_type, return_type_object)

    def override_text_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        self.ai_text.override_return_type(return_type, return_type_object)

    def override_audio_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        self.ai_audio.override_return_type(return_type, return_type_object) if self.ai_audio is not None else None


@dataclass
class AiSettingComboList:
    list_image: list[AiSetting]
    list_text: list[AiSetting]
    list_audio: list[AiSetting] | None = None

    def override_img_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        for ai in self.list_image:
            ai.override_return_type(return_type, return_type_object)

    def override_text_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        for ai in self.list_text:
            ai.override_return_type(return_type, return_type_object)

    def override_audio_ret_type(self, return_type: AiReturnType, return_type_object: Type[BaseModel] | None = None):
        if self.list_audio is not None:
            for ai in self.list_audio:
                ai.override_return_type(return_type, return_type_object)