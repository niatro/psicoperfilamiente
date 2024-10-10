from anthropic import Anthropic
from ..config import ANTHROPIC_API_KEY, ANTHROPIC_SONNET_MODEL
import json

class AnthropicModel:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def create_api_message(self, base64_string, media_type, prompt_text):
        return [
            {
                "role": 'user',
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_string}},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]

    def send_to_anthropic(self, image_path, prompt_text, base64_string=None, media_type=None):
        try:
            if base64_string and media_type:
                message_list = self.create_api_message(base64_string, media_type, prompt_text)
            else:
                message_list = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]

            response = self.client.messages.create(
                model=ANTHROPIC_SONNET_MODEL,
                max_tokens=2048,
                messages=message_list
            )
            if response.content and response.content[0].text:
                return {"content": [{"text": response.content[0].text}]}
            else:
                print("Respuesta de la API vacía o no válida.")
                return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
            return {}
        except Exception as e:
            print(f"Error processing API response: {str(e)}")
            return {}