from enum import Enum

from loguru import logger
from pylizlib.config.pylizdir import PylizDir
from pylizlib.os import fileutils
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo

from pylizai.core.ai_setting import AiSetting, AiQueries
from pylizai.model.ai_prompts import AiPrompt
from pylizai.runner.ai_common_runner import AiCommonRunner
from pylizai.runner.ai_runner import AiRunner, AiPoolResult
from pylizai.utils.ai_res_extr import AiResultExtractor


class AiImageScanningType(Enum):
    DOUBLE_QUERY_WITH_TEXT_GEN = "DOUBLE_QUERY_WITH_TEXT_GEN"
    SINGLE_QUERY_ONLY_VISION = "SINGLE_QUERY_ONLY_VISION"


class AiImageScanner:

    def __init__(self, pyliz_dir: PylizDir, scanning_type: AiImageScanningType):
        self.pyliz_dir = pyliz_dir
        self.scanning_type = scanning_type

    def run(
            self,
            path: str,
            ai_image_setting: AiSetting,
            ai_text_setting: AiSetting | None = None
    ) -> AiPayloadMediaInfo:
        logger.debug(f"Running image scanner with {self.scanning_type}")
        if not fileutils.is_image_file(path):
            raise ValueError(f"Path {path} is not an image file.")
        if self.scanning_type == AiImageScanningType.DOUBLE_QUERY_WITH_TEXT_GEN:
            if ai_text_setting is None:
                raise ValueError("ai_text_setting must be provided for AiImageScanningType.DOUBLE_QUERY_WITH_TEXT_GEN")
            obj = self.RunnerWithTextGen(self.pyliz_dir, ai_image_setting, ai_text_setting)
            return obj.run(path)
        elif self.scanning_type == AiImageScanningType.SINGLE_QUERY_ONLY_VISION:
            obj = self.RunnerWithSigleQueryVision(self.pyliz_dir, ai_image_setting)
            return obj.run(path)
        else:
            raise ValueError("Unsupported image_method in AiPixelRunner")

    def run_multiple(
            self,
            paths: list[str],
            list_setting_images: list[AiSetting],
    ) -> list[AiPoolResult]:
        queries = AiQueries(AiPrompt.IMAGE_VISION_JSON.value, list_setting_images, paths)
        runner = AiRunner(self.pyliz_dir)
        result = runner.run_multiple(queries)
        if result.status:
            return result.payload
        else:
            raise ValueError(f"Error running multiple image queries: {result.error}")


    class RunnerWithSigleQueryVision:

        def __init__(
                self,
                pyliz_dir: PylizDir,
                ai_image_setting: AiSetting,
        ):
            self.pyliz_dir = pyliz_dir
            self.ai_image_setting = ai_image_setting

        def run(self, path: str) -> AiPayloadMediaInfo:
            logger.debug(f"RunnerWithSigleQueryVision running image query...")
            ai_image_result = AiCommonRunner.run_query(self.pyliz_dir, self.ai_image_setting, AiPrompt.IMAGE_VISION_JSON.value, path, )
            return ai_image_result


    class RunnerWithTextGen:

        def __init__(
                self,
                pyliz_dir: PylizDir,
                ai_image_setting: AiSetting,
                ai_text_setting: AiSetting | None = None,
        ):
            self.pyliz_dir = pyliz_dir
            self.ai_image_setting = ai_image_setting
            self.ai_text_setting = ai_text_setting


        def run(self, path: str) -> AiPayloadMediaInfo:
            logger.debug(f"RunnerWithTextGen running image query...")
            ai_image_result = AiCommonRunner.run_query(self.pyliz_dir, self.ai_image_setting, AiPrompt.IMAGE_VISION_DETAILED_1.value, path, )
            prompt_text = AiPrompt.TEXT_EXTRACT_FROM_VISION_1.value + ai_image_result
            logger.debug(f"RunnerWithTextGen running text query...")
            ai_text_result = AiCommonRunner.run_query(self.pyliz_dir, self.ai_text_setting, prompt_text)
            return AiResultExtractor.extract(ai_text_result, AiPrompt.TEXT_EXTRACT_FROM_VISION_1)



