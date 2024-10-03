from setuptools import setup, find_packages

setup(
    name='MeSHSearch',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'metapub',
        'pandas'  # O cualquier otra dependencia
    ],
    entry_points={
        'console_scripts': [
            'buscar-ncbi=Paquete.main:cli',
        ],
    },
    description='Paquete para buscar avanzada de artículos en NCBI, mediante terminos MeSH y exportar a CSV',
    author='Mario',
    author_email='mariohrondonn@gmail.com',
    url='https://github.com/mariohrondon/MeSHSearch',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
