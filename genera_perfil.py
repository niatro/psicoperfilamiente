import openai
import anthropic
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargar claves API desde .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')

# Configuración de modelos
models = {
    "openai": [
        "gpt-4o",
        "gpt-4o-mini"
    ],

    "anthropic": [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
}

def select_model():
    print("Selecciona el tipo de modelo:")
    model_types = list(models.keys())
    for i, key in enumerate(model_types, 1):
        print(f"{i}. {key}")
    model_type_index = int(input("Tipo de modelo (número): ").strip()) - 1
    
    if model_type_index < 0 or model_type_index >= len(model_types):
        print("Tipo de modelo inválido. Elige un número válido.")
        return select_model()
    
    model_type = model_types[model_type_index]
    
    print(f"Selecciona un modelo de {model_type}:")
    model_list = models[model_type]
    for j, model in enumerate(model_list, 1):
        print(f"{j}. {model}")
    model_name_index = int(input("Nombre del modelo (número): ").strip()) - 1
    
    if model_name_index < 0 or model_name_index >= len(model_list):
        print("Nombre del modelo inválido. Elige un número válido.")
        return select_model()
    
    model_name = model_list[model_name_index]
    
    return model_type, model_name

def generate_profile_with_gpt4(json_data, model_name):
    try:
        response = openai.ChatCompletion.create(
            model=model_name,  # Usar el modelo seleccionado por el usuario
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

def generate_profile_with_anthropic(json_data, model_name):
    client = Anthropic()
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

def save_profile(profile_text, output_file):
    with open(output_file, 'w') as text_file:
        text_file.write(profile_text)
    print(f"Perfil guardado en {output_file}")

def main():
    carpeta_json = "json_profiles"
    carpeta_perfiles = "perfiles"
    
    if not os.path.exists(carpeta_perfiles):
        os.makedirs(carpeta_perfiles)
    
    model_type, model_name = select_model()
    
    for filename in os.listdir(carpeta_json):
        if filename.endswith(".json"):
            with open(os.path.join(carpeta_json, filename), 'r') as json_file:
                json_data = json.load(json_file)
                
            print(f"Generando perfil para {filename} usando {model_type}:{model_name}...")
            
            if model_type == "openai":
                profile_text = generate_profile_with_gpt4(json_data, model_name)  # Pasar model_name como argumento
            else:
                profile_text = generate_profile_with_anthropic(json_data, model_name)
            
            if profile_text:
                output_file = os.path.join(carpeta_perfiles, f"{os.path.splitext(filename)[0]}.txt")
                save_profile(profile_text, output_file)

if __name__ == "__main__":
    main()