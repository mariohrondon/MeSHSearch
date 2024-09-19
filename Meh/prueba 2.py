import os

# Establecer la clave de API como variable de entorno
os.environ['NCBI_API_KEY'] = 'tu_clave_de_api_aqui'

# Verificar que la variable de entorno se ha establecido
if not os.getenv('NCBI_API_KEY'):
    print("NCBI_API_KEY no está establecida")
else:
    print("NCBI_API_KEY está establecida")

'--------------------------------------'
import pandas as pd
from metapub import PubMedFetcher

keyword = '((((all[sb] NOT(animals [mh] NOT humans[mh] AND(microbiota[mh]))AND(female genitalia[MeSH Terms]) ) AND (("2010/07/01"[Date - Publication]: "2024/07/21"[Date - Publication]))) NOT (Review[Publication Type]))'
num_of_articles = 500
fetch = PubMedFetcher()
pmids = fetch.pmids_for_query (keyword, retmax= num_of_articles)
articles = {}

#retrieve information for ech article 
for pmid in pmids:
    articles[pmid] = fetch._eutils_article_by_pmid(pmid)

#retrieve relevant information adn create Data Frames 
titles={}
for pmids in pmids:
    titles[pmids] = fetch._eutils_article_by_pmid(pmid).title
Title = pd.DataFrame(list(titles.items(), colums=['pmids','Title']))
# data frames de author 
author={}
for pmids in pmids:
    author[pmids] = fetch._eutils_article_by_pmid(pmid).author
Author = pd.DataFrame(list(author.items(),colums= ['pmids', 'Authors']))

#Merge all DataFrames into a single one 
data_frames = [Title]
from functools import reduce
df_merge = reduce(lambda left, right: pd.merge(left,right, on=['pmid'], how='outer'), data_frames) 

df_merge.to_csv('Prueba uno de recoleccion de datos')
#-------------------------------
with  open(archivo_csv, mode='w', encoding='utf-8') as archivo:
    escritor_csv = csv.writer(archivo)
    #encabezados
    escritor_csv.writerow(['Title'])