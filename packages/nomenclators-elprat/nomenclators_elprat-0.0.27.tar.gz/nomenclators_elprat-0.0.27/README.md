# Nomenclator Archetype

**Nomenclator Archetype** es una librería para generar implementaciones CRUD y utilizar dependencias 
siguiendo los principios de la arquitectura **Domain-Driven Design (DDD)**.

Proporciona una estructura modular y reutilizable para proyectos futuros del ayuntamiento de l'Prat, 
incluyendo capas de Dominio, Repositorio, Servicio y Rutas.

## Características

- Basado en los principios de Domain-Driven Design.
- Generación automática de CRUD utilizando comandos personalizados.
- Plantillas configurables con Jinja2 para adaptarse a diferentes necesidades.
- Integración con FastAPI para generación de rutas RESTful.
- Extensible para diferentes tipos de almacenamiento y lógica de negocio.

## Requisitos

- Python 3.9.20 o superior.
- Dependencias:
  - `click`
  - `jinja2`
  - `fastapi`
  - `SQLAlchemy`

## Instalación

1. Clona el repositorio o descarga el código fuente.
2. Instala la librería utilizando `pip`:

   ```bash
   pip install .
