from linea_produccion import *

class NodoListaLineasProduccion():
    def __init__(self, #numero, cantidad_componentes, tiempo_ensamblaje
                linea_de_produccion):
        self.linea_de_produccion = linea_de_produccion
        # self.numero = numero
        # self.cantidad_componentes = cantidad_componentes
        # self.tiempo_ensamblaje = tiempo_ensamblaje
        self.anterior = None
        self.siguiente = None

class ListaLineasProduccion():
    def __init__(self):
        self.inicio = None
    
    def aniadir_linea_de_produccion(self, lista_lineas_produccion):
        nuevo = NodoListaLineasProduccion(lista_lineas_produccion)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def mostrar_lista_lineas_de_produccion(self):
        tmp = self.inicio
        while tmp is not None:
            # print('numero: ', tmp.numero,'Cantidad de componentes: ',tmp.cantidad_componentes,'Tiempo de ensamblaje: ',tmp.tiempo_ensamblaje)
            tmp.linea_de_produccion.mostrar_lineas_de_produccion()
            tmp = tmp.siguiente
    
    def obtener_por_linea_de_ensamblaje(self, numero):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.linea_de_produccion:
                if i.get_numero() == numero:
                    print('numero: '+str(i.get_numero())+', Cantidad de componentes: '+str(i.cantidad_componentes)+', Tiempo de ensamblaje: '+str(i.tiempo_ensamblaje))
            tmp = tmp.siguiente
        return None

if __name__ == '__main__':
    ll = LineaProduccion()
    ll.insertar_linea_de_produccion(1, 5, 2)
    ll2 = LineaProduccion()
    ll2.insertar_linea_de_produccion(5, 3, 4)
    lp = ListaLineasProduccion()
    lp.aniadir_linea_de_produccion(ll)
    lp.aniadir_linea_de_produccion(ll2)
    lp.mostrar_lista_lineas_de_produccion()
    # lp.obtener_por_linea_de_ensamblaje(5)
    
    