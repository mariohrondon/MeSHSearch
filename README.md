# Extracción de Información de Artículos Usando Términos MeSH dentro del repositorio de PudMed

Este proyecto tiene como objetivo automatizar la extracción de información de artículos científicos de bases de datos como PubMed utilizando términos MeSH (Medical Subject Headings). La información que ha sido extraída se organiza y se guarda dentro en un archivo CSV para facilitar su análisis.

## Características

- **Búsquedas basadas en MeSH**: Utiliza términos MeSH para realizar consultas precisas.
- **Extracción de datos**: Extrae información relevante de los artículos como título, autores, resumen, fecha de publicación, entre otros.
- **Almacenamiento en CSV**: La información obtenida se guarda en un archivo CSV para un análisis sencillo o integración con otros sistemas.
- **Automatización**: Permite configurar la búsqueda para que se ejecute de manera periódica y se actualice el archivo CSV automáticamente si se encuentran nuevos artículos.
  
## Requisitos

- Python 3.12.66
- Las siguientes bibliotecas de Python:
  - `pandas`
  - `requests`
  - `csv`
  - `metapub`
  - `click` (para la interfaz de línea de comandos)

Puedes instalar las dependencias ejecutando:

```bash
pip install -r requirements.txt
