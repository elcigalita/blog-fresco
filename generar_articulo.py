import openai
import datetime
import os
import re
from dotenv import load_dotenv
from pytrends.request import TrendReq

# Cargar la API key desde .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# ===== PERSONALIZACIÓN =====
tema = "curiosidades sobre inteligencia artificial"
tema_fallback = "inteligencia artificial"
categoria_principal = "ia"
tags = "ia curiosidades tecnologia"
# ===========================

# Paso 1: Obtener keywords desde Google Trends
def obtener_keywords(tema_base):
    try:
        pytrends = TrendReq(hl='es-ES', tz=360)
        pytrends.build_payload([tema_base], cat=0, timeframe='now 7-d', geo='', gprop='')
        related_queries = pytrends.related_queries()
        top_related = related_queries.get(tema_base, {}).get('top')

        if top_related is not None and not top_related.empty:
            return [fila['query'] for fila in top_related.head(3).to_dict('records')]
    except Exception as e:
        print(f"⚠️ Error al obtener keywords para '{tema_base}': {e}")

    return []

# Intenta primero con el tema original
palabras_clave = obtener_keywords(tema)

# Si no hay resultados, intenta con un tema genérico
if not palabras_clave:
    print(f"⚠️ No se encontraron keywords para '{tema}', probando con '{tema_fallback}'...")
    palabras_clave = obtener_keywords(tema_fallback)

# Si aún no hay, usar keywords por defecto
if not palabras_clave:
    print("⚠️ No se encontraron keywords. Usando palabras clave por defecto.")
    palabras_clave = ["inteligencia artificial", "cómo funciona", "ejemplos"]

keywords_txt = ", ".join(palabras_clave)

# Paso 2: Generar título optimizado para SEO
prompt_titulo = (
    f"Genera un título para un artículo de blog optimizado para SEO sobre {tema}. "
    f"Usa palabras clave como: {keywords_txt}. "
    f"El título debe responder a una pregunta como 'qué es', 'cómo funciona', 'ejemplos de', etc. "
    f"Evita listas tipo '5 cosas' o comillas. Hazlo natural, claro y atractivo."
)

titulo_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_titulo}]
)
titulo = titulo_response.choices[0].message.content.strip()

# Paso 3: Generar artículo original
prompt_articulo = (
    f"Escribe un artículo original de unas 600 palabras sobre {tema}. "
    f"Incluye los conceptos clave: {keywords_txt}. "
    f"Evita estructuras repetitivas como listas numeradas. "
    f"Usa un tono divulgativo, profesional pero cercano. No uses contenido con derechos de autor."
)

contenido_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_articulo}]
)
contenido = contenido_response.choices[0].message.content.strip()

# Paso 4: Formatear fecha y slug
fecha_actual = datetime.datetime.now()
fecha_str = fecha_actual.strftime("%Y-%m-%d")
hora_str = "12:00:00 +0000"
slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
nombre_archivo = f"_posts/{fecha_str}-{slug}.md"

# Paso 5: URL de imagen sin copyright desde Unsplash
imagen_url = f"https://source.unsplash.com/800x400/?{categoria_principal}"

# Paso 6: Front matter con metadata y keywords
front_matter = f"""---
layout: post
title:  "{titulo}"
date:   {fecha_str} {hora_str}
categories: {tags}
image: {imagen_url}
keywords: [{keywords_txt}]
---

![Imagen relacionada]({imagen_url})
"""

# Paso 7: Crear carpeta y guardar el archivo
os.makedirs("_posts", exist_ok=True)
with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + contenido)

print(f"✅ Artículo generado correctamente: {nombre_archivo}")
