import openai
import datetime
import os
import re
from dotenv import load_dotenv

# Cargar API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Prompt con variedad e innovación
prompt = (
    "Escribe un artículo original y divulgativo de unas 600 palabras sobre un tema sorprendente de inteligencia artificial. "
    "Evita repetir estructuras como '5 curiosidades'. Sé informal, llamativo, y evita contenido con copyright. "
    "Al final del artículo, sugiere 3 etiquetas separadas por comas (formato: etiquetas: tag1, tag2, tag3)."
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

contenido = response.choices[0].message.content

# Extraer título
titulo_match = re.search(r"^# (.+)", contenido)
titulo = titulo_match.group(1).strip() if titulo_match else "Artículo sobre IA"

# Extraer excerpt para SEO
excerpt_match = re.search(r"(?:^# .+\n+)(.*?)(\n|$)", contenido, re.DOTALL)
excerpt = excerpt_match.group(1).strip() if excerpt_match else ""

# Extraer etiquetas
lineas = contenido.strip().split('\n')
tags_line = lineas[-1] if "etiquetas:" in lineas[-1].lower() else "etiquetas: ia, tecnologia, curiosidades"
tags = [tag.strip() for tag in tags_line.split(":")[-1].split(",")]

# Limpiar contenido (quitar línea de etiquetas)
if "etiquetas:" in lineas[-1].lower():
    contenido = "\n".join(lineas[:-1])

# Slug y fecha
slug = re.sub(r'[^a-zA-Z0-9\-]', '', titulo.lower().replace(' ', '-'))[:50]
fecha = datetime.datetime.now().strftime("%Y-%m-%d")
nombre_archivo = f"_posts/{fecha}-{slug}.md"

# ✅ Diccionario para imágenes según categoría principal
categoria_principal = tags[0].lower() if tags else "ia"

imagenes_por_categoria = {
    "ia": "https://source.unsplash.com/800x400/?artificial-intelligence",
    "tecnologia": "https://source.unsplash.com/800x400/?technology,futuristic",
    "curiosidades": "https://source.unsplash.com/800x400/?curious,thinking,lightbulb",
    "etica": "https://source.unsplash.com/800x400/?ethics,ai,balance",
    "noticias": "https://source.unsplash.com/800x400/?news,ai"
}

imagen_url = imagenes_por_categoria.get(categoria_principal, "https://source.unsplash.com/800x400/?ai")

# 📝 Front matter
front_matter = f"""---
layout: post
title:  "{titulo}"
date:   {fecha} 12:00:00 +0000
categories: ia curiosidades tecnologia
tags: [{', '.join(tags)}]
excerpt: "{excerpt[:160]}"
image: {imagen_url}
---

"""

# Crear carpeta y guardar
os.makedirs("_posts", exist_ok=True)
with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(front_matter + f"![Imagen relacionada]({imagen_url})\n\n" + contenido)

print(f"✅ Artículo generado: {nombre_archivo}")
