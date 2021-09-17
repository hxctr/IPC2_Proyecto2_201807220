class NodoProducto():
    def __init__(self, nombre, cola_de_elaboracion):
        self.nombre = nombre
        self.cola_de_elaboracion = cola_de_elaboracion
        self.anterior = None
        self.siguiente = None
    
    def get_nombre(self):
        return self.nombre
    
    def get_elaboracion(self):
        return self.cola_de_elaboracion

class Productos():
    def __init__(self):
        self.inicio = None
    
    def insertar_producto(self, nombre, cola_de_elaboracion):
        nuevo = NodoProducto(nombre, cola_de_elaboracion)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while self.inicio is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def motrar_productos(self):
        tmp = self.inicio
        while tmp is not None:
            print('Nombre: ',tmp.nombre,' Cola de ensamblaje: ', tmp.cola_de_elaboracion)
            tmp = tmp.siguiente
    
    def __iter__(self):
        tmp = self.inicio
        while tmp:
            yield tmp
            tmp = tmp.siguiente

if __name__ == '__main__':
    pc = Productos()
    pc.insertar_producto('smartwatch', 'L2pC5 L10pC6 L6pC15 L4pC22 L11pC3 L5pC8 L13pC1 L8pC9 L5pC5 L2pC5 L13pC14 L12pC22 L13pC16')
    pc.motrar_productos()
    