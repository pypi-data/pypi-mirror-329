import base64



class AiMessageGenerator:

    @staticmethod
    def has_vision_file(query) -> bool:
        from pylizai.core.ai_setting import AiQuery, AiQueryType
        return query.query_type == AiQueryType.IMAGE

    @staticmethod
    def gen_message_mistral(query):
        if AiMessageGenerator.has_vision_file(query):
            with open(query.payload_path, "rb") as image_file:
                base_image = base64.b64encode(image_file.read()).decode('utf-8')
            return [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query.prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base_image}"
                        }
                    ]
                }
            ]
        else:
            return [
                {
                    "role": "user",
                    "content": query.prompt,
                },
            ]

    @staticmethod
    def gen_message_lmstudio(query):
        prompt = query.prompt
        if AiMessageGenerator.has_vision_file(query):
            with open(query.payload_path, "rb") as image_file:
                img_ext = query.payload_path.split('.')[-1]
                base_image = base64.b64encode(image_file.read()).decode('utf-8')
            return [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{img_ext};base64,{base_image}",
                            }
                        }
                    ]
                }
            ]
        else:
            return [
                {
                    "role": "user",
                    "content": query.prompt,
                },
            ]