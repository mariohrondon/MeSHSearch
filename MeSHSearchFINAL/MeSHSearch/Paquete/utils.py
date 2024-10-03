import os
import csv

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
