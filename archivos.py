import os

def graficar_cola(dot, nombre):
    path = os.getcwd() +'/reportes_de_colas_de_secuencia/'+nombre+'.dot'
    
    archivo = open(path, 'w')
    archivo.write(dot)
    archivo.close()