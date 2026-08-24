import feedparser
import requests
from feedgen.feed import FeedGenerator

SOURCE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCZjpA3YBPXvJv3pg4SPEjfw"

# Definimos los grupos de palabras. Cada lista interna requiere que TODAS 
# sus palabras estén presentes. El video pasará si cumple con CUALQUIERA de los grupos.
FILTROS = [
    ["Nacional","(Goles)"]
]

rss_text = requests.get(SOURCE_RSS, timeout=30).text
feed = feedparser.parse(rss_text)

fg = FeedGenerator()
fg.title("RSS Filtrado")
fg.link(href=SOURCE_RSS)
fg.description("Videos filtrados de YouTube")

for entry in feed.entries:
    title = entry.title
    title_lower = title.lower()

    # Evalúa si todos los elementos de al menos un grupo están en el título
    if any(all(k.lower() in title_lower for k in grupo) for grupo in FILTROS):
        fe = fg.add_entry()

        fe.title(title)
        fe.link(href=entry.link)

        if hasattr(entry, "published"):
            fe.pubDate(entry.published)

        if hasattr(entry, "summary"):
            fe.description(entry.summary)

fg.rss_file("feed.xml")
print("¡RSS generado y guardado como 'feed.xml' exitosamente!")
