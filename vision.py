import openai
import pytesseract
import pandas as pd
import os
import json
from PIL import Image
from dotenv import load_dotenv

# Cargar claves API desde .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurar la ruta de instalación de Tesseract (en caso de ser necesario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    try:
        # Usar OCR para extraer texto de la imagen
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error al extraer texto de la imagen {image_path}: {str(e)}")
        return None

def process_text_with_gpt4(text):
    try:
        # Enviar el texto extraído a la API de OpenAI para estructurarlo
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que extrae información de perfiles de LinkedIn."
                },
                {
                    "role": "user",
                    "content": f"""
                    Extrae la siguiente información del perfil de LinkedIn en formato JSON. Asegúrate de que la respuesta esté estructurada como un objeto JSON válido. La información requerida es:
                    - Nombre
                    - Empresa
                    - Cargo
                    - Experiencia (incluyendo años e instituciones)
                    - Educación (incluyendo años e instituciones)
                    - Certificaciones y licencias (incluyendo años e instituciones)
                    - Cantidad de contactos
                    
                    El texto del perfil es el siguiente:
                    \n\n{text}
                    """
                }
            ]
        )
        # Imprimir la respuesta cruda para verificar el contenido
        raw_response = response['choices'][0]['message']['content']
        print("Respuesta cruda de GPT-4:", raw_response)
        
        # Limpiar la respuesta eliminando los delimitadores ```json ... ```
        cleaned_response = raw_response.strip().strip("```").strip("json").strip()
        
        return cleaned_response
    except Exception as e:
        print(f"Error al procesar el texto con GPT-4: {str(e)}")
        return None


def save_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON guardado en {output_file}")

def main():
    carpeta_capturas = "capturas_linkedin"
    carpeta_json = "json_profiles"
    
    if not os.path.exists(carpeta_json):
        os.makedirs(carpeta_json)
    
    for filename in os.listdir(carpeta_capturas):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(carpeta_capturas, filename)
            print(f"Procesando {filename}...")
            
            text = extract_text_from_image(image_path)
            if text:
                result = process_text_with_gpt4(text)
                if result:
                    try:
                        json_data = json.loads(result)
                        output_file = os.path.join(carpeta_json, f"{os.path.splitext(filename)[0]}.json")
                        save_json(json_data, output_file)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar el JSON de {filename}: {str(e)}")

if __name__ == "__main__":
    main()