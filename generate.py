import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCZjpA3YBPXvJv3pg4SPEjfw"

# Definimos las palabras clave exactamente como las necesitas
# Usamos minúsculas para compararlas más fácilmente después
KEYWORDS = [
    "(goles)", 
    "nacional"
]

# Obtenemos el feed
rss_text = requests.get(SOURCE_RSS, timeout=30).text
feed = feedparser.parse(rss_text)

# Configuramos el generador del nuevo feed
fg = FeedGenerator()
fg.title("RSS Filtrado")
fg.link(href=SOURCE_RSS)
fg.description("Videos que contienen '(goles)' y 'Nacional'")

# Iteramos y filtramos
for entry in feed.entries:
    title_lower = entry.title.lower()

    # all() asegura que el título contenga AMBOS elementos de la lista
    if all(k.lower() in title_lower for k in KEYWORDS):
        fe = fg.add_entry()

        fe.title(entry.title)
        fe.link(href=entry.link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)

# Generamos el archivo
fg.rss_file("feed.xml")
