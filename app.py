import os
import argparse
import getpass
from linkedin_scraper import LinkedInScraper, ScreenshotManager, main as linkedin_scraper_main
from linkedin_profile_image_extractor import LinkedInProfileImageProcessor
from linkedin_profile_analyzer import LinkedInProfileAnalyzer
from web_search_profile import process_profiles as web_search_process
from web_search_profile import process_profiles as web_search_process
from web_analyzer import WebAnalyzer
from ai_profile_generator import AIProfileGenerator
from mails import AIEmailGenerator
from models import MODELS

def select_model():
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
    for i, model in enumerate(MODELS[model_type], 1):
        print(f"{i}. {model}")
    
    while True:
        choice = input(f"Ingrese el número del modelo de {model_type} que desea usar: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(MODELS[model_type]):
                model_name = MODELS[model_type][index]
                break
            else:
                print("Número de modelo no válido. Por favor, intente de nuevo.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    return model_type, model_name

def main():
    model_type, model_name = select_model()

    # LinkedIn Scraper
    print("Iniciando proceso de scraping de LinkedIn...")
    linkedin_scraper_main()

    # LinkedIn Profile Image Extractor
    print("Extrayendo imágenes de perfil...")
    image_processor = LinkedInProfileImageProcessor("captura_1", "profile_photos")
    image_processor.process_images()

    # LinkedIn Profile Analyzer
    print("Analizando perfiles de LinkedIn...")
    analyzer = LinkedInProfileAnalyzer("capturas_linkedin", "json_profiles")
    analyzer.process_images()

    # Web Search Profile
    print("Iniciando búsqueda web...")
    try:
        web_search_process("json_profiles", "web_search_results")
        print("Búsqueda web completada con éxito.")
    except Exception as e:
        print(f"Error durante la búsqueda web: {str(e)}")

    # Web Analyzer
    print("Analizando resultados de búsqueda web...")
    web_analyzer = WebAnalyzer()
    web_analyzer.process_web_search_results(model_type, model_name)

    # AI Profile Generator
    print("Realizando psicoperfilamiento...")
    profile_generator = AIProfileGenerator()
    profile_generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

    # Email Generator
    print("Generando emails personalizados...")
    email_generator = AIEmailGenerator()
    email_generator.process_profiles("perfiles_completos", "mails", model_type, model_name)

    print("Proceso completado.")

if __name__ == "__main__":
    main()
