from typing import List, Dict
from web_search import web_search
import json
import os
import requests
from bs4 import BeautifulSoup
import time
import random
import re

def get_web_search_results(name: str, 
                           company: str,
                           max_searches: int = 5, 
                           max_query_length: int = 1000, 
                           search_depth: str = "advanced",
                           max_content_length: int = 10000) -> List[Dict]:
    """
    Realiza una búsqueda web sobre una persona basada en su nombre y empresa, excluyendo LinkedIn.

    Args:
    name (str): Nombre de la persona.
    company (str): Empresa de la persona.
    max_searches (int): Número máximo de búsquedas permitidas. Por defecto es 5.
    max_query_length (int): Longitud máxima de la consulta. Por defecto es 1000 caracteres.
    search_depth (str): Profundidad de la búsqueda ("basic" o "advanced"). Por defecto es "advanced".
    max_content_length (int): Longitud máxima del contenido de cada resultado. Por defecto es 10000 caracteres.

    Returns:
    List[Dict]: Lista de diccionarios con los resultados de la búsqueda web.
    """
    query = f'"{name}" "{company}" -site:linkedin.com'
    print(f"Realizando búsqueda web con la consulta: {query}")
    results = web_search(query, max_searches, max_query_length, search_depth, max_content_length)
    print(f"Se encontraron {len(results)} resultados para la búsqueda web.")
    return results

def extract_content_from_url(url: str, max_content_length: int = 10000) -> str:
    """
    Extrae el contenido relevante de una URL.

    Args:
    url (str): URL de la página web.
    max_content_length (int): Longitud máxima del contenido a extraer.

    Returns:
    str: Contenido extraído de la página web.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Eliminar scripts, estilos y elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Extraer el título de la página
        title = soup.title.string if soup.title else "Sin título"
        
        # Extraer el contenido principal
        main_content = ""
        for tag in ['article', 'main', 'div', 'p']:
            content = soup.find(tag, class_=re.compile(r'(content|article|main|text)'))
            if content:
                main_content = content.get_text(separator='\n', strip=True)
                break
        
        if not main_content:
            # Si no se encuentra contenido principal, extraer todos los párrafos
            paragraphs = soup.find_all('p')
            main_content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # Combinar título y contenido principal
        full_content = f"Título: {title}\n\nContenido:\n{main_content}"
        
        # Limpiar el texto
        full_content = re.sub(r'\s+', ' ', full_content)  # Eliminar espacios múltiples
        full_content = re.sub(r'\n\s*\n', '\n\n', full_content)  # Eliminar líneas vacías múltiples
        
        return full_content[:max_content_length]
    except Exception as e:
        print(f"Error al extraer contenido de {url}: {str(e)}")
        return ""

def process_profiles(json_folder: str, output_folder: str):
    """
    Procesa los perfiles JSON y realiza búsquedas web para cada uno.

    Args:
    json_folder (str): Carpeta que contiene los archivos JSON de perfiles.
    output_folder (str): Carpeta donde se guardarán los resultados de la búsqueda web.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            with open(os.path.join(json_folder, filename), 'r', encoding='utf-8') as file:
                profile_data = json.load(file)
            
            # Buscar el nombre en diferentes campos posibles
            name = profile_data.get('Nombre') or profile_data.get('nombre') or profile_data.get('name', '')
            
            # Buscar la empresa en diferentes campos posibles
            company = profile_data.get('Empresa') or profile_data.get('empresa') or profile_data.get('company', '')
            
            # Si no hay empresa, intentar extraerla de la experiencia
            if not company and 'Experiencia' in profile_data:
                experiences = profile_data['Experiencia']
                if experiences and isinstance(experiences, list) and len(experiences) > 0:
                    company = experiences[0].get('company', '')

            if name:
                print(f"Realizando búsqueda web para {name} {'de ' + company if company else ''} (excluyendo LinkedIn)...")
                try:
                    web_results = get_web_search_results(name, company)
                    
                    # Extraer contenido de cada URL
                    for result in web_results:
                        print(f"Extrayendo contenido de {result['link']}...")
                        result['extracted_content'] = extract_content_from_url(result['link'])
                        # Pausa aleatoria para evitar ser bloqueado
                        time.sleep(random.uniform(1, 3))
                    
                    output_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_web_search.json")
                    with open(output_filename, 'w', encoding='utf-8') as outfile:
                        json.dump(web_results, outfile, indent=4, ensure_ascii=False)
                    
                    print(f"Resultados de búsqueda web guardados en {output_filename}")
                except Exception as e:
                    print(f"Error durante la búsqueda web para {name}: {str(e)}")
            else:
                print(f"No se pudo realizar la búsqueda web para {filename}. No se encontró el nombre.")

if __name__ == "__main__":
    json_folder = "json_profiles"
    web_search_output_folder = "web_search_results"
    process_profiles(json_folder, web_search_output_folder)
