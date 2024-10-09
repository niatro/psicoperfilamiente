import openai
import json
import os
import time
import random
import re
from dotenv import load_dotenv
from anthropic import Anthropic
from models import MODELS
from prompt_profile import (
    get_archetype_analysis_prompt,
    get_archetypes,
    get_photo_analysis_prompt,
    get_linkedin_profile_prompt
)
import base64
import requests

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
    """Reintenta una función con retroceso exponencial."""
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
        self.ensure_folders_exist()

    def ensure_folders_exist(self):
        pass  # Ya no necesitamos crear carpetas adicionales

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

    def analyze_photo(self, photo_path, model_type, model_name):
        if not os.path.exists(photo_path):
            return "No se encontró la foto de perfil."

        try:
            # Codificar la imagen en base64
            with open(photo_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Crear el Data URL de la imagen
            data_url = f"data:image/jpeg;base64,{base64_image}"

            # Crear el payload para la solicitud
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Por favor, proporciona una descripción detallada de la siguiente imagen y realiza un análisis psicológico objetivo basado en ella."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_url
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }

            # Realizar la solicitud a la API de OpenAI
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # Procesar la respuesta
            if response.status_code == 200:
                response_data = response.json()
                photo_analysis = response_data['choices'][0]['message']['content']
                return photo_analysis
            else:
                print(f"Error en la solicitud a la API de OpenAI: {response.status_code} - {response.text}")
                return "No se pudo analizar la foto debido a un error en la solicitud a la API."
        except Exception as e:
            print(f"Error al analizar la foto: {str(e)}")
            return "No se pudo analizar la foto debido a un error."
        
    def analyze_json(self, json_data, model_type, model_name):
        prompt = get_linkedin_profile_prompt(json.dumps(json_data, indent=4))
        
        if model_type == "openai":
            return self.generate_with_openai(prompt, model_name)
        else:
            return self.generate_with_anthropic(prompt, model_name)

    def generate_content(self, prompt, model_type, model_name):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if model_type == "openai":
                    return self.generate_with_openai(prompt, model_name)
                else:
                    return self.generate_with_anthropic(prompt, model_name)
            except Exception as e:
                print(f"Intento {attempt + 1} fallido: {str(e)}")
                if attempt == max_retries - 1:
                    print("Se alcanzó el número máximo de intentos. Retornando None.")
                    return None
                time.sleep(2 ** attempt)  # Espera exponencial entre intentos

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
            raise

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
            raise

    @staticmethod
    def save_profile(profile_text, output_file):
        if profile_text is None:
            error_message = "No se pudo generar el perfil. El texto del perfil es None."
            print(f"Advertencia: {error_message}")
            with open(output_file, 'w', encoding='utf-8') as text_file:
                text_file.write(error_message)
            print(f"Mensaje de error guardado en {output_file}")
        else:
            with open(output_file, 'w', encoding='utf-8') as text_file:
                text_file.write(profile_text)
            print(f"Perfil guardado en {output_file}")

    def load_search_results(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                search_data = f.read()
            return search_data
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo de resultados de búsqueda: {file_path}")
            return ""
        except Exception as e:
            print(f"Error al cargar los resultados de búsqueda de {file_path}: {str(e)}")
            return ""

    def format_search_results(self, search_data):
        try:
            data = json.loads(search_data)
            results = data.get('results', [])
            formatted_results = ""
            for result in results:
                title = result.get('title', 'Sin título')
                content = result.get('content', 'Sin contenido disponible')
                url = result.get('url', 'URL no disponible')
                formatted_results += f"**{title}**\n{content}\n[Leer más]({url})\n\n"
            return formatted_results.strip()
        except json.JSONDecodeError:
            return "No se pudieron procesar los resultados de búsqueda."

    def sanitize_filename(self, filename):
        # Reemplaza caracteres no permitidos por guiones bajos
        sanitized = re.sub(r'[<>:"/\\|?*.,]', '_', filename)
        sanitized = sanitized.replace(' ', '_')
        sanitized = sanitized.strip('_')
        return sanitized

    def process_json_files(self, json_folder, photo_folder, web_search_folder, output_folder, model_type, model_name):
        # Ya no necesitamos crear carpetas adicionales
        for filename in os.listdir(json_folder):
            if filename.endswith(".json"):
                json_path = os.path.join(json_folder, filename)
                base_filename = os.path.splitext(filename)[0]
                photo_path = os.path.join(photo_folder, f"{base_filename}_profile.png")
                
                try:
                    # Cargar datos JSON
                    with open(json_path, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)
                    
                    # Obtener análisis del JSON (opcional, ya que usamos json_data directamente)
                    # json_analysis = self.analyze_json(json_data, model_type, model_name)
                    
                    # Analizar foto y obtener el análisis
                    photo_analysis = self.analyze_photo(photo_path, model_type, model_name)
                    
                    # Cargar y formatear resultados de búsqueda web
                    name = json_data.get('Nombre', '').strip()
                    company = json_data.get('Empresa', '').strip()
                    
                    # Si no se encuentra 'Nombre' o 'Empresa', intentar con otras claves
                    if not name:
                        for key in json_data.keys():
                            if 'nombre' in key.lower():
                                name = json_data[key].strip()
                                break
                    if not company:
                        for key in json_data.keys():
                            if 'empresa' in key.lower():
                                company = json_data[key].strip()
                                break
                    
                    # Imprimir los valores extraídos
                    print(f"Procesando archivo: {filename}")
                    print(f"Nombre extraído: '{name}'")
                    print(f"Empresa extraída: '{company}'")
                    
                    # Si aún no se encuentran 'Nombre' o 'Empresa', emitir advertencia y continuar
                    if not name or not company:
                        print(f"Advertencia: No se pudo encontrar nombre o empresa para {filename}. Contenido del archivo: {json.dumps(json_data, indent=2)}")
                        continue
                    
                    # Sanear los nombres para crear nombres de archivo válidos
                    name_filename = self.sanitize_filename(name)
                    company_filename = self.sanitize_filename(company)
                    
                    person_search_file = os.path.join(web_search_folder, f'{name_filename}_person_search.json')
                    company_search_file = os.path.join(web_search_folder, f'{company_filename}_company_search.json')
                    
                    # Imprimir los nombres de archivo construidos
                    print(f"Archivo de búsqueda de persona: {person_search_file}")
                    print(f"Archivo de búsqueda de empresa: {company_search_file}")
                    
                    # Listar archivos en la carpeta web_search_results
                    print("Archivos en la carpeta web_search_results:")
                    for file in os.listdir(web_search_folder):
                        print(f"- {file}")
                    
                    person_search_results_raw = self.load_search_results(person_search_file)
                    company_search_results_raw = self.load_search_results(company_search_file)
                    
                    formatted_person_search_results = self.format_search_results(person_search_results_raw)
                    formatted_company_search_results = self.format_search_results(company_search_results_raw)
                    
                    # Generar perfil completo
                    full_profile_prompt = get_archetype_analysis_prompt(
                        json_data, photo_analysis, self.archetypes,
                        formatted_person_search_results, formatted_company_search_results,
                        person_search_file, company_search_file
                    )
                    full_profile = self.generate_content(full_profile_prompt, model_type, model_name)
                    
                    if full_profile is None:
                        raise Exception("No se pudo generar el perfil completo")
                    
                    output_file = os.path.join(output_folder, f"{base_filename}_full_profile.txt")
                    self.save_profile(full_profile, output_file)
                    print(f"Perfil completo generado y guardado para {base_filename}")
                except Exception as e:
                    print(f"Error al procesar el archivo {filename}: {str(e)}")
                    error_message = f"No se pudo generar el perfil completo debido a un error: {str(e)}"
                    error_file = os.path.join(output_folder, f"{base_filename}_error.txt")
                    with open(error_file, 'w', encoding='utf-8') as f:
                        f.write(error_message)
                    print(f"Se ha guardado un archivo de error para {base_filename}")

    def main():
        generator = AIProfileGenerator()
        model_type, model_name = generator.select_model()
        generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

        # Asegurarse de que las carpetas existan
        for folder in ["json_profiles", "profile_photos", "web_search_results", "perfiles_completos"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Carpeta '{folder}' creada.")

    if __name__ == "__main__":
        main()
