import os
from typing import Optional, Tuple, List

import librosa
import numpy as np
import torch
import whisper
from pylizlib.os import fileutils, pathutils
from pylizmedia.model.audioModels import AudioSegment
from pylizmedia.util.vidutils import VideoUtils
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from pylizai.core.ai_setting import AiQuery
from loguru import logger
from pylizai.model.ai_dw_type import AiDownloadType
from pylizai.model.ai_file_type import AiReturnType


class WhisperController:

    def __init__(self, app_model_folder: str, app_temp_folder: str):
        self.whisper_model_folder = os.path.join(app_model_folder, "whisper")
        self.temp_folder = app_temp_folder

    #
    # def __run_from_lib(self, query: AiQuery):
    #     file = query.payload_path
    #     if not os.path.exists(file):
    #         return Operation(status=False, error="File not found during whisper operation.")
    #     if not fileutils.is_video_file(file) and not fileutils.is_audio_file(file):
    #         return Operation(status=False, error="File is not a video or audio file.")
    #     text = Whisper.transcribe(
    #         temp_folder=self.temp_folder,
    #         model_name=query.setting.source.model_name,
    #         video_path=query.payload_path,
    #         whisper_folder_path=self.whisper_model_folder,
    #     )
    #
    # def __run_from_hg(self, query: AiQuery) -> Operation[str]:
    #     return Operation(status=False, error="Hugging face download not supported for whisper operation")

    @staticmethod
    def __transcribe_with_ws_obj(audio_file_path: str, whisper_obj: whisper.Whisper) -> str:
        logger.debug(f"Transcribing audio {audio_file_path}")
        risultato = whisper_obj.transcribe(audio_file_path)
        return risultato["text"]

    def __get_temp_audio_path(self, query: AiQuery,) -> str:
        temp_media_hash = fileutils.gen_file_hash(query.payload_path)
        temp_media_folder = os.path.join(self.temp_folder, temp_media_hash)
        pathutils.check_path(temp_media_folder, True)
        audio_file_name = pathutils.get_filename_no_ext(query.payload_path) + ".wav"
        return os.path.join(temp_media_folder, audio_file_name)

    def __transcribe_file(self, query: AiQuery, whisper_obj: whisper.Whisper) -> str:
        if fileutils.is_video_file(query.payload_path):
            audio_path = self.__get_temp_audio_path(query)
            logger.debug(f"Extracting audio from video {query.payload_path} to {audio_path}")
            VideoUtils.extract_audio(query.payload_path, audio_path, True)
            return self.__transcribe_with_ws_obj(audio_path, whisper_obj)
        elif fileutils.is_audio_file(query.payload_path):
            return self.__transcribe_with_ws_obj(query.payload_path, whisper_obj)
        else:
            raise ValueError("Unsupported file type for whisper transcribe")


    def __run_and_get_str(self, query: AiQuery):
        dw_type = query.setting.download_type
        if dw_type == AiDownloadType.PYTHON_LIB:
            raise NotImplementedError("Python lib not implemented yet in WhisperController")
        elif dw_type == AiDownloadType.HG_FILES:
            raise NotImplementedError("Hugging face not implemented yet in WhisperController")
        elif dw_type == AiDownloadType.WEB_FILES or dw_type == AiDownloadType.DEFAULT:
            model_file_path = os.path.join(self.whisper_model_folder, query.setting.source.get_main_ai_file().file_name)
            whisper_obj = whisper.load_model(model_file_path)
            return self.__transcribe_file(query, whisper_obj)
        else:
            raise ValueError(f"Unsupported download type for whisper: {dw_type}")

    def __run_and_get_segments(self, query: AiQuery) -> List[AudioSegment]:
        if query.setting.download_type == AiDownloadType.HG_REPO:
            transcriber = WhisperSegmentTranscriber(
                whisper_model_path=self.whisper_model_folder,
                model_name=query.setting.source.hg_repo
            )
            result = transcriber.transcribe(query.payload_path)
            return result
        else:
            raise NotImplementedError("Only Hugging Face download supported for audio segment return type")


    def run(self, query: AiQuery):
        logger.debug("Running whisper query with return type: " + query.setting.return_type.value)
        if query.setting.return_type == AiReturnType.STRING:
            return self.__run_and_get_str(query)
        elif query.setting.return_type == AiReturnType.AUDIO_SEGMENTS:
            return self.__run_and_get_segments(query)
        else:
            raise NotImplementedError("Return type not implemented yet in WhisperController")


class WhisperSegmentTranscriber:
    """Audio transcription using OpenAI's Whisper model with direct model interaction"""

    def __init__(
            self,
            whisper_model_path: str,
            model_name: str = "openai/whisper-tiny",
            device: Optional[str] = None,
    ):
        super().__init__()
        if device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"

        logger.info(f"Initializing Whisper transcriber with model {model_name} on {device}")
        self.device = device
        self.whisper_model_path = whisper_model_path

        # Initialize processor and model
        self.processor = WhisperProcessor.from_pretrained(model_name, cache_dir=self.whisper_model_path)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.model.to(device)

        # Disable forced decoder ids
        self.model.config.forced_decoder_ids = None

        # Target sampling rate for Whisper
        self.target_sampling_rate = 16000

    def _extract_audio(self, video_path: str) -> Tuple[np.ndarray, int]:
        """Extract audio from video file and return as numpy array with sampling rate using librosa"""
        try:
            # Load audio using librosa
            raw_audio, original_sampling_rate = librosa.load(
                video_path,
                sr=self.target_sampling_rate,
                mono=True
            )

            # Ensure float32 dtype and normalize
            raw_audio = raw_audio.astype(np.float32)
            if np.abs(raw_audio).max() > 1.0:
                raw_audio = raw_audio / np.abs(raw_audio).max()

            logger.debug(f"Raw audio shape: {raw_audio.shape}, dtype: {raw_audio.dtype}")

            return raw_audio, original_sampling_rate

        except Exception as e:
            logger.error(f"Error extracting audio with librosa: {str(e)}")
            raise


    def _segment_audio(self, audio: np.ndarray, sampling_rate: int, segment_duration: int = 30) -> List[
        Tuple[np.ndarray, float]]:
        """Segment audio into chunks for processing"""
        segment_length = segment_duration * sampling_rate
        segments = []
        start_idx = 0

        while start_idx < len(audio):
            end_idx = min(start_idx + segment_length, len(audio))
            segment = audio[start_idx:end_idx]
            start_time = start_idx / sampling_rate
            segments.append((segment, start_time))
            start_idx = end_idx

        return segments

    def transcribe(self, video_path: str) -> List[AudioSegment]:
        """Transcribe audio from video file using Whisper"""
        logger.info(f"Starting audio transcription for {video_path}")

        # Extract audio
        audio_array, original_sampling_rate = self._extract_audio(video_path)

        # Segment audio into manageable chunks
        audio_segments = self._segment_audio(audio_array, self.target_sampling_rate)

        transcribed_segments = []

        # Process each audio segment
        for segment_audio, start_time in audio_segments:
            # Prepare features
            input_features = self.processor(
                [segment_audio],  # Changed here
                sampling_rate=self.target_sampling_rate,
                return_tensors="pt"
            ).input_features.to(self.device)

            # Generate transcription
            predicted_ids = self.model.generate(input_features)

            # Decode transcription
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]  # Take first element as we process one segment at a time

            # Calculate segment duration
            duration = len(segment_audio) / self.target_sampling_rate

            # Create AudioSegment
            segment = AudioSegment(
                text=transcription.strip(),
                start_time=start_time,
                end_time=start_time + duration,
                confidence=1.0  # Note: Basic Whisper doesn't provide confidence scores
            )

            transcribed_segments.append(segment)

        logger.info(f"Transcription completed: {len(transcribed_segments)} segments")
        return transcribed_segments