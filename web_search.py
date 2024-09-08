import os
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import List, Dict

load_dotenv()
tavily_api_key = os.getenv('TAVILY_API_KEY')
tavily_client = TavilyClient(api_key=tavily_api_key)

def web_search(query: str, 
               max_searches: int = 3, 
               max_query_length: int = 1000, 
               search_depth: str = "advanced",
               max_content_length: int = 5000) -> List[Dict]:
    """
    Realiza una búsqueda web utilizando TAVILY.

    Args:
    query (str): La consulta de búsqueda.
    max_searches (int): Número máximo de resultados a devolver.
    max_query_length (int): Longitud máxima de la consulta.
    search_depth (str): Profundidad de la búsqueda ("basic" o "advanced").
    max_content_length (int): Longitud máxima del contenido de cada resultado.

    Returns:
    List[Dict]: Lista de diccionarios con los resultados de la búsqueda web.
    """
    query = query[:max_query_length]
    
    try:
        response = tavily_client.search(query=query, search_depth=search_depth, max_results=max_searches)
        
        results = []
        for result in response['results']:
            content = f"{result['title']}\n\n{result['content']}"
            content = content[:max_content_length]
            
            results.append({
                "title": result['title'],
                "link": result['url'],
                "content": content
            })
        
        print(f"Se encontraron {len(results)} resultados para la búsqueda: {query}")
        return results
    except Exception as e:
        print(f"Error al realizar la búsqueda web con TAVILY: {e}")
        return []
