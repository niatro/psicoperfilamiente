# prueba_vision.py

import os
import sys

# Ajustar el path para importar módulos desde 'scr' y el directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from scr.processors.data_processor import DataProcessor

def main():
    # Asegurarse de que la clave API esté configurada
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY no está configurada.")
        return

    model_name = 'gpt-4o-mini'  # Asegúrate de que este es el nombre correcto del modelo

    data_processor = DataProcessor(model_name=model_name)

    photo_folder = 'profile_photos'

    # Verificar que la carpeta profile_photos existe
    if not os.path.exists(photo_folder):
        print(f"Error: La carpeta '{photo_folder}' no existe.")
        return

    output_folder = 'photo_analysis'

    print("Iniciando el análisis de imágenes...")
    data_processor.process_images_in_folder(photo_folder, output_folder)
    print("Análisis completado.")

if __name__ == "__main__":
    main()
