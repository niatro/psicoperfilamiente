# scr/models/openai_model.py

import requests
import json
import time
import os

# Ajustar el path para importar módulos desde 'scr'
from scr.config import OPENAI_API_KEY  # Asegúrate de que 'config.py' está en 'scr' y contiene 'OPENAI_API_KEY'
from scr.utils.image_utils import load_and_encode_image

class OpenAIModel:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')

    def send_to_openai(self, payload, retries=3, delay=5):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        for attempt in range(retries):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response_json = response.json()
                if response.status_code != 200:
                    print(f"Error en la solicitud: {response_json.get('error', {}).get('message', 'Error desconocido')}")
                    return None
                return response_json
            except requests.exceptions.Timeout:
                print(f"Timeout occurred, retrying... ({attempt + 1}/{retries})")
                time.sleep(delay)
            except Exception as e:
                print(f"Error al procesar la respuesta de OpenAI: {str(e)}")
                print(f"Contenido de la respuesta: {response.content if response else 'No response'}")
                return None

        print("No se pudo obtener una respuesta después de varios intentos.")
        return None