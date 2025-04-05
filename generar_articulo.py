import openai
import datetime
import os
import re
from dotenv import load_dotenv

# Cargar la API key desde .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# ===== PERSONALIZACIÓN =====
tema = "curiosidades sobre inteligencia artificial"
categoria_principal = "ia"
tags = "ia curiosidades tecnologia"
# ===========================

# Paso 1: Generar título llamativo y breve
prompt_titulo = f"Genera un título breve, original y llamativo para un artículo de blog divulgativo sobre {tema}. No uses comillas."
titulo_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_titulo}]
)
titulo = titulo_response.choices[0].message.content.strip()

# Paso 2: Generar artículo original
prompt_articulo = (
    f"Escribe un artículo original de unas 600 palabras sobre {tema}. "
    f"Evita estructuras repetitivas como '5 cosas' o listas numeradas. "
    f"Usa un tono divulgativo, profesional pero cercano. No uses contenido con derechos de autor."
)
contenido_response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_articulo}]
)
contenido = contenido_response.choices[0].message.content.strip()

# Paso 3: Formatear fecha y slug
fecha_actual = datetime.datetime.now()
fecha_str = fecha_actual.strftime("%Y-%m-%d")
slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
hora_str = "12:00:00 +0000"
nombre_archivo = f"_posts/{fecha_str}-{slug}.md"

# Paso 4: URL de imagen sin copyright desde Unsplash
imagen_url = f"https://source.unsplash.com/800x400/?{categoria_principal}"

# Paso 5: Front matter con imagen y metadata
front_matter = f"""---
layout: post
title:  "{titulo}"
date:   {fecha_str} {hora_str}
categories: {tags}
---

![Imagen relacionada]({imagen_url})
"""

# Paso 6: Crear carpeta y guardar
os.makedirs("_posts", exist_ok=True)
with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + contenido)

print(f"✅ Artículo generado correctamente: {nombre_archivo}")
