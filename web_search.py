import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def web_search(query: str, 
               max_searches: int = 3, 
               max_query_length: int = 1000, 
               search_depth: str = "advanced",
               max_content_length: int = 5000) -> List[Dict]:
    """
    Realiza una búsqueda web básica utilizando Google.

    Args:
    query (str): La consulta de búsqueda.
    max_searches (int): Número máximo de resultados a devolver.
    max_query_length (int): Longitud máxima de la consulta.
    search_depth (str): Profundidad de la búsqueda (no se utiliza en esta implementación básica).
    max_content_length (int): Longitud máxima del contenido de cada resultado.

    Returns:
    List[Dict]: Lista de diccionarios con los resultados de la búsqueda web.
    """
    query = query[:max_query_length]  # Limitar la longitud de la consulta
    url = f"https://www.google.com/search?q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div', class_='g')[:max_searches]:
        anchor = g.find('a')
        if anchor:
            link = anchor['href']
            title = anchor.find('h3')
            title = title.text if title else "Sin título"
            snippet = g.find('div', class_='VwiC3b')
            snippet = snippet.text if snippet else "Sin descripción"
            
            content = f"{title}\n\n{snippet}"
            content = content[:max_content_length]  # Limitar la longitud del contenido
            
            results.append({
                "title": title,
                "link": link,
                "content": content
            })
    
    return results
