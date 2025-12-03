import requests
import json

# 1. CONFIGURACIÓN
API_URL = "http://localhost:8001/api/recommend"

# Los 5 pares de prompts para comparar
test_cases = [
    {
        "tema": "1. CIENCIA FICCIÓN (Viajes en el tiempo)",
        "en": "I am looking for a mind-bending sci-fi movie involving time travel and complex paradoxes.",
        "es": "Busco una película de ciencia ficción alucinante que involucre viajes en el tiempo y paradojas complejas."
    },
    {
        "tema": "2. DRAMA (Emotivo/Real)",
        "en": "A deeply emotional drama that will make me cry, preferably based on a true story.",
        "es": "Un drama profundamente emotivo que me haga llorar, preferiblemente basado en hechos reales."
    },
    {
        "tema": "3. CYBERPUNK (Estética)",
        "en": "Dystopian movies with a cyberpunk aesthetic, neon lights, and high technology.",
        "es": "Películas distópicas con estética cyberpunk, luces de neón y alta tecnología."
    },
    {
        "tema": "4. SOLEDAD (Supervivencia)",
        "en": "Movies about a character trying to survive alone in the wilderness or space.",
        "es": "Películas sobre un personaje intentando sobrevivir solo en la naturaleza o en el espacio."
    },
    {
        "tema": "5. FEEL-GOOD (Ligera)",
        "en": "A feel-good movie to cheer me up, something lighthearted and inspiring.",
        "es": "Una película que me haga sentir bien para animarme, algo ligero e inspirador."
    }
]

def obtener_recomendacion(prompt, idioma):
    """Envía la petición tal cual lo hace tu CURL"""
    
    # Estructura exacta de tu BODY
    payload = {
        "query": prompt,
        "max_results": 5,    # Pedimos 5 para ver la calidad
        "max_runtime": 300   # Ponemos 300 min para que no filtre por duración
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Asumiendo que la API devuelve una lista o un objeto con una lista
            # Ajusta esto si tu respuesta tiene otra forma (ej: data['movies'])
            return data 
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Excepción de conexión: {e}"

# 2. EJECUCIÓN
print(f"{'='*70}")
print(f"TEST COMPARATIVO DE IDIOMAS (all-MiniLM-L6-v2)")
print(f"{'='*70}\n")

for caso in test_cases:
    print(f"--- {caso['tema']} ---")
    
    # Prueba en Inglés
    print(f"🇬🇧 Prompt: \"{caso['en']}\"")
    resultados_en = obtener_recomendacion(caso['en'], "EN")
    print(f"   Resultado: {json.dumps(resultados_en, indent=2, ensure_ascii=False)}\n")
    
    # Prueba en Español
    print(f"🇪🇸 Prompt: \"{caso['es']}\"")
    resultados_es = obtener_recomendacion(caso['es'], "ES")
    print(f"   Resultado: {json.dumps(resultados_es, indent=2, ensure_ascii=False)}")
    
    print("-" * 70 + "\n")