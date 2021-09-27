from xml.dom import minidom
import random
import xml.etree.ElementTree as ET

class nodoProducto():
    def __init__(self, producto):
        self.producto = producto
        self.anterior = None
        self.siguiente = None
    
    def get_producto(self):
        return self.producto

class LKProducto():
    def __init__(self):
        self.inicio = None
    
    def aniadir_productos_a_simular(self, producto):
        nuevo = nodoProducto(producto)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def __iter__(self):
        tmp = self.inicio
        while tmp:
            yield tmp
            tmp = tmp.siguiente

class NodoLKSimulacion():
    def __init__(self, nombre, productos):
        self.nombre = nombre
        self.productos = productos
        self.anterior = None
        self.siguiente = None

class LKSimulacion():
    def __init__(self):
        self.inicio = None
    
    def aniadir_lista_a_simular(self, nombre, productos):
        nuevo = NodoLKSimulacion(nombre, productos)
        if self.inicio is None:
            self.inicio = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
    
    def mostrar_datos_de_simulacion(self):
        tmp = self.inicio
        while tmp is not None:
            print(tmp.nombre)
            for i in tmp.productos:
                print(i.get_producto())
            tmp = tmp.siguiente
        return None
    
    def generar_archivo_de_simulacion_masiva(self):
        tmp = self.inicio
        while tmp is not None:
            document = minidom.Document()
            root = document.createElement("SalidaSimulacion")

            nombre_simulacion = document.createElement("Nombre")
            nombre_simulacion.appendChild(document.createTextNode("Simulacion_"))
            root.appendChild(nombre_simulacion)
            
            listado_productos = document.createElement("ListadoProductos")
            root.appendChild(listado_productos)
            
            producto = document.createElement("Producto")
            listado_productos.appendChild(producto)
            
            for i in tmp.productos:
                nombre_producto = document.createElement("Nombre")
                nombre_producto.appendChild(document.createTextNode(str(i.get_producto())))
                producto.appendChild(nombre_producto)
            
            for i in tmp.productos:
                tiempo_total = document.createElement("TiempoTotal")
                tiempo_total.appendChild(document.createTextNode(str(random.randint(70, 120))))
                producto.appendChild(tiempo_total)
            
            elaboracion_optima = document.createElement("ElaboracionOptima")
            producto.appendChild(elaboracion_optima)
            
            for i in tmp.productos:
                tiempo = document.createElement("Tiempo")
                tiempo.setAttribute("NoSegundo", i)
                elaboracion_optima.appendChild(tiempo)
            
            for i in tmp.productos:
                linea_de_ensamblaje = document.createElement("LineaEnsamblaje")
                linea_de_ensamblaje.setAttribute("NoLinea", i)
                linea_de_ensamblaje.appendChild(document.createTextNode("   "))
                tiempo.appendChild(linea_de_ensamblaje)
            
            xml_str = root.toprettyxml(indent="\t")
            save_path_file="Simulacion_.xml"
            
            with open(save_path_file, "w") as f:
                f.write(xml_str)
            
            tmp = tmp.siguiente
        return None

simulacion = LKSimulacion()

def cargar_archivo_simulacion():
    
    tree = ET.parse('simulacion.xml')
    root = tree.getroot()
    
    for elemento in root:
        nombre_simulacion = elemento.text
        
        lista_de_productos_simular = LKProducto()
        for subelement in elemento.iter('ListadoProductos'):
            producto_nombre = subelement.find('Producto').text
            lista_de_productos_simular.aniadir_productos_a_simular(producto_nombre.strip())
        simulacion.aniadir_lista_a_simular(nombre_simulacion.strip(), lista_de_productos_simular)
    print('pase aqui ya')




if __name__ == '__main__':
    # producto = LKProducto()
    # producto.aniadir_productos_a_simular('smartwatch')
    # producto.aniadir_productos_a_simular('watch')
    # producto.aniadir_productos_a_simular('computadora')
    # producto.aniadir_productos_a_simular('celular')
    # producto.aniadir_productos_a_simular('televisor')
    # listap = LKSimulacion()
    # listap.aniadir_lista_a_simular('nombre del file', producto)
    # listap.mostrar_datos_de_simulacion()
    cargar_archivo_simulacion()
    simulacion.mostrar_datos_de_simulacion()