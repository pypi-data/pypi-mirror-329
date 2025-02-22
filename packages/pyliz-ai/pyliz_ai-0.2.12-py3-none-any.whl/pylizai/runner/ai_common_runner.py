
from pylizlib.config.pylizdir import PylizDir

from pylizai.core.ai_setting import AiQuery, AiSetting
from loguru import logger
from pylizai.runner.ai_runner import AiRunner


class AiCommonRunner:

    @staticmethod
    def run_query(
            pyliz_dir: PylizDir,
            ai_setting: AiSetting,
            prompt: str,
            media_path: str | None = None
    ):
        query = AiQuery(ai_setting, prompt, media_path)
        ai_result = AiRunner(pyliz_dir).run(query)
        if not ai_result.status:
            raise ValueError(ai_result.error)
        logger.trace(f"RunForMedia (pixel) result.status = {ai_result.status}")
        logger.trace(f"RunForMedia (pixel) result.payload = {ai_result.payload}")
        return ai_result.payload
