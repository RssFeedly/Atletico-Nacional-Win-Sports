import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCZjpA3YBPXvJv3pg4SPEjfw"

# Palabras clave exactas que deben estar en el título
KEYWORDS = ["(goles)", "nacional"]

# Obtenemos el feed
print("Descargando RSS de YouTube...")
response = requests.get(SOURCE_RSS, timeout=30)
feed = feedparser.parse(response.content)

print(f"Total de videos encontrados en el feed: {len(feed.entries)}")

# Configuramos el generador del nuevo feed
fg = FeedGenerator()
fg.title("RSS Filtrado - Goles de Nacional")
fg.link(href=SOURCE_RSS)
fg.description("Videos que contienen '(goles)' y 'nacional'")

added_count = 0

# Iteramos y filtramos
for entry in feed.entries:
    # Limpiamos espacios extra al inicio o final por seguridad
    title = entry.title.strip()
    title_lower = title.lower()
    
    # Imprimimos para verificar en consola qué lee exactamente
    print(f"\nAnalizando título: '{title}'")
    
    # Verificamos si AMBAS palabras clave están en el título en minúsculas
    # Como KEYWORDS ya tiene '(goles)' en minúscula, coincidirá si el título lo tiene
    match_all = all(kw in title_lower for kw in KEYWORDS)
    
    if match_all:
        print(f" -> ¡ÉXITO! Coincidencia encontrada. Agregando al XML...")
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=entry.link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)
            
        added_count += 1
    else:
        print(" -> No cumple con el filtro (falta '(goles)' o 'nacional').")

# Generamos el archivo XML
fg.rss_file("feed.xml", encoding='utf-8')
print(f"\n--- Proceso finalizado ---")
print(f"Se agregaron {added_count} videos al archivo feed.xml")
