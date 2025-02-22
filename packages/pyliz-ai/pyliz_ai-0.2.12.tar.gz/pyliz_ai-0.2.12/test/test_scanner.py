
import unittest

import os
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiSettingCombo, AiSettingComboList
from pylizai.core.ai_source_type import AiSourceType
from pylizai.media.ai_image_scanner import AiImageScanningType
from pylizai.media.ai_media_scanner import AiMediaScanner
from pylizai.media.ai_video_scanner import AiVideoScanningType
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_model_list import AiModelList
from pylizai.model.ai_power import AiPower
from test.pylizAiTest import PylizAiTest



class TestScanner(unittest.TestCase):

    def setUp(self):
        self.testObj = PylizAiTest()
        self.ai_image_gemini_settings = AiSetting(
            model=AiModelList.GEMINI,
            source_type=AiSourceType.API_GEMINI,
            power=AiPower.LOW,
            api_key=os.getenv('GEMINI_API_KEY'),
        )
        self.ai_video_mistral_settings = AiSetting(
            model=AiModelList.OPEN_MISTRAL,
            source_type=AiSourceType.API_MISTRAL,
            power=AiPower.LOW,
            api_key=os.getenv('MISTRAL_API_KEY'),
        )
        self.ai_text_gemini_settings = AiSetting(
            model=AiModelList.OPEN_MISTRAL,
            source_type=AiSourceType.API_MISTRAL,
            power=AiPower.LOW,
            api_key=os.getenv('MISTRAL_API_KEY'),
        )
        self.ai_audio_settings = AiSetting(
            model=AiModelList.WHISPER,
            source_type=AiSourceType.LOCAL_WHISPER,
            power=AiPower.LOW,
        )
        self.ai_image_ollama_settings = AiSetting(
            model=AiModelList.LLAVA,
            source_type=AiSourceType.OLLAMA_SERVER,
            power=AiPower.LOW,
            remote_url=os.getenv('OLLAMA_LOCALHOST'),
            return_type=AiReturnType.OBJECT,
            return_type_object=AiPayloadMediaInfo
        )
        self.ai_text_ollama_settings = AiSetting(
            model=AiModelList.LLAMA_32,
            source_type=AiSourceType.OLLAMA_SERVER,
            power=AiPower.LOW,
            remote_url=os.getenv('OLLAMA_LOCALHOST'),
        )

    def test_scan_image(self):
        scanner = AiMediaScanner(self.testObj.pyliz_dir)
        result = scanner.scan_image(
            path=os.getenv("LOCAL_IMAGE_FOR_TEST"),
            scanning_type=AiImageScanningType.SINGLE_QUERY_ONLY_VISION,
            ai_image=self.ai_image_ollama_settings,
            ai_text=self.ai_text_ollama_settings
        )
        PylizAiTest.handle_result(self, result)

    def test_scan_video(self):
        scanner = AiMediaScanner(self.testObj.pyliz_dir)
        ai_combo = AiSettingCombo(self.ai_image_ollama_settings, self.ai_text_ollama_settings, self.ai_audio_settings)
        list_images = [self.ai_image_ollama_settings, self.ai_image_gemini_settings]
        list_text = [self.ai_text_ollama_settings]
        ai_combo_list = AiSettingComboList(list_images, list_text, [self.ai_audio_settings])
        result = scanner.scan_video(
            path=os.getenv("LOCAL_VIDEO_5_FOR_TEST"),
            scanning_type=AiVideoScanningType.PYLIZ,
            ai_combo_list=ai_combo_list,
        )
        PylizAiTest.handle_result(self, result)

    def test_scan_video_api(self):
        scanner = AiMediaScanner(self.testObj.pyliz_dir)
        result = scanner.scan_video(
            path=os.getenv("LOCAL_VIDEO_4_FOR_TEST"),
            scanning_type=AiVideoScanningType.DIRECT_API,
            ai_video_api=self.ai_video_mistral_settings
        )
        PylizAiTest.handle_result(self, result)

