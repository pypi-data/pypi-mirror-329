from pylizlib.config.pylizdir import PylizDir
from pylizlib.model.operation import Operation
from pylizmedia.liz_media import LizMedia
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiSettingComboList
from loguru import logger
from pylizai.media.ai_image_scanner import AiImageScanningType, AiImageScanner
from pylizai.media.ai_video_scanner import AiVideoScanningType, AiVideoScanner
from pylizai.model.ai_file_type import AiReturnType


class AiMediaScanner:

    def __init__(self, pyliz_dir: PylizDir):
        self.pyliz_dir = pyliz_dir



    def scan_image(
            self,
            path: str,
            ai_image: AiSetting,
            ai_text: AiSetting | None = None,
            scanning_type: AiImageScanningType = AiImageScanningType.SINGLE_QUERY_ONLY_VISION,
    ) -> Operation[LizMedia]:
        try:
            logger.info(f"Scanning image {path} with {scanning_type}")
            ai_image.override_return_type(AiReturnType.OBJECT, AiPayloadMediaInfo)
            ai_text.override_return_type(AiReturnType.STRING_JSON) if ai_text is not None else None
            media = LizMedia(path)
            scanner = AiImageScanner(self.pyliz_dir, scanning_type)
            ai_info = scanner.run(path, ai_image, ai_text)
            media.apply_ai_info(ai_info)
            return Operation(status=True, payload=media)
        except Exception as e:
            return Operation(status=False, error=str(e))

    def scan_video(
            self,
            path: str,
            scanning_type: AiVideoScanningType,
            ai_combo_list: AiSettingComboList | None = None,
            ai_video_api: AiSetting | None = None,
            ai_oso_text: AiSetting | None = None,
    ) -> Operation[LizMedia]:
        try:
            logger.info(f"Scanning video {path} with scanning {scanning_type}")
            media = LizMedia(path)
            scanner = AiVideoScanner(self.pyliz_dir, scanning_type)
            scanner.set_settings(ai_combo_list, ai_video_api, ai_oso_text)
            scanner.check()
            ai_info = scanner.run(path)
            media.apply_ai_info(ai_info)
            return Operation(status=True, payload=media)
        except Exception as e:
            return Operation(status=False, error=str(e))

    # def scan_video(
    #         self,
    #         path: str,
    #         scanning_type: AiVideoScanningType,
    #         ai_image: AiSetting,
    #         ai_text: AiSetting,
    #         ai_audio: AiSetting | None = None,
    # ):
    #     try:
    #         logger.info(f"Scanning video {path} with scanning {scanning_type}")
    #         media = LizMedia(path)
    #         scanner = AiVideoScanner(self.pyliz_dir, scanning_type)
    #         ai_info = scanner.run_with_runner(path, ai_image, ai_text, ai_audio)
    #         media.apply_ai_info(ai_info)
    #         return Operation(status=True, payload=media)
    #     except Exception as e:
    #         return Operation(status=False, error=str(e))
    #
    #
    # def scan_video_direct(self, path: str, ai_video: AiSetting):
    #     if not fileutils.is_video_file(path):
    #         return Operation(status=False, error=f"Path {path} is not an video file.")
    #     try:
    #         # logger.info(f"Scanning video {path} directly")
    #         # media = LizMedia(path)
    #         # result = AiCommonRunner.run_query(self.pyliz_dir, ai_video, AiPrompt.VIDEO_EASY_1.value, path, )
    #         # ai_info = scanner.run(path, ai_image, ai_text)
    #         # media.apply_ai_info(ai_info)
    #         return None
    #     except Exception as e:
    #         return Operation(status=False, error=str(e))
