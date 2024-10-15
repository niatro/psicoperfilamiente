import os
import json
import re
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from linkedin_scraper import main as linkedin_scraper_main
from linkedin_profile_image_extractor import LinkedInProfileImageProcessor
from linkedin_profile_analyzer import LinkedInProfileAnalyzer
from web_search_tavily import main as tavily_search
from ai_profile_generator import AIProfileGenerator
from models import MODELS

console = Console()

def select_model():
    rprint("[bold cyan]Seleccione el tipo de modelo:[/bold cyan]")
    rprint("1. OpenAI")
    rprint("2. Anthropic")
    
    while True:
        choice = Prompt.ask("Ingrese el número de su elección (1 o 2)")
        if choice == "1":
            model_type = "openai"
            break
        elif choice == "2":
            model_type = "anthropic"
            break
        else:
            rprint("[bold red]Opción no válida. Por favor, ingrese 1 o 2.[/bold red]")
    
    rprint(f"\n[bold cyan]Modelos disponibles para {model_type}:[/bold cyan]")
    for i, model in enumerate(MODELS[model_type], 1):
        rprint(f"{i}. {model}")
    
    while True:
        choice = Prompt.ask(f"Ingrese el número del modelo de {model_type} que desea usar")
        try:
            index = int(choice) - 1
            if 0 <= index < len(MODELS[model_type]):
                model_name = MODELS[model_type][index]
                break
            else:
                rprint("[bold red]Número de modelo no válido. Por favor, intente de nuevo.[/bold red]")
        except ValueError:
            rprint("[bold red]Por favor, ingrese un número válido.[/bold red]")
    
    return model_type, model_name

def get_target_email():
    target_email = Prompt.ask("Ingrese el correo electrónico de la persona a analizar")
    return target_email

def add_email_to_profiles(json_folder, email):
    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(json_folder, filename)
            with open(json_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            profile_data['Email'] = email
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=4, ensure_ascii=False)
            rprint(f"[green]Email agregado al perfil {filename}[/green]")


def main():
    rprint(Panel("Bienvenido al Sistema de Análisis de Perfiles", style="bold green"))
    
    model_type, model_name = select_model()
    target_email = get_target_email()

    rprint("[cyan]Scraping de LinkedIn...[/cyan]")
    linkedin_scraper_main()

    rprint("[cyan]Extrayendo imágenes de perfil...[/cyan]")
    image_processor = LinkedInProfileImageProcessor("captura_1", "profile_photos")
    image_processor.process_images()

    rprint("[cyan]Analizando perfiles de LinkedIn...[/cyan]")
    analyzer = LinkedInProfileAnalyzer("capturas_linkedin", "json_profiles")
    analyzer.process_images()

    rprint("[cyan]Agregando email al perfil...[/cyan]")
    add_email_to_profiles("json_profiles", target_email)

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
                name = profile_data.get('Nombre', '').strip()
                company = profile_data.get('Empresa', '').strip()
                # Intenta buscar en otras claves posibles si no se encuentran 'Nombre' o 'Empresa'
                if not name:
                    for key in profile_data.keys():
                        if 'nombre' in key.lower():
                            name = profile_data[key].strip()
                            break
                if not company:
                    for key in profile_data.keys():
                        if 'empresa' in key.lower():
                            company = profile_data[key].strip()
                            break

                if not name or not company:
                    rprint(f"[bold yellow]Advertencia: No se pudo encontrar nombre o empresa para {filename}. Contenido del archivo: {json.dumps(profile_data, indent=2)}[/bold yellow]")
                    continue

                rprint(f"[cyan]Buscando información para: {name} de {company}[/cyan]")
                tavily_search(name, company)

                # Verificar si se crearon los archivos JSON
                # Usaremos la misma función de sanitización que en web_search_tavily.py
                def sanitize_filename(filename):
                    sanitized = re.sub(r'[<>:"/\\|?*.,]', '_', filename)
                    sanitized = sanitized.replace(' ', '_')
                    sanitized = sanitized.strip('_')
                    return sanitized

                name_filename = sanitize_filename(name)
                company_filename = sanitize_filename(company)

                person_file = os.path.join('web_search_results', f'{name_filename}_person_search.json')
                company_file = os.path.join('web_search_results', f'{company_filename}_company_search.json')

                if os.path.exists(person_file) and os.path.exists(company_file):
                    rprint(f"[green]Archivos JSON creados para {name} y {company}[/green]")
                else:
                    rprint(f"[bold yellow]Advertencia: No se encontraron archivos JSON para {name} o {company}[/bold yellow]")
    except Exception as e:
        rprint(f"[bold red]Error durante la búsqueda web con Tavily: {str(e)}[/bold red]")

    rprint("[cyan]Realizando psicoperfilamiento...[/cyan]")
    profile_generator = AIProfileGenerator()
    profile_generator.process_json_files("json_profiles", "profile_photos", "web_search_results", "perfiles_completos", model_type, model_name)

    rprint(Panel("Proceso completado con éxito", style="bold green"))

if __name__ == "__main__":
    main()
