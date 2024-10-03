import os

# Abre el archivo en modo de lectura
with open('api_key.txt', 'r') as readfile:
    # Lee la primera línea del archivo
    api_key = readfile.readlines()

# Imprime la primera línea
print(api_key)

import csv
import time
from metapub import PubMedFetcher
from datetime import datetime


# Instanciar PubMedFetcher con la clave API
fetcher = PubMedFetcher(api_key=api_key)

# Función para leer PMIDs existentes del archivo CSV (para evitar duplicados)
def leer_pmids_existentes(archivo_csv):
    
    pmids_existentes = set()
    if os.path.exists(archivo_csv):
        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Saltar los encabezados
            for fila in lector_csv:
                if fila:
                    pmids_existentes.add(fila[5])  # El PMID está en la columna 6 (índice 5)
    return pmids_existentes

# Función para realizar búsqueda con términos MeSH y exportar nuevos resultados a CSV
def buscar_y_exportar_a_csv(termino_busqueda, archivo_csv="resultados_ncbi.csv"):
    
    try:
        # Realizar la búsqueda en PubMed usando el término de búsqueda
        pmids = fetcher.pmids_for_query(termino_busqueda, retmax=1000000)  # Recuperar todos los resultados disponibles

        # Si no se encuentran PMIDs, no hacer nada
        if not pmids:
            print(f"No se encontraron resultados para el término: {termino_busqueda}")
            return

        print(f"Total de resultados obtenidos: {len(pmids)}")

        # Leer PMIDs existentes para evitar duplicados
        pmids_existentes = leer_pmids_existentes(archivo_csv)
        nuevos_pmids = [pmid for pmid in pmids if pmid not in pmids_existentes]

        if not nuevos_pmids:
            print("No hay nuevos resultados para agregar.")
            return

        print(f"Nuevos resultados para agregar: {len(nuevos_pmids)}")

        #
        with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
            escritor_csv = csv.writer(archivo)
            
            # Escribir encabezados solo si el archivo es nuevo
            if os.stat(archivo_csv).st_size == 0:
                escritor_csv.writerow(['Titulo', 'Autor(es)', 'DOI', 'URL', 'Journal', 'NCBIID', 'Citation', 'PMCID', 'Año de Publicación'])

            # Procesar cada nuevo PMID
            for pmid in nuevos_pmids:
                try:
                    # Obtener información del artículo
                    articulo = fetcher.article_by_pmid(pmid)
                    # Extraer datos
                    titulo = articulo.title
                    autores = ", ".join(articulo.authors)
                    doi = articulo.doi if articulo.doi else "N/A"
                    url = articulo.url if articulo.url else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    journal = articulo.journal if articulo.journal else "N/A"
                    ncbiid = pmid
                    citation = articulo.citation if articulo.citation else "N/A"
                    pmcid = getattr(articulo, 'pmcid', 'N/A')
                    year_of_publication = articulo.year if articulo.year else "N/A"
                    
                    # Escribir fila en CSV
                    escritor_csv.writerow([titulo, autores, doi, url, journal, ncbiid, citation, pmcid, year_of_publication])
                except Exception as e:
                    print(f"Error al procesar el artículo con PMID {pmid}: {e}")
        
        print(f"Los nuevos resultados fueron agregados al archivo: {archivo_csv}")

    except Exception as e:
        print(f"Error al realizar la búsqueda: {e}")

# Función para ejecutar la búsqueda cada 24 horas

def ejecutar_busqueda_periodica(buscar_y_exportar_a_csv,intervalos_horas=5):
    while True:
        print(f"INICIANDO busqueda en PudMed: {datetime.now()}")
        buscar_y_exportar_a_csv(termino_de_busqueda, archivo_csv="resultados_ncbi.csv")
        time.sleep(intervalos_horas)

# Ejemplo de uso:
termino_de_busqueda = '((((all[sb] NOT(animals [mh] NOT humans [mh])) AND (microbiota [mh])) AND (female genitalia[MeSH Terms]) ) AND (("2010/07/01"[Date - Publication] : "2024/07/21"[Date - Publication]))) NOT (Review[Publication Type])'
buscar_y_exportar_a_csv(termino_de_busqueda)
#Busqueda periodica 

ejecutar_busqueda_periodica(buscar_y_exportar_a_csv, intervalos_horas=5)

#-------- Implementacion de CLI

import argparse

def cli():
    parser = argparse.ArgumentParser(description='Buscar artículos en NCBI y exportar a CSV.')
    
    parser.add_argument('--termino', type=str, required=True, help='Término de búsqueda en NCBI.')
    parser.add_argument('--archivo', type=str, default='resultados_ncbi.csv', help='Archivo CSV donde exportar los resultados.')
    parser.add_argument('--intervalo', type=float, default=24, help='Intervalo de búsqueda (default: 24 horas).')
    parser.add_argument('--unidad', type=str, choices=['segundos', 'minutos', 'horas'], default='horas', 
                        help='Unidad de tiempo para el intervalo (default: horas).')

    args = parser.parse_args()

    # Convertir el intervalo a segundos según la unidad de tiempo
    if args.unidad == 'segundos':
        intervalo_segundos = args.intervalo
    elif args.unidad == 'minutos':
        intervalo_segundos = args.intervalo * 60
    else:
        intervalo_segundos = args.intervalo * 3600

    ejecutar_busqueda_periodica(args.termino, args.archivo, intervalo_segundos)

