import os
import json
import openai
import anthropic
from dotenv import load_dotenv
from models import MODELS

# Cargar variables de entorno
load_dotenv()

class WebAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        openai.api_key = self.openai_api_key
        self.models = MODELS
        self.input_folder = "web_search_results"
        self.output_folder = "web_analysis_results"
        self.ensure_output_folder_exists()

    def ensure_output_folder_exists(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

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

    def analyze_web_search(self, web_search_data, model_type, model_name):
        prompt = f"""
        Analiza la siguiente información obtenida de una búsqueda web sobre una persona:

        {json.dumps(web_search_data, indent=2, ensure_ascii=False)}

        Por favor, proporciona un análisis detallado que incluya:
        1. Un resumen de la presencia en línea de la persona.
        2. Principales logros o hitos mencionados en las fuentes.
        3. Áreas de experiencia o especialización identificadas.
        4. Cualquier información relevante sobre su carrera o trayectoria profesional.
        5. Posibles intereses o actividades fuera del ámbito profesional.
        6. Una evaluación de la coherencia de la información entre las diferentes fuentes.
        7. Cualquier dato interesante o único que destaque en la búsqueda.

        Por favor, proporciona un análisis objetivo y basado en los hechos presentados en los resultados de la búsqueda.
        """

        if model_type == "openai":
            return self.generate_with_openai(prompt, model_name)
        else:
            return self.generate_with_anthropic(prompt, model_name)

    def generate_with_openai(self, prompt, model_name):
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un asistente que analiza información de búsquedas web sobre personas."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error al generar análisis con OpenAI: {str(e)}")
            return None

    def generate_with_anthropic(self, prompt, model_name):
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system="Eres un asistente que analiza información de búsquedas web sobre personas.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al generar análisis con Anthropic: {str(e)}")
            return None

    def process_web_search_results(self, model_type, model_name):
        for filename in os.listdir(self.input_folder):
            if filename.endswith("_web_search.json"):
                input_path = os.path.join(self.input_folder, filename)
                output_filename = filename.replace("_web_search.json", "_web_analysis.txt")
                output_path = os.path.join(self.output_folder, output_filename)

                print(f"Analizando {filename}...")

                with open(input_path, 'r', encoding='utf-8') as file:
                    web_search_data = json.load(file)

                analysis = self.analyze_web_search(web_search_data, model_type, model_name)

                if analysis:
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.write(analysis)
                    print(f"Análisis guardado en {output_path}")
                else:
                    print(f"No se pudo generar el análisis para {filename}")

def main():
    analyzer = WebAnalyzer()
    model_type, model_name = analyzer.select_model()  # Solo para pruebas independientes
    analyzer.process_web_search_results(model_type, model_name)

if __name__ == "__main__":
    main()
