import openai
import anthropic
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from models import MODELS
from prompt_email import get_email_generation_prompt

# Cargar variables de entorno
load_dotenv()

class AIEmailGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.models = MODELS

    def select_model(self):
        print("Selecciona el tipo de modelo:")
        model_types = list(self.models.keys())
        for i, key in enumerate(model_types, 1):
            print(f"{i}. {key}")
        model_type_index = int(input("Tipo de modelo (número): ").strip()) - 1
        
        if model_type_index < 0 or model_type_index >= len(model_types):
            print("Tipo de modelo inválido. Elige un número válido.")
            return self.select_model()
        
        model_type = model_types[model_type_index]
        
        print(f"Selecciona un modelo de {model_type}:")
        model_list = self.models[model_type]
        for j, model in enumerate(model_list, 1):
            print(f"{j}. {model}")
        model_name_index = int(input("Nombre del modelo (número): ").strip()) - 1
        
        if model_name_index < 0 or model_name_index >= len(model_list):
            print("Nombre del modelo inválido. Elige un número válido.")
            return self.select_model()
        
        model_name = model_list[model_name_index]
        
        return model_type, model_name

    def generate_email_with_openai(self, profile_text, model_name):
        try:
            openai.api_key = self.openai_api_key
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un asistente que genera emails personalizados de manera amigable y persuasiva."},
                    {"role": "user", "content": get_email_generation_prompt(profile_text)}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error al generar el email con OpenAI: {str(e)}")
            return None

    def generate_email_with_anthropic(self, profile_text, model_name):
        try:
            client = Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=1024,
                system="Eres un asistente que genera emails personalizados de manera amigable y persuasiva.",
                messages=[
                    {"role": "user", "content": get_email_generation_prompt(profile_text)}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al generar el email con Anthropic: {str(e)}")
            return None

    @staticmethod
    def save_email(email_text, output_file):
        with open(output_file, 'w', encoding='utf-8') as text_file:
            text_file.write(email_text)
        print(f"Email guardado en {output_file}")

    def process_profiles(self, input_folder, output_folder, model_type, model_name):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for filename in os.listdir(input_folder):
            if filename.endswith("_full_profile.txt"):
                with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as profile_file:
                    profile_text = profile_file.read()
                
                print(f"Generando email para {filename} usando {model_type}:{model_name}...")
                
                if model_type == "openai":
                    email_text = self.generate_email_with_openai(profile_text, model_name)
                else:
                    email_text = self.generate_email_with_anthropic(profile_text, model_name)
                
                if email_text:
                    output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_email.txt")
                    self.save_email(email_text, output_file)

def main():
    generator = AIEmailGenerator()
    model_type, model_name = generator.select_model()  # Solo para pruebas independientes
    generator.process_profiles("perfiles_completos", "mails", model_type, model_name)

if __name__ == "__main__":
    main()
