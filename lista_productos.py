from producto import *
from cola import *
import re

class NodoListaDeProductos():
    def __init__(self, producto):
        self.producto = producto
        self.anterior = None
        self.siguiente = None

class ListaDeProductos():
    def __init__(self):
        self.inicio = None
    
    def aniadir_lista_de_productos(self, lista_de_productos):
        nuevo = NodoListaDeProductos(lista_de_productos)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def mostar_lista_de_productos(self):
        tmp = self.inicio
        while tmp is not None:
            tmp.producto.motrar_productos()
            tmp = tmp.siguiente
    
    def obtener_producto_por_nombre(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.producto:
                if i.get_nombre() == nombre:
                    print('nombre: '+str(i.get_nombre())+' Linea de elaboracion: '+str(i.get_elaboracion()))
                tmp = tmp.siguiente
        return None
    
    def graficar_cola_de_un_producto(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.producto:
                cola = ListaSimple()
                if i.get_nombre() == nombre:
                    resultado = re.findall("L[1-9]+p?C[1-9]+", str(i.get_elaboracion()))
                    print(resultado)
                    for j in range(len(resultado)):
                        cola.enqueue(resultado[j])
                    cola.graficar(nombre)
                tmp = tmp.siguiente
        return None

if __name__ == '__main__':
    lp = Productos()
    lp.insertar_producto('smartwatch', 'L2pC5 L10pC6 L6pC15 L4pC22 L11pC3 L5pC8 L13pC1 L8pC9 L5pC5 L2pC5 L13pC14 L12pC22 L13pC16')
    lp2 = Productos()
    lp2.insertar_producto('tv smart lcd', 'L1pC1p L2pC2p')
    listap = ListaDeProductos()
    listap.aniadir_lista_de_productos(lp)
    listap.aniadir_lista_de_productos(lp2)
    # listap.mostar_lista_de_productos()
    # listap.obtener_producto_por_nombre('smartwatch')
    listap.graficar_cola_de_un_producto('smartwatch')