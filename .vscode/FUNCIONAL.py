import os

# Establecer la clave de API como variable de entorno
os.environ['NCBI_API_KEY'] = "8ebf817356ed286025790c223adf4e06ca08"

# Verificar que la variable de entorno se ha establecido
if not os.getenv('NCBI_API_KEY'):
    print("NCBI_API_KEY no está establecida")
else:
    print("NCBI_API_KEY está establecida")

print('----------------------------------------------------------------')

import pandas as pd
from metapub import PubMedFetcher
import csv
# Comprobar si la clave de API está correctamente configurada
api_key = os.getenv('NCBI_API_KEY')

# Inicializar metapub con la clave API y Colocar las variables para busqueda tipo pmids queary con keywords
fetch = PubMedFetcher(api_key=api_key)

#chatgtp codigo de busqueda
def buscar_y_exportar_a_csv(termino_busqueda, max_resultados=90000, archivo_csv="resultados_ncbi.csv"):
    try:
        # Realizar la búsqueda en PubMed
        pmids = fetch.pmids_for_query(termino_busqueda, retmax=max_resultados)
        print(f"Total de resultados obtenidos: {len(pmids)}")

        # Crear o abrir el archivo CSV para escribir los resultados
        with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
            escritor_csv = csv.writer(archivo)
            # Escribir encabezados
            escritor_csv.writerow(['Titulo', 'Autor(es)', 'DOI', 'URL', 'Journal', 'NCBIID', 'Citation', 'PMCID', 'Año de Publicación'])

            # Procesar cada PMID
            for pmid in pmids:
                try:
                    # Obtener información del artículo
                    articulo = fetch.article_by_pmid(pmid)
                    # Extraer datos
                    titulo = articulo.title
                    autores = ", ".join(articulo.authors)
                    doi = articulo.doi if articulo.doi else "N/A"
                    url = articulo.url if articulo.url else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    journal = articulo.journal if articulo.journal else "N/A"
                    ncbiid = pmid
                    citation = articulo.citation if articulo.citation else "N/A"
                    pmcid = getattr(articulo, 'pmicd', 'N/A')  # Verificar si el artículo tiene PMCID
                    year_of_publication = articulo.year if articulo.year else "N/A"
                    # Escribir fila en CSV
                    escritor_csv.writerow([titulo, autores, doi, url, journal, ncbiid, citation, pmcid, year_of_publication])
                except Exception as e:
                    print(f"Error al procesar el artículo con PMID {pmid}: {e}")
        
        print(f"Búsqueda completada. Resultados guardados en: {archivo_csv}")

    except Exception as e:
        print(f"Error al realizar la búsqueda: {e}")

# Ejemplo de uso:
termino_de_busqueda = '((((all[sb] NOT(animals [mh] NOT humans [mh])) AND (microbiota [mh])) AND (female genitalia[MeSH Terms]) ) AND (("2010/07/01"[Date - Publication] : "2024/07/21"[Date - Publication]))) NOT (Review[Publication Type])'
buscar_y_exportar_a_csv(termino_de_busqueda, max_resultados=900000)