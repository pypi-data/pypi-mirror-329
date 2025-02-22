import os

from huggingface_hub import hf_hub_download

from pylizlib.os.fileutils import download_file

from loguru import logger
from pylizai.model.ai_file_type import AiFile, AiHgFile


class AiDownloader:

    @staticmethod
    def download_ai_file(file: AiFile, dest_folder: str):
        logger.debug(f"Downloading file {file.file_name} from {file.url} to {dest_folder}")
        file_path = os.path.join(dest_folder, file.file_name)
        download_file(file.url, file_path, on_progress=lambda percent: logger.trace(f"Download progress: {percent}%"))

    @staticmethod
    def download_hg_file(file: AiHgFile, dest_folder: str):
        logger.debug(f"Downloading file {file.file_name} from HG repo {file.repository} inside {dest_folder}")
        hf_hub_download(repo_id=file.repository, filename=file.file_name, local_dir=dest_folder)