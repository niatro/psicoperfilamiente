import os
import argparse
import getpass
from linkedin_scraper import LinkedInScraper, ScreenshotManager, main as linkedin_scraper_main
from rich import print as rprint
from linkedin_profile_image_extractor import LinkedInProfileImageProcessor
from linkedin_profile_analyzer import LinkedInProfileAnalyzer
from web_search_profile import process_profiles as web_search_process
from web_analyzer import WebAnalyzer
from ai_profile_generator import AIProfileGenerator
from mails import AIEmailGenerator
from models import MODELS

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

console = Console()

def select_model():
    console.print(Panel("Selección de Modelo de IA", style="bold magenta"))
    console.print("[bold cyan]Seleccione el tipo de modelo:[/bold cyan]")
    console.print("1. OpenAI")
    console.print("2. Anthropic")
    
    while True:
        choice = Prompt.ask("Ingrese el número de su elección", choices=["1", "2"])
        if choice == "1":
            model_type = "openai"
            break
        elif choice == "2":
            model_type = "anthropic"
            break
    
    console.print(f"\n[bold cyan]Modelos disponibles para {model_type}:[/bold cyan]")
    for i, model in enumerate(MODELS[model_type], 1):
        console.print(f"{i}. {model}")
    
    while True:
        choice = Prompt.ask(f"Ingrese el número del modelo de {model_type} que desea usar", choices=[str(i) for i in range(1, len(MODELS[model_type])+1)])
        index = int(choice) - 1
        model_name = MODELS[model_type][index]
        break
    
    return model_type, model_name

def get_user_email():
    return input("Por favor, ingrese su correo electrónico: ")

def main():
    rprint(Panel("Bienvenido al Sistema de Análisis de Perfiles", style="bold green"))
    
    model_type, model_name = select_model()
    user_email = get_user_email()

    rprint("[cyan]Scraping de LinkedIn...[/cyan]")
    linkedin_scraper_main()

    # LinkedIn Profile Image Extractor
    rprint("[cyan]Extrayendo imágenes de perfil...[/cyan]")
    image_processor = LinkedInProfileImageProcessor("captura_1", "profile_photos")
    image_processor.process_images()

    # LinkedIn Profile Analyzer
    rprint("[cyan]Analizando perfiles de LinkedIn...[/cyan]")
    analyzer = LinkedInProfileAnalyzer("capturas_linkedin", "json_profiles")
    analyzer.process_images()

    # Web Search Profile
    rprint("[cyan]Iniciando búsqueda web...[/cyan]")
    try:
        web_search_process("json_profiles", "web_search_results")
    except Exception as e:
        rprint(f"[bold red]Error durante la búsqueda web: {str(e)}[/bold red]")

    # Web Analyzer
    rprint("[cyan]Analizando resultados de búsqueda web...[/cyan]")
    web_analyzer = WebAnalyzer()
    web_analyzer.process_web_search_results(model_type, model_name)

    # AI Profile Generator
    rprint("[cyan]Realizando psicoperfilamiento...[/cyan]")
    profile_generator = AIProfileGenerator()
    profile_generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

    # Email Generator
    rprint("[cyan]Generando emails personalizados...[/cyan]")
    email_generator = AIEmailGenerator()
    email_generator.process_profiles("perfiles_completos", "mails", model_type, model_name)

    rprint(Panel("Proceso completado con éxito", style="bold green"))

if __name__ == "__main__":
    main()
