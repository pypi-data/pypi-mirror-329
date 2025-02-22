from enum import Enum

from loguru import logger
from sympy.polys.polyconfig import query

from pylizai.core.ai_setting import AiQuery
from pylizai.model.ai_file_type import AiReturnType

prompt_llava_json = """
Analyze the image thoroughly and provide a detailed description of every visible element. Return a json including the following information:
- "description": a detailed description of the image (minimum 15-20 words), considering colors, objects, actions, and any other relevant details.
- "tags": a list of tags that describe the image. Include specific objects, actions, locations, and any discernible themes. (minimum 5 maximum 10 tags)
- "text": a list of all the text found in the image (if any).
- "filename": phrase that summarizes the image content (maximum 30 characters).
"""

prompt_llava_json_2 = """
Analyze the image thoroughly and respond **ONLY** with a valid JSON object. Do not include any additional text, explanations, or formatting outside of the JSON object. Ensure the JSON object adheres to the following rules:
1. Use proper JSON syntax with no escaped characters like \\n or \\\".
2. Ensure keys and string values are enclosed in double quotes ("").
3. Ensure no trailing commas and use a valid JSON format.
4. Do not include null values unless explicitly required.
5. Return the JSON object directly without wrapping it in a string.

The JSON structure should follow this format:

{
  "description": "A detailed description of the image (minimum 15-20 words), considering colors, objects, actions, and any other relevant details.",
  "tags": ["tag1", "tag2", ..., "tagN"],  // A list of 5-10 tags that describe the image, including objects, actions, locations, and themes.
  "text": ["found text 1", "found text 2", ..., "found text N"],  // All text found in the image, or an empty list if none.
  "filename": "A phrase summarizing the image content (maximum 30 characters)."
}

Respond strictly with this JSON format.
"""

extract_info_from_image = """
Analyze the following text that contains a description of image. Return a json including the following information:
- "tags": a list of tags that describe the image. Include specific objects, actions, locations, and any discernible themes. (minimum 5 maximum 10 tags)
- "text": a list of all the text found in the image (if specified).
- "filename": phrase that summarizes the image content (maximum 30 characters).
"""

extract_info_from_video_recap ="""
Analyze the following text that contains a description of all frames inside a video and the audio transcript. Return a json including the following information:
- "tags": a list of tags that describe the video. Include specific objects, actions, locations, and any discernible themes. (minimum 5 maximum 10 tags)
- "text": a list of all the text found in the image (if specified).
- "filename": phrase that summarizes the video content (maximum 30 characters).
- "description": a detailed description of the video (minimum 15-20 words), considering colors, objects, actions, and any other relevant details.
"""

prompt_llava_detailed_STEP1 = """
Analyze the image thoroughly and provide a detailed description of every visible element. 
If there are people, try to recognize them. If there are objects, try to identify them.
If the are texts, try to read them.
"""

prompt_video_easy_1 = """ "Describe in details the content of the video. Include the main actions, objects, and any other relevant details."""


class AiPrompt(Enum):

    IMAGE_VISION_DETAILED_1 = prompt_llava_detailed_STEP1
    IMAGE_VISION_JSON = prompt_llava_json
    TEXT_EXTRACT_FROM_VISION_1 = extract_info_from_image
    TEXT_EXTRACT_FROM_MULTIPLE_VISION = extract_info_from_video_recap
    VIDEO_EASY_1 = prompt_video_easy_1



def attach_prompt_schema_if_required(query: AiQuery):
    if query.setting.return_type == AiReturnType.OBJECT:
        if query.setting.return_type_object is None:
            raise Exception("During editing of current prompt return type object is not set in query setting.")
        logger.trace("Adding JSON schema to prompt...")
        schema = query.setting.return_type_object.model_json_schema()
        new_prompt = query.prompt + "\n\n" + "Use this JSON schema:" + "\n" + f"ReturnObject = {schema["properties"]}" + "\n" + "Return: ReturnObject"
        query.prompt = new_prompt