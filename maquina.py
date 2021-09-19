from linea_produccion import *
from producto import *
from cola import *
import re
import xml.etree.ElementTree as ET

class NodoMaquina():
    def __init__(self, cantidad_lineas_de_produccion, linea_de_produccion, productos):
        self.cantidad_lineas_de_produccion = cantidad_lineas_de_produccion
        self.linea_de_produccion = linea_de_produccion
        self.productos = productos
        self.anterior = None
        self.siguiente = None

class Maquina():
    def __init__(self):
        self.inicio = None
    
    def aniadir_listas_a_la_maquina(self, cantidad_lineas_de_produccion, linea_de_produccion, productos):
        nuevo = NodoMaquina(cantidad_lineas_de_produccion, linea_de_produccion, productos)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def mostrar_todas_los_datos_de_mi_maquina(self):
        tmp = self.inicio
        while tmp is not None:
            print('**Cantidad de lineas de produccion**')
            print('\t',tmp.cantidad_lineas_de_produccion)
            
            tmp.linea_de_produccion.mostrar_lineas_de_produccion()
            
            tmp.productos.motrar_productos()
            tmp = tmp.siguiente
    
    def obtener_por_linea_de_ensamblaje(self, numero):#Obtener valores de la lista por medio de la linea de ensamblaje
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.linea_de_produccion:
                if i.get_numero() == numero:
                    print('numero: '+str(i.get_numero())+', Cantidad de componentes: '+str(i.cantidad_componentes)+', Tiempo de ensamblaje: '+str(i.tiempo_ensamblaje))
            tmp = tmp.siguiente
        return None
    
    def obtener_producto_por_nombre(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.productos:
                if i.get_nombre() == nombre:
                    print('nombre: '+str(i.get_nombre())+' Linea de elaboracion: '+str(i.get_elaboracion()))
            tmp = tmp.siguiente
        return None
    
    def graficar_cola_de_un_producto(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.productos:
                cola = ListaSimple()
                if i.get_nombre() == nombre:
                    resultado = re.findall("L[1-9]+p?C[1-9]+", str(i.get_elaboracion()))#Aqui retorna una lista
                    # print(resultado)
                    for j in range(len(resultado)):
                        cola.enqueue(resultado[j])#Sin embargo aqui ya se pasa a un TDA para su respectiva grafica
                    cola.graficar(nombre)
            tmp = tmp.siguiente
        return None


matriz_maquina = Maquina()
def cargar_datos_de_archivo_a_objeto_maquina():
    
    #Aqui tiene que ser un tipo de get text
    tree = ET.parse('maquina.xml')
    root = tree.getroot()
    
    
    for elemento in root:
        cantidad_lineas_produccion = elemento.text
        cantidad_lineas_produccion = cantidad_lineas_produccion.replace('\t', '')
        cantidad_lineas_produccion = cantidad_lineas_produccion.replace('\n', '')
        # print(cantidad_lineas_produccion)
        lista_lineas_produccion = LineaProduccion()
        lista_de_productos = Productos()

        for subelement in elemento.iter('LineaProduccion'):
            numero = int(subelement.find('Numero').text)
            cantidad_componentes = int(subelement.find('CantidadComponentes').text)
            tiempo_ensamblaje = int(subelement.find('TiempoEnsamblaje').text)
            # print(numero, cantidad_componentes, tiempo_ensamblaje)
            lista_lineas_produccion.insertar_linea_de_produccion(numero, cantidad_componentes, tiempo_ensamblaje)
        
        for subelement in elemento.iter('Producto'):
            nombre = subelement.find('nombre').text
            elaboracion = subelement.find('elaboracion').text
            lista_de_productos.insertar_producto(nombre.strip(), elaboracion.strip())
        matriz_maquina.aniadir_listas_a_la_maquina(cantidad_lineas_produccion, lista_lineas_produccion, lista_de_productos)
    
def graficar_cola_de_elaboracion(nombre):
    matriz_maquina.graficar_cola_de_un_producto(nombre)
    


if __name__ == '__main__':
    # maquina = Maquina()
    # lp = LineaProduccion()
    # lp.insertar_linea_de_produccion(5, 20, 4)#lista
    # pr = Productos()
    # pr.insertar_producto('smartwatch', 'L2pC5 L10pC6 L6pC15 L4pC22 L11pC3 L5pC8 L13pC1 L8pC9 L5pC5 L2pC5 L13pC14 L12pC22 L13pC16')
    # maquina.aniadir_listas_a_la_maquina(5, lp, pr)
    # maquina.mostrar_todas_los_datos_de_mi_maquina()
    # maquina.obtener_por_linea_de_ensamblaje(5)
    # maquina.obtener_producto_por_nombre('smartwatch')
    cargar_datos_de_archivo_a_objeto_maquina()
    # matriz_maquina.mostrar_todas_los_datos_de_mi_maquina()
    matriz_maquina.obtener_producto_por_nombre('Barbie')
    graficar_cola_de_elaboracion('Barbie')
    
