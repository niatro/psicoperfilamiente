# data_processor.py

import os
import json
from scr.models.openai_model import OpenAIModel
from scr.utils.image_utils import load_and_encode_image
from prompt_profile import get_photo_analysis_prompt

class DataProcessor:
    def __init__(self, model_name='gpt-4o'):
        self.model_name = model_name
        self.openai_model = OpenAIModel()

    def process_image(self, image_path, output_folder):
        try:
            # Cargar y codificar la imagen
            base64_string = load_and_encode_image(image_path)
            
            # Obtener el prompt
            prompt_text = get_photo_analysis_prompt("")

            # Construir el mensaje
            message_content = [
                {"type": "text", "text": prompt_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_string}",
                        "detail": "high"
                    }
                }
            ]
            message = {
                "role": "user",
                "content": message_content
            }

            # Construir el payload
            payload = {
                "model": self.model_name,
                "temperature": 0.5,
                "messages": [message],
                "max_tokens": 1000
            }

            # Enviar la solicitud a la API de OpenAI
            response = self.openai_model.send_to_openai(payload)

            # Procesar la respuesta
            if response and 'choices' in response and response['choices']:
                analysis = response['choices'][0]['message']['content']
                # Guardar el análisis en un archivo
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_file = os.path.join(output_folder, f"{base_name}_analysis.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(analysis)
                print(f"Análisis guardado en {output_file}")
            else:
                print(f"No se recibió una respuesta válida para {image_path}")

        except Exception as e:
            print(f"Error al procesar la imagen {image_path}: {str(e)}")

    def process_images_in_folder(self, image_folder, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(image_folder, filename)
                print(f"Procesando imagen: {filename}")
                self.process_image(image_path, output_folder)
