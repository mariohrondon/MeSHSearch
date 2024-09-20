import time 
from datetime import datetime
palabra='se repite?'
numero1= 1
numero2= 2
def suma_simple(numero1, numero2):
    print(numero1+numero2)
def repetir_suma(suma_simple,intervalo_seg=5):
    while True:
        print(f'INICIANDO REPETICICON DE PALABRA:{datetime.now()}')
        suma_simple(numero1,numero2)
        time.sleep(intervalo_seg)
        

repetir_suma(suma_simple, intervalo_seg=5)