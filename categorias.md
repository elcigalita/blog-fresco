---
layout: default
title: Categorías
permalink: /categorias/
---

<h1>Categorías del blog</h1>
<ul>
  {% assign categorias = site.categories | sort %}
  {% for category in categorias %}
    {% assign name = category[0] %}
    {% assign posts = category[1] %}
    <li>
      <a href="{{ '/categoria/' | append: name | append: '/' | relative_url }}">
        {{ name | capitalize }}
      </a> ({{ posts | size }})
    </li>
  {% endfor %}
</ul>
