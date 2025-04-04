import openai
import datetime
import os
import re
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave desde el entorno
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Prompt para el artículo
prompt = "Escribe un artículo de 600 palabras sobre 5 curiosidades increíbles sobre inteligencia artificial. Usa un tono informal y divulgativo."

# Solicitud al modelo
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# Contenido generado
contenido = response.choices[0].message.content

# Generar título y slug seguro
titulo = contenido.split('\n')[0].replace('# ', '').strip()
if len(titulo) < 5:
    titulo = "Curiosidades sobre IA"

slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
fecha = datetime.datetime.now().strftime("%Y-%m-%d")
nombre_archivo = f"_posts/{fecha}-{slug}.md"

# Front matter de Jekyll
front_matter = f"""---
layout: post
title:  "{titulo}"
date:   {fecha} 12:00:00 +0000
categories: ia curiosidades tecnologia
---

"""

# Crear carpeta si no existe
os.makedirs("_posts", exist_ok=True)

# Guardar el artículo
with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(front_matter + contenido)

print(f"✅ Artículo guardado como: {nombre_archivo}")
