import os
import sys
import json
import re
from dotenv import load_dotenv
from tavily import TavilyClient
import requests

load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*.,]', '_', filename)
    sanitized = sanitized.replace(' ', '_')
    sanitized = sanitized.strip('_')
    return sanitized

def search_with_tavily(query, max_results=10):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    try:
        response = tavily_client.search(query, search_depth="advanced", max_results=max_results, exclude_domains=["linkedin.com"])
        # Filtrar resultados para excluir cualquier URL de LinkedIn que pueda haber pasado
        filtered_results = [result for result in response['results'] if 'linkedin.com' not in result['url']]
        response['results'] = filtered_results
        return response
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP al realizar la búsqueda: {e}")
        if e.response.status_code == 400:
            print("Error 400: Bad Request. Verifica que la consulta sea válida y que tu API key sea correcta.")
        elif e.response.status_code == 401:
            print("Error 401: No autorizado. Verifica que tu API key sea válida y esté correctamente configurada.")
        else:
            print(f"Código de estado HTTP: {e.response.status_code}")
        print(f"Respuesta del servidor: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error inesperado al realizar la búsqueda: {e}")
        return None

def save_results(results, filename):
    if results is None:
        print(f"No se pudieron guardar los resultados en {filename} porque la búsqueda falló.")
        return
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    print(f"Resultados guardados en {filename}")

def main(name, company):
    print(f"Buscando información sobre: {name} de {company}")

    # Asegurarse de que la carpeta 'web_search_results' exista
    if not os.path.exists('web_search_results'):
        os.makedirs('web_search_results')
        print("Carpeta 'web_search_results' creada.")

    # Sanear los nombres para los archivos
    name_filename = sanitize_filename(name)
    company_filename = sanitize_filename(company)

    # Primera búsqueda: persona y empresa
    person_query = f"{name} {company} -site:linkedin.com"
    person_results = search_with_tavily(person_query)
    person_file = os.path.join('web_search_results', f'{name_filename}_person_search.json')
    save_results(person_results, person_file)

    # Segunda búsqueda: empresa (con manejo de consultas cortas)
    company_query = f"{company} -site:linkedin.com" if len(company) >= 5 else f"{company} company -site:linkedin.com"
    company_results = search_with_tavily(company_query)
    company_file = os.path.join('web_search_results', f'{company_filename}_company_search.json')
    save_results(company_results, company_file)

    if os.path.exists(person_file) and os.path.exists(company_file):
        print(f"Los resultados han sido guardados en:\n{person_file}\n{company_file}")
    else:
        print("No se pudieron guardar todos los resultados. Verifique los archivos en 'web_search_results'.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Por favor, proporcione el nombre de la persona y la empresa como argumentos.")
        sys.exit(1)
    name = sys.argv[1]
    company = sys.argv[2]
    main(name, company)
