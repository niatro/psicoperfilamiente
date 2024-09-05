import openai
import json
import os
import base64
import time
import random
from dotenv import load_dotenv
from anthropic import Anthropic
from models import MODELS
from prompt_profile import get_archetype_analysis_prompt, get_archetypes, get_photo_analysis_prompt, get_linkedin_profile_prompt

# Cargar variables de entorno
load_dotenv()

def retry_with_exponential_backoff(
    func,
    max_retries=5,
    initial_wait=1,
    exponential_base=2,
    jitter=0.1,
    *args,
    **kwargs
):
    """Retry a function with exponential backoff."""
    retries = 0
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise e
            wait = initial_wait * (exponential_base ** (retries - 1))
            wait *= (1 + jitter * (random.random() * 2 - 1))
            print(f"Reintentando en {wait:.2f} segundos...")
            time.sleep(wait)

class AIProfileGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        openai.api_key = self.openai_api_key
        self.models = MODELS
        self.archetypes = get_archetypes()
        self.json_analysis_folder = "analisis_json"
        self.photo_analysis_folder = "analisis_photo"
        self.ensure_folders_exist()

    def ensure_folders_exist(self):
        for folder in [self.json_analysis_folder, self.photo_analysis_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def read_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error al leer el archivo {file_path}: {str(e)}")
            return None

    def select_model(self):
        print("Seleccione el tipo de modelo:")
        print("1. OpenAI")
        print("2. Anthropic")
        
        while True:
            choice = input("Ingrese el número de su elección (1 o 2): ")
            if choice == "1":
                model_type = "openai"
                break
            elif choice == "2":
                model_type = "anthropic"
                break
            else:
                print("Opción no válida. Por favor, ingrese 1 o 2.")
        
        print(f"\nModelos disponibles para {model_type}:")
        for i, model in enumerate(self.models[model_type], 1):
            print(f"{i}. {model}")
        
        while True:
            choice = input(f"Ingrese el número del modelo de {model_type} que desea usar: ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.models[model_type]):
                    model_name = self.models[model_type][index]
                    break
                else:
                    print("Número de modelo no válido. Por favor, intente de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        
        return model_type, model_name

    def analyze_photo(self, photo_path):
        try:
            with open(photo_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error al leer la foto: {str(e)}")
            return None

    def analyze_json(self, json_path, model_type, model_name):
        with open(json_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        
        prompt = get_linkedin_profile_prompt(json.dumps(json_data, indent=4))
        
        if model_type == "openai":
            return self.generate_with_openai(prompt, model_name)
        else:
            return self.generate_with_anthropic(prompt, model_name)

    def analyze_photo(self, photo_path, model_type, model_name):
        if not os.path.exists(photo_path):
            return "No se encontró la foto de perfil."
        
        try:
            with open(photo_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            prompt = get_photo_analysis_prompt(photo_path)
            return self.generate_vision_content(base64_image, model_type, model_name, prompt)
        except Exception as e:
            print(f"Error al analizar la foto: {str(e)}")
            return "No se pudo analizar la foto debido a un error."

    def generate_vision_content(self, base64_image, model_type, model_name, prompt):
        if model_type == "openai":
            return self.generate_vision_with_openai(base64_image, model_name, prompt)
        else:
            return self.generate_vision_with_anthropic(base64_image, model_name, prompt)

    def generate_profile_with_gpt4(self, json_data, model_name):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente que genera un perfil detallado basado en la información proporcionada."
                    },
                    {
                        "role": "user",
                        "content": f"Genera un perfil detallado basado en la siguiente información:\n\n{json.dumps(json_data, indent=4)}"
                    }
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error al generar el perfil con GPT-4: {str(e)}")
            return None

    def generate_profile_with_anthropic(self, json_data, model_name):
        client = Anthropic(api_key=self.anthropic_api_key)
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=1024,
                system="Eres un asistente que genera perfiles detallados a partir de información JSON.",
                messages=[
                    {"role": "user", "content": f"Genera un perfil detallado basado en la siguiente información:\n\n{json.dumps(json_data, indent=4)}"}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al generar el perfil con Anthropic: {str(e)}")
            return None

    def generate_vision_with_openai(self, base64_image, model_name, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ],
                    }
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error al generar análisis de visión con OpenAI: {str(e)}")
            return None

    def generate_vision_with_anthropic(self, base64_image, model_name, prompt):
        try:
            client = Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al generar análisis de visión con Anthropic: {str(e)}")
            return "No se pudo generar el análisis de la foto debido a un error."

    def generate_content(self, prompt, model_type, model_name):
        if model_type == "openai":
            return self.generate_with_openai(prompt, model_name)
        else:
            return self.generate_with_anthropic(prompt, model_name)

    def generate_with_openai(self, prompt, model_name):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un asistente que genera perfiles detallados."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error al generar contenido con OpenAI: {str(e)}")
            return None

    def generate_with_anthropic(self, prompt, model_name):
        try:
            client = Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system="Eres un asistente que genera perfiles detallados.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al generar contenido con Anthropic: {str(e)}")
            return None

    @staticmethod
    def save_profile(profile_text, output_file):
        if profile_text is None:
            print(f"Advertencia: No se pudo guardar el perfil en {output_file} porque el texto es None.")
            return
        with open(output_file, 'w', encoding='utf-8') as text_file:
            text_file.write(profile_text)
        print(f"Perfil guardado en {output_file}")

    def process_json_files(self, json_folder, photo_folder, web_search_folder, output_folder, model_type, model_name):
        self.ensure_folders_exist()
        
        for filename in os.listdir(json_folder):
            if filename.endswith(".json"):
                json_path = os.path.join(json_folder, filename)
                base_filename = os.path.splitext(filename)[0]
                photo_path = os.path.join(photo_folder, f"{base_filename}_profile.png")
                web_search_path = os.path.join(web_search_folder, f"{base_filename}_web_search.json")
                
                # Analizar JSON
                with open(json_path, 'r', encoding='utf-8') as json_file:
                    json_data = json.load(json_file)
                json_analysis = self.analyze_json(json_path, model_type, model_name)
                json_analysis_path = os.path.join(self.json_analysis_folder, f"{base_filename}_json_analysis.txt")
                self.save_profile(json_analysis, json_analysis_path)
                
                # Analizar foto
                photo_analysis = self.analyze_photo(photo_path, model_type, model_name)
                photo_analysis_path = os.path.join(self.photo_analysis_folder, f"{base_filename}_photo_analysis.txt")
                self.save_profile(photo_analysis, photo_analysis_path)
                
                # Leer resultados de búsqueda web
                with open(web_search_path, 'r', encoding='utf-8') as web_search_file:
                    web_search_data = json.load(web_search_file)
                
                # Generar perfil completo
                full_profile_prompt = get_archetype_analysis_prompt(json_data, photo_analysis, self.archetypes, web_search_data)
                full_profile = self.generate_content(full_profile_prompt, model_type, model_name)
                
                output_file = os.path.join(output_folder, f"{base_filename}_full_profile.txt")
                self.save_profile(full_profile, output_file)

def main():
    generator = AIProfileGenerator()
    model_type, model_name = generator.select_model()  # Solo para pruebas independientes
    generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

    # Asegurarse de que las carpetas existan
    for folder in ["json_profiles", "profile_photos", "web_search_results", "perfiles_completos"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Carpeta '{folder}' creada.")

if __name__ == "__main__":
    main()
