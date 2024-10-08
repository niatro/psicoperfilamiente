import os
import json
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from linkedin_scraper import main as linkedin_scraper_main
from linkedin_profile_image_extractor import LinkedInProfileImageProcessor
from linkedin_profile_analyzer import LinkedInProfileAnalyzer
from web_search_tavily import main as tavily_search
from ai_profile_generator import AIProfileGenerator
from mails import AIEmailGenerator
from models import MODELS

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

    rprint("[cyan]Extrayendo imágenes de perfil...[/cyan]")
    image_processor = LinkedInProfileImageProcessor("captura_1", "profile_photos")
    image_processor.process_images()

    rprint("[cyan]Analizando perfiles de LinkedIn...[/cyan]")
    analyzer = LinkedInProfileAnalyzer("capturas_linkedin", "json_profiles")
    analyzer.process_images()

    rprint("[cyan]Iniciando búsqueda web con Tavily...[/cyan]")
    
    # Asegurarse de que la carpeta 'web_search_results' exista
    if not os.path.exists("web_search_results"):
        os.makedirs("web_search_results")
        rprint("[green]Carpeta 'web_search_results' creada.[/green]")
    
    try:
        for filename in os.listdir("json_profiles"):
            if filename.endswith(".json"):
                with open(os.path.join("json_profiles", filename), 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                name = profile_data.get('Nombre', '')
                company = profile_data.get('Empresa', '')
                # Intenta buscar en otras claves posibles si no se encuentran 'Nombre' o 'Empresa'
                if not name:
                    for key in profile_data.keys():
                        if 'nombre' in key.lower():
                            name = profile_data[key]
                            break
                if not company:
                    for key in profile_data.keys():
                        if 'empresa' in key.lower():
                            company = profile_data[key]
                            break
                
                if not name or not company:
                    rprint(f"[bold yellow]Advertencia: No se pudo encontrar nombre o empresa para {filename}. Contenido del archivo: {json.dumps(profile_data, indent=2)}[/bold yellow]")
                    continue

                rprint(f"[cyan]Buscando información para: {name} de {company}[/cyan]")
                tavily_search(name, company)
                
                # Verificar si se crearon los archivos JSON
                person_file = os.path.join('web_search_results', f'{name.replace(" ", "_")}_person_search.json')
                company_file = os.path.join('web_search_results', f'{company.replace(" ", "_")}_company_search.json')
                
                if os.path.exists(person_file) and os.path.exists(company_file):
                    rprint(f"[green]Archivos JSON creados para {name} y {company}[/green]")
                else:
                    rprint(f"[bold yellow]Advertencia: No se encontraron archivos JSON para {name} o {company}[/bold yellow]")
    except Exception as e:
        rprint(f"[bold red]Error durante la búsqueda web con Tavily: {str(e)}[/bold red]")

    rprint("[cyan]Realizando psicoperfilamiento...[/cyan]")
    profile_generator = AIProfileGenerator()
    profile_generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

    rprint("[cyan]Generando emails personalizados...[/cyan]")
    email_generator = AIEmailGenerator()
    email_generator.process_profiles("perfiles_completos", "mails", model_type, model_name)

    rprint(Panel("Proceso completado con éxito", style="bold green"))

if __name__ == "__main__":
    main()
