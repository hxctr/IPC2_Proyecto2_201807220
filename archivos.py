import os

def graficar_cola(dot, nombre):
    nombre = nombre.replace(' ', '_')
    
    path = os.getcwd() +'/'+(nombre)+'.dot'
    
    archivo = open(path, 'w')
    archivo.write(dot)
    archivo.close()
    
    os.system('dot.exe -Tjpg '+str(nombre)+'.dot -o '+str(nombre)+'.jpg')