import openai
import datetime
import os
import re
import requests
import pytz
from dotenv import load_dotenv

# ========== CARGA API ==========
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# ========== CONFIGURACIÓN ==========
tema = "curiosidades sobre inteligencia artificial"
temas_alternativos = [
    "inteligencia artificial",
    "chatgpt",
    "machine learning",
    "automatización",
    "big data",
    "redes neuronales"
]
categoria_principal = "ia"
tags = "ia curiosidades tecnologia"

# ========== KEYWORDS EN CACHÉ ==========
fallback_keywords = {
    "curiosidades sobre inteligencia artificial": ["qué es la inteligencia artificial", "cómo funciona la IA", "ejemplos de IA"],
    "inteligencia artificial": ["aplicaciones de IA", "IA explicada fácil", "ventajas de la inteligencia artificial"],
    "chatgpt": ["qué es chatgpt", "cómo usar chatgpt", "ejemplos de prompts"],
    "machine learning": ["algoritmos de aprendizaje automático", "modelos supervisados", "ML ejemplos"],
    "automatización": ["automatización con IA", "procesos automáticos", "robots inteligentes"],
    "big data": ["qué es big data", "análisis de datos masivos", "uso de big data"],
    "redes neuronales": ["red neuronal artificial", "entrenamiento de redes", "casos reales de redes neuronales"]
}

# ========== OBTENER KEYWORDS ==========
palabras_clave = []
temas_a_probar = [tema] + temas_alternativos

for intento in temas_a_probar:
    print(f"🔍 Buscando keywords para: {intento}")
    if intento in fallback_keywords:
        palabras_clave = fallback_keywords[intento]
        print(f"✅ Keywords cargadas desde caché: {palabras_clave}")
        break

if not palabras_clave:
    print("⚠️ No se encontraron keywords. Usando genéricas.")
    palabras_clave = ["inteligencia artificial", "cómo funciona", "ejemplos"]

keywords_txt = ", ".join(palabras_clave)

# ========== GENERAR TÍTULO VARIADO ==========
prompt_titulo = (
    f"Genera un título original y optimizado para SEO para un artículo de blog divulgativo sobre {tema}. "
    f"Usa alguna de estas palabras clave: {keywords_txt}. "
    f"Evita fórmulas comunes como 'Qué es...' o 'Cómo funciona...'. "
    f"Inspírate en enfoques creativos, históricos, polémicos, cotidianos o de impacto. "
    f"Debe ser llamativo, natural, claro y único."
)

titulo_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_titulo}]
)
titulo = titulo_response.choices[0].message.content.strip()
titulo = titulo.replace('"', '').replace("“", "").replace("”", "").strip()

# ========== GENERAR ARTÍCULO VARIADO ==========
prompt_articulo = (
    f"Escribe un artículo original de unas 600 palabras sobre {tema}, usando estas palabras clave: {keywords_txt}. "
    f"Evita introducirlo con frases genéricas como 'La inteligencia artificial (IA) es...'. "
    f"Elige un enfoque distinto: histórico, cotidiano, comparativo, humorístico o de impacto. "
    f"No uses listas numeradas. El tono debe ser divulgativo, natural y cercano. "
    f"No uses contenido repetitivo ni con derechos de autor."
)

contenido_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_articulo}]
)
contenido = contenido_response.choices[0].message.content.strip()

# ========== FECHA, SLUG Y ARCHIVO ==========
zona_horaria = pytz.timezone("Europe/Madrid")
fecha_actual = datetime.datetime.now(zona_horaria)
fecha_str = fecha_actual.strftime("%Y-%m-%d")
hora_str = fecha_actual.strftime("%H:%M:%S %z")
slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
nombre_archivo = f"_posts/{fecha_str}-{slug}.md"

# ========== DESCARGAR IMAGEN ==========
imagen_url_remota = f"https://source.unsplash.com/800x400/?{categoria_principal}"
imagen_local_path = f"assets/images/posts/{fecha_str}-{slug}.jpg"
imagen_local_url = f"/assets/images/posts/{fecha_str}-{slug}.jpg"
os.makedirs("assets/images/posts", exist_ok=True)

try:
    response = requests.get(imagen_url_remota)
    if response.status_code == 200:
        with open(imagen_local_path, "wb") as img_file:
            img_file.write(response.content)
        print("✅ Imagen descargada correctamente.")
    else:
        print(f"⚠️ Error al descargar imagen: Código {response.status_code}")
except Exception as e:
    print(f"⚠️ Error al descargar imagen: {e}")

# ========== GUARDAR POST ==========
front_matter = f"""---
layout: post
title: "{titulo}"
date: {fecha_str} {hora_str}
categories: {tags}
image: {imagen_local_url}
keywords: [{keywords_txt}]
---

![Imagen relacionada sobre {categoria_principal}]({imagen_local_url})
"""

os.makedirs("_posts", exist_ok=True)
with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + contenido)

print(f"✅ Artículo generado correctamente: {nombre_archivo}")


