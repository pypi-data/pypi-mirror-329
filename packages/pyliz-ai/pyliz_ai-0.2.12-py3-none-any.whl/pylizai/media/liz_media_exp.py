from eagleliz.eagleliz import EAGLE_LOCALHOST_URL, Eagleliz
from eagleliz.types import PathItem
from loguru import logger
from pylizlib.os import fileutils
from pylizmedia.liz_media import LizMedia


class LizMediaExporter:

    @staticmethod
    def export_to_json(media: LizMedia):
        fileutils.write_json_to_file(media.path, media.file_name + ".json", media.to_json_only_ai())

    @staticmethod
    def convert_media_to_eagle_item(media: LizMedia) -> PathItem:
        return PathItem(
            name=media.ai_file_name,
            path=media.path,
            annotation=media.ai_description,
            tags=media.ai_tags,
        )

    @staticmethod
    def __attach_image_metadata():
        pass

    @staticmethod
    def __attach_video_metadata():
        pass

    @staticmethod
    def __attach_audio_metadata():
        pass

    @staticmethod
    def attach_metadata(media: LizMedia):
        if media.is_image:
            LizMediaExporter.__attach_image_metadata()
        elif media.is_video:
            LizMediaExporter.__attach_video_metadata()
        elif media.is_audio:
            LizMediaExporter.__attach_audio_metadata()
        else:
            logger.error(f"Media type not supported: {media.type}")

    @staticmethod
    def send_to_eagle(media: list[LizMedia], url: str = EAGLE_LOCALHOST_URL, ):
        eagleliz = Eagleliz(url)
        items = [LizMediaExporter.convert_media_to_eagle_item(m) for m in media]
        resp = eagleliz.add_from_paths(items)
        if resp.is_successful():
            logger.info(f"Files added to eagle.")
        else:
            logger.error(f"Error while adding files to eagle: {resp.get_error()}")
