class NodoLineaProduccion():
    def __init__(self, numero, cantidad_componentes, tiempo_ensamblaje):
        self.numero = numero
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.anterior = None
        self.siguiente = None
    
    def get_numero(self):
        return self.numero
    
    def get_cantidad_componentes(self):
        return self.cantidad_componentes
    
    def get_tiempo_ensamblaje(self):
        return self.tiempo_ensamblaje
    
        

class LineaProduccion():
    def __init__(self):
        self.inicio = None
    
    def insertar_linea_de_produccion(self, numero, cantidad_componentes, tiempo_ensamblaje):
        nuevo = NodoLineaProduccion(numero, cantidad_componentes, tiempo_ensamblaje)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp 
    
    def mostrar_lineas_de_produccion(self):
        tmp = self.inicio
        while tmp is not None:
            print('numero: ', tmp.numero,'Cantidad de componentes: ', tmp.cantidad_componentes,'Tiempo de ensamblaje: ', tmp.tiempo_ensamblaje)
            tmp = tmp.siguiente
    
    def __iter__(self):
        tmp = self.inicio
        while tmp:
            yield tmp
            tmp = tmp.siguiente
    

if __name__ == '__main__':
    ll = LineaProduccion()
    ll.insertar_linea_de_produccion(1, 5, 2)
    ll.mostrar_lineas_de_produccion()
    
    