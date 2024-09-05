import os
import json
from dotenv import load_dotenv
import openai
import pytesseract
from PIL import Image
from prompt_profile import get_linkedin_profile_prompt

# Cargar variables de entorno
load_dotenv()

# Configurar API key de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurar ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class LinkedInProfileAnalyzer:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def extract_text_from_image(self, image_path):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print(f"Error al extraer texto de la imagen {image_path}: {str(e)}")
            return None

    def process_text_with_gpt4(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un asistente que extrae información de perfiles de LinkedIn."},
                    {"role": "user", "content": get_linkedin_profile_prompt(text)}
                ]
            )
            raw_response = response['choices'][0]['message']['content']
            print("Respuesta cruda de GPT-4:", raw_response)
            
            cleaned_response = raw_response.strip().strip("```").strip("json").strip()
            return cleaned_response
        except Exception as e:
            print(f"Error al procesar el texto con GPT-4: {str(e)}")
            return None

    def save_json(self, data, output_file):
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON guardado en {output_file}")

    def process_images(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.input_folder, filename)
                print(f"Procesando {filename}...")
                
                text = self.extract_text_from_image(image_path)
                if text:
                    result = self.process_text_with_gpt4(text)
                    if result:
                        try:
                            json_data = json.loads(result)
                            output_file = os.path.join(self.output_folder, f"{os.path.splitext(filename)[0]}.json")
                            self.save_json(json_data, output_file)
                        except json.JSONDecodeError as e:
                            print(f"Error al decodificar el JSON de {filename}: {str(e)}")

def main():
    input_folder = "capturas_linkedin"
    output_folder = "json_profiles"
    
    analyzer = LinkedInProfileAnalyzer(input_folder, output_folder)
    analyzer.process_images()

if __name__ == "__main__":
    main()
