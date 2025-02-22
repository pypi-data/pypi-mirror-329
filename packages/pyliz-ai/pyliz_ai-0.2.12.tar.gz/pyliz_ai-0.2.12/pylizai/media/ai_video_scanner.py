import base64
import io
import os
from enum import Enum
from typing import List

import numpy as np
from PIL import Image
from pylizlib.os import fileutils, osutils, pathutils
from pylizmedia.model.videoModels import Frame
from pylizmedia.video.FrameSelectors import FrameSelector, DynamicFrameSelector

from loguru import logger
from pylizlib.config.pylizdir import PylizDir, PylizDirFoldersTemplate
from pylizmedia.liz_media import LizMedia
from pylizmedia.model.ai_payload_info import AiPayloadMediaInfo
from pylizmedia.util.vidutils import VideoUtils

from pylizai.core.ai_setting import AiSetting, AiSettingComboList
from pylizai.media.ai_image_scanner import AiImageScanningType, AiImageScanner
from pylizai.model.ai_file_type import AiReturnType
from pylizai.model.ai_prompts import AiPrompt
from pylizai.runner.ai_common_runner import AiCommonRunner
from pylizai.utils.ai_res_extr import AiResultExtractor


class AiVideoScanningType(Enum):
    OSO = "OpenSceneOllama (Windows only)"
    PYLIZ = "Pyliz Easy"
    DIRECT_API = "Direct API call"


class AiVideoScanner:

    def __init__(self, pyliz_dir, scanning_type: AiVideoScanningType):
        self.ai_oso_text: AiSetting | None = None
        self.ai_video_api: AiSetting | None = None
        self.ai_combo_list: AiSettingComboList | None = None
        self.pyliz_dir = pyliz_dir
        self.scanning_type = scanning_type

    def set_settings(
            self,
            ai_combo_list: AiSettingComboList | None = None,
            ai_video_api: AiSetting | None = None,
            ai_oso_text: AiSetting | None = None,
    ):
        self.ai_combo_list = ai_combo_list
        self.ai_video_api = ai_video_api
        self.ai_oso_text = ai_oso_text
        self.ai_combo_list.override_img_ret_type(AiReturnType.OBJECT, AiPayloadMediaInfo)
        self.ai_combo_list.override_text_ret_type(AiReturnType.STRING_JSON)

    def check(self):
        logger.debug(f"Checking Video Scanner requirements...")
        if self.scanning_type == AiVideoScanningType.DIRECT_API:
            if self.ai_video_api is None:
                raise ValueError("Direct API call requires ai_video_api")
        elif self.scanning_type == AiVideoScanningType.OSO:
            if self.ai_oso_text is None:
                raise ValueError("OpenSceneOllama requires ai_oso_text ai setting variable set!")
            if osutils.is_os_unix():
                raise ValueError("OpenSceneOllama is only available on Windows")
        elif self.scanning_type == AiVideoScanningType.PYLIZ:
            if self.ai_combo_list is None:
                raise ValueError("This video runner requires AiComboList object set!")


    def run(self, path: str) -> AiPayloadMediaInfo:
        logger.debug(f"Running video scanner with {self.scanning_type}")
        if not fileutils.is_video_file(path):
            raise ValueError(f"Path {path} is not a video file.")
        if self.scanning_type == AiVideoScanningType.OSO:
            pass
        elif self.scanning_type == AiVideoScanningType.PYLIZ:
            scanner = AiVideoScanner.RunnerPyliz(self.pyliz_dir, self.ai_combo_list, DynamicFrameSelector())
            return scanner.run(path)
        elif self.scanning_type == AiVideoScanningType.DIRECT_API:
            self.ai_video_api.set_return_type(AiReturnType.OBJECT, AiPayloadMediaInfo)
            return AiVideoScanner.RunnerDirectApi.run(self.pyliz_dir, self.ai_video_api, path)
        else:
            raise ValueError("Unsupported video_scanning_type in AiVideoScanner")


    class RunnerDirectApi:

        @staticmethod
        def run(pyliz_dir: PylizDir, ai_video: AiSetting, path: str) -> AiPayloadMediaInfo:
            return AiCommonRunner.run_query(pyliz_dir, ai_video, AiPrompt.VIDEO_EASY_1.value, path)


    class RunnerPyliz:

        def __init__(self, pyliz_dir: PylizDir, ai_combo_list: AiSettingComboList, frame_selector: FrameSelector):
            self.pyliz_dir = pyliz_dir
            self.ai = ai_combo_list
            self.scan_audio = self.ai.list_audio is not None and len(self.ai.list_audio) > 0
            self.temp_media_dir = None
            self.frame_selector = frame_selector
            if self.ai.list_image is None or len(self.ai.list_image) == 0:
                raise ValueError("No image settings found passed to VideoScanner.")
            if self.ai.list_text is None or len(self.ai.list_text) == 0:
                raise ValueError("No text settings found passed to VideoScanner.")

        def __setup_temp_media_path(self, video_path):
            temp_dir = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.TEMP)
            pathutils.check_path(temp_dir, create_if_not=True)
            file_hash = fileutils.gen_file_hash(video_path)
            temp_media_dir = os.path.join(temp_dir, file_hash)
            pathutils.check_path(temp_media_dir, create_if_not=True)
            self.temp_media_dir = temp_media_dir

        def __frame_to_base64(self, frame: np.ndarray) -> str:
            """Convert a frame to base64 string"""
            image = Image.fromarray(frame)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()

        def __extract_frames_objs(self, path):
            logger.debug("Extracting frames...")
            frames_folder = os.path.join(self.temp_media_dir, "frames")
            frames: list[Frame] = VideoUtils.extract_frame_advanced(path, frames_folder, DynamicFrameSelector())
            return frames

        def __extract_audio(self, path):
            if not self.scan_audio:
                return ""
            logger.debug("Extracting audio...")
            return AiCommonRunner.run_query(self.pyliz_dir, self.ai.list_audio[0], "", path)

        def __gen_recap_from_frames(self, frames: List[LizMedia]) -> str:
            logger.debug(f"Generating recap from frames...")
            recap = ""
            for index, frame in enumerate(frames):
                recap += f"Frame {index}: {frame.get_desc_plus_text()}\n"
            return recap

        def __gen_video_recap(self, audio: str, frames_recap: str) -> str:
            logger.debug(f"Generating video recap...")
            return f"Audio: {audio}\nFrames:\n{frames_recap}"


        def __analyze_frames_single_setting(self, frames, frames_paths_list) -> list[LizMedia]:
            scanner = AiImageScanner(self.pyliz_dir, AiImageScanningType.SINGLE_QUERY_ONLY_VISION)
            liz_frames = []
            frames_count = len(frames)
            for index, frame_path in enumerate(frames_paths_list):
                logger.debug(f"Scanning frame {index} of {frames_count-1}: {frame_path}")
                frame = LizMedia(frame_path)
                frame_result = scanner.run(frame_path, self.ai.list_image[0])
                frame.apply_ai_info(frame_result)
                liz_frames.append(frame)
            return liz_frames

        def __analyze_frames_multi_setting(self, frames_paths_list: list[str]) -> list[LizMedia]:
            scanner = AiImageScanner(self.pyliz_dir, AiImageScanningType.SINGLE_QUERY_ONLY_VISION)
            pool_results = scanner.run_multiple(frames_paths_list, self.ai.list_image)
            liz_frames = []
            for current_frame in pool_results:
                frame = LizMedia(current_frame.path_used)
                frame.apply_ai_info(current_frame.result_obj)
                liz_frames.append(frame)
            return liz_frames

        def __analyze_frames(self, frames) -> list[LizMedia]:
            frames_folder = os.path.join(self.temp_media_dir, "frames")
            frames_path_list = []
            for index, file in enumerate(os.listdir(frames_folder)):
                current_frame_path = os.path.join(frames_folder, file)
                frames_path_list.append(current_frame_path)
            if len(self.ai.list_image) == 1:
                return self.__analyze_frames_single_setting(frames, frames_path_list)
            elif len(self.ai.list_image) > 1:
                return self.__analyze_frames_multi_setting(frames_path_list)
            else:
                raise ValueError("No image settings found in AiSettingComboList")

        def run(self, path: str) -> AiPayloadMediaInfo:
            # creo path temporaneo per il video
            self.__setup_temp_media_path(path)
            # estraggo audio se necessario
            audio = self.__extract_audio(path)
            # estraggo i frame
            frames = self.__extract_frames_objs(path)
            # analizzo i frame
            liz_frames = self.__analyze_frames(frames)
            # genero recap
            frames_recap = self.__gen_recap_from_frames(liz_frames)
            video_recap = self.__gen_video_recap(audio, frames_recap)
            # ottengo risultato
            prompt_type = AiPrompt.TEXT_EXTRACT_FROM_MULTIPLE_VISION
            prompt_text = prompt_type.value + "\n\n" + video_recap
            result = AiCommonRunner.run_query(self.pyliz_dir, self.ai.list_text[0], prompt_text)
            return AiResultExtractor.extract(result, AiPrompt.TEXT_EXTRACT_FROM_MULTIPLE_VISION)





    # class RunnerPylizEasySt:
    #
    #     def __init__(self, pyliz_dir: PylizDir, ai_combo: AiSettingCombo):
    #         self.pyliz_dir = pyliz_dir
    #         self.settings = ai_combo
    #         self.scan_audio = self.settings.ai_audio is not None
    #
    #     def __get_transcribed_audio(self, path: str) -> str:
    #         logger.debug(f"Getting audio transcription...")
    #         return AiCommonRunner.run_query(self.pyliz_dir, self.settings.ai_audio, "", path)
    #
    #
    #     def __get_frames_temp_path(self, path) -> str:
    #         temp_path = self.pyliz_dir.get_folder_template_path(PylizDirFoldersTemplate.TEMP)
    #         if temp_path is None:
    #             raise ValueError("Unable to create temp folder")
    #         check_path(temp_path, create_if_not=True)
    #         file_hash = fileutils.gen_file_hash(path)
    #         scanning_path = os.path.join(temp_path, f"{file_hash}", "frames")
    #         check_path(scanning_path, create_if_not=True)
    #         return scanning_path
    #
    #     def __get_liz_frames(self, path: str) -> List[LizMedia]:
    #         liz_frames = []
    #         logger.debug(f"Getting liz frames...")
    #         frame_path = self.__get_frames_temp_path(path)
    #         logger.trace(f"Extracting frames to {frame_path}...")
    #         VideoUtils.extract_frames(path, frame_path, 90)
    #         frames_count = sum(len(files) for _, _, files in os.walk(frame_path))
    #         scanner = AiImageScanner(self.pyliz_dir, AiImageScanningType.SINGLE_QUERY_ONLY_VISION)
    #         for index, file in enumerate(os.listdir(frame_path)):
    #             logger.debug(f"Scanning frame {index} of {frames_count-1}: {file}")
    #             current_frame_path = os.path.join(frame_path, file)
    #             frame_result = scanner.run(current_frame_path, self.settings.ai_image, self.settings.ai_text)
    #             frame = LizMedia(current_frame_path)
    #             frame.apply_ai_info(frame_result)
    #             liz_frames.append(frame)
    #         return liz_frames
    #
    #
    #
    #
    #     def __gen_video_recap(self, audio: str, frames_recap: str) -> str:
    #         logger.debug(f"Generating video recap...")
    #         return f"Audio: {audio}\nFrames:\n{frames_recap}"
    #
    #     def run(self, path: str) -> AiPayloadMediaInfo:
    #         frames = self.__get_liz_frames(path)
    #         frames_recap = self.__gen_recap_from_frames(frames)
    #         if self.scan_audio:
    #             audio = self.__get_transcribed_audio(path)
    #         else:
    #             audio = ""
    #         video_recap = self.__gen_video_recap(audio, frames_recap)
    #         prompt_type = AiPrompt.TEXT_EXTRACT_FROM_MULTIPLE_VISION
    #         prompt_text = prompt_type.value + "\n\n" + video_recap
    #         result = AiCommonRunner.run_query(self.pyliz_dir, self.settings.ai_text, prompt_text)
    #         return AiResultExtractor.extract(result, AiPrompt.TEXT_EXTRACT_FROM_MULTIPLE_VISION)
    #

