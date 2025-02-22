
import os
import time

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pylizlib.model.operation import Operation
from pylizlib.os import fileutils

from pylizai.core.ai_results import AiResult
from pylizai.core.ai_setting import AiQuery
from loguru import logger
from pylizai.model.ai_file_type import AiReturnType


class GeminiController:

    def __init__(self, key: str):
        genai.configure(api_key=key)

    @staticmethod
    def __upload( path: str, file_name: str):
        logger.debug(f"Uploading file to Google temp cache: {path}")
        uri = sample_file = genai.upload_file(path=path, display_name=file_name)
        logger.info(f"Uploaded file to Google temp cache: {sample_file}")
        return uri

    @staticmethod
    def __verify_loaded_video( uri):
        # Check whether the file is ready to be used.
        while uri.state.name == "PROCESSING":
            logger.debug('.', end='')
            time.sleep(10)
            video_file = genai.get_file(uri.name)

        if uri.state.name == "FAILED":
            raise ValueError(uri.state.name)

    def scan_image(self, query: AiQuery) -> str:
        logger.debug("Scanning image with Gemini...")
        path = query.payload_path
        file_name = os.path.basename(path)
        uri = self.__upload(path, file_name)
        model = genai.GenerativeModel(model_name=query.setting.source.model_name)
        json_in_response: bool = query.setting.return_type == AiReturnType.OBJECT or query.setting.return_type == AiReturnType.STRING_JSON
        has_return_type_obj = query.setting.return_type == AiReturnType.OBJECT and query.setting.return_type_object is not None
        response = model.generate_content(
            [uri, query.prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json" if json_in_response else None,
                response_schema=query.setting.return_type_object if has_return_type_obj else None,
            ),
        )
        genai.delete_file(uri.name)
        logger.info("result =" + response.text)
        return response.text





    def scan_video(self, query: AiQuery) -> Operation[str]:
        logger.debug("Scanning video with Gemini...")
        try:
            path = query.payload_path
            file_name = os.path.basename(path)

            # Upload file
            uri = self.__upload(path, file_name)
            self.__verify_loaded_video(uri)

            # Verifica che il file sia pronto con un timeout
            # max_wait_time = 300  # 300 secondi (5 minuti)
            # wait_interval = 10   # Controlla ogni 10 secondi
            # elapsed_time = 0
            #
            # while elapsed_time < max_wait_time:
            #     video_file = genai.get_file(uri.name)
            #
            #     if video_file.state == "ACTIVE":
            #         # Il file è pronto
            #         break
            #     elif video_file.state == "FAILED":
            #         # Fallimento nell'elaborazione del file
            #         raise ValueError("File processing failed on server.")
            #
            #     logger.debug(f"File processing... Waiting for ACTIVE state. Elapsed time: {elapsed_time}s")
            #     time.sleep(wait_interval)
            #     elapsed_time += wait_interval
            #
            # if elapsed_time >= max_wait_time:
            #     raise TimeoutError(f"File processing timeout after {max_wait_time} seconds.")

            # Usa il modello per generare contenuti
            model_name = query.setting.source.model_name
            model = genai.GenerativeModel(model_name=model_name)
            logger.trace("Generating content with model " + query.setting.source.model_name)
            response = model.generate_content(
                [uri, query.prompt],
                request_options={"timeout": 600},
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                }
            )

            logger.debug("result = " + response.text)

            # Cancella il file dal server dopo l'uso
            genai.delete_file(uri.name)

            return Operation(status=True, payload=response.text)
        except Exception as e:
            logger.error(f"Error scanning video: {str(e)}")
            return Operation(status=False, error=str(e))

    def gen_text(self, model_name: str, prompt: str):
        model = genai.GenerativeModel(model_name=model_name)
        result = model.generate_content(prompt)
        return result.text

    def run(self, query: AiQuery) -> str:
        path = query.payload_path
        if fileutils.is_image_file(path):
            return self.scan_image(query)
        elif fileutils.is_video_file(path):
            return self.scan_video(query)
        elif path is None:
            return self.gen_text(query.setting.source.model_name, query.prompt)
