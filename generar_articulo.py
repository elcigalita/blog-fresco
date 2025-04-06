import openai
import datetime
import os
import re
import requests
import pytz
import time
from dotenv import load_dotenv
from pytrends.request import TrendReq

# Cargar API key de OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# ========== CONFIGURACIÓN PERSONAL ==========
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
# ============================================

def obtener_keywords(tema_base):
    try:

        time.sleep(10)  # duerme 10 segundos antes de cada petición
        pytrends = TrendReq(hl='es-ES', tz=360, geo='ES')
        sugerencias = pytrends.suggestions(keyword=tema_base)
        if sugerencias:
            return [s['title'] for s in sugerencias[:3]]
    except Exception as e:
        print(f"⚠️ Error al obtener sugerencias para '{tema_base}': {e}")
    return []

# Buscar keywords de forma progresiva hasta encontrar alguna válida
# Lista en caché de keywords por tema
fallback_keywords = {
    "curiosidades sobre inteligencia artificial": ["qué es la inteligencia artificial", "cómo funciona la IA", "ejemplos de IA"],
    "inteligencia artificial": ["aplicaciones de IA", "IA explicada fácil", "ventajas de la inteligencia artificial"],
    "chatgpt": ["qué es chatgpt", "cómo usar chatgpt", "ejemplos de prompts"],
    "machine learning": ["algoritmos de aprendizaje automático", "modelos supervisados", "ML ejemplos"],
    "automatización": ["automatización con IA", "procesos automáticos", "robots inteligentes"],
    "big data": ["qué es big data", "análisis de datos masivos", "uso de big data"],
    "redes neuronales": ["red neuronal artificial", "entrenamiento de redes", "casos reales de redes neuronales"]
}

# Elegir keywords desde la caché, en orden de temas
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

# ================= GENERAR TÍTULO =================
prompt_titulo = (
    f"Genera un título para un artículo de blog optimizado para SEO sobre {tema}. "
    f"Usa palabras clave como: {keywords_txt}. "
    f"Debe responder a una pregunta como 'qué es', 'cómo funciona', etc. "
    f"Evita listas tipo '5 cosas' o comillas. Hazlo natural y atractivo."
)

titulo_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_titulo}]
)
titulo = titulo_response.choices[0].message.content.strip()
titulo = titulo.replace('"', '').replace("“", "").replace("”", "").strip()

# ================= GENERAR ARTÍCULO =================
prompt_articulo = (
    f"Escribe un artículo original de unas 600 palabras sobre {tema}. "
    f"Incluye los conceptos clave: {keywords_txt}. "
    f"Evita estructuras repetitivas y listas numeradas. "
    f"Usa un tono divulgativo, profesional pero cercano. No uses contenido con copyright."
)

contenido_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_articulo}]
)
contenido = contenido_response.choices[0].message.content.strip()

# ================= FORMATEAR ARCHIVO =================
zona_horaria = pytz.timezone("Europe/Madrid")
fecha_actual = datetime.datetime.now(zona_horaria)
fecha_str = fecha_actual.strftime("%Y-%m-%d")
hora_str = fecha_actual.strftime("%H:%M:%S %z")
slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
nombre_archivo = f"_posts/{fecha_str}-{slug}.md"

# ================= DESCARGAR IMAGEN =================
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

# ================= GUARDAR POST =================
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

