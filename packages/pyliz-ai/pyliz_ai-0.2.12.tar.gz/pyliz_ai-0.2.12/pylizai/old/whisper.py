

# class Whisper:
#
#
#     @staticmethod
#     def get_model_obj_from_lib(model_name: str, whisper_folder_path: str):
#
#         # Imposta la directory personalizzata per i modelli
#         logger.debug(f"Setting WHISPER_CACHE_DIR to {whisper_folder_path}")
#         os.environ["WHISPER_CACHE_DIR"] = whisper_folder_path
#         # Carica il modello, che verrà scaricato se non già presente
#         logger.debug(f"Loading Whisper model {model_name}")
#         modello = whisper.load_model(model_name, download_root=whisper_folder_path)
#         return modello
#
#
#     @staticmethod
#     def transcribe(
#             temp_folder: str,
#             model_name: str,
#             video_path: str,
#             whisper_folder_path: str,
#     ) -> str:
#         audio_id = datautils.gen_random_string(10)
#         audio_path = os.path.join(temp_folder, f"{audio_id}.wav")
#         logger.debug(f"Extracting audio from video {video_path} to {audio_path}")
#         VideoUtils.extract_audio(video_path, audio_path)
#
#         # Scarica il modello di Whisper
#         logger.debug(f"Loading Whisper model {model_name}")
#         modello = Whisper.get_model_obj_from_lib(model_name, whisper_folder_path)
#
#         # Trascrive l'audio e restituisce il testo
#         logger.debug(f"Transcribing audio {audio_path}")
#         risultato = modello.transcribe(audio_path)
#         return risultato["text"]


