from linea_produccion import *
from producto import *
from cola import *
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import random
from simulacion import *

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
    
    def obtener_componente_maximo(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.productos:
                cola = ListaSimple()
                if i.get_nombre() == nombre:
                    resultado = re.sub("L[0-9]+p?C", '',str(i.get_elaboracion()))
                    numero_componente = re.split(' ', resultado)
                    max_com = max(numero_componente, key=int)
            tmp = tmp.siguiente
        return int(max_com)
    
    def generar_archivo_de_simulacion_individual(self, nombre):
        tmp = self.inicio
        while tmp is not None:
            for i in tmp.productos:
                if i.get_nombre() == nombre:
                    print('nombre: '+str(i.get_nombre())+' Linea de elaboracion: '+str(i.get_elaboracion()))
                    
                    #Desde esta tabulacion debe ir el minidom
                    document = minidom.Document()
                    root = document.createElement("SalidaSimulacion")
                    
                    nombre_simulacion = document.createElement("Nombre")
                    nombre_simulacion.appendChild(document.createTextNode("Simulacion_"+str(i.get_nombre())))
                    root.appendChild(nombre_simulacion)
                    
                    listado_productos = document.createElement("ListadoProductos")
                    root.appendChild(listado_productos)
                    
                    
                    producto = document.createElement("Producto")
                    listado_productos.appendChild(producto)
                    
                    nombre_producto = document.createElement("Nombre")
                    nombre_producto.appendChild(document.createTextNode(str(i.get_nombre())))
                    producto.appendChild(nombre_producto)
                    
                    tiempo_total = document.createElement("TiempoTotal")
                    tiempo_total.appendChild(document.createTextNode(str(random.randint(70, 120))))
                    producto.appendChild(tiempo_total)
                    
                    elaboracion_optima = document.createElement("ElaboracionOptima")
                    producto.appendChild(elaboracion_optima)
                    
                    tiempo = document.createElement("Tiempo")
                    tiempo.setAttribute("NoSegundo", "1")
                    elaboracion_optima.appendChild(tiempo)
                    
                    linea_de_ensamblaje = document.createElement("LineaEnsamblaje")
                    linea_de_ensamblaje.setAttribute("NoLinea", "1")
                    linea_de_ensamblaje.appendChild(document.createTextNode("   "))
                    tiempo.appendChild(linea_de_ensamblaje)
                    
                    xml_str = root.toprettyxml(indent="\t")
                    save_path_file="Simulacion_"+str(i.get_nombre())+".xml"
                    
                    with open(save_path_file, "w") as f:
                        f.write(xml_str)
                    
                    
                    
                    
                    
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

from tkinter import *
from functools import partial
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import messagebox
from  tkinter import ttk


matriz_maquina = Maquina()
drop_down = list()
simulacion = LKSimulacion()

filename = ''
def cargar_datos_de_archivo_a_objeto_maquina():
    Tk().withdraw()
    global filename
    
    filename = askopenfilename()
    
    tree = ET.parse(filename)
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
            drop_down.append(str(nombre.strip()))
            lista_de_productos.insertar_producto(nombre.strip(), elaboracion.strip())
        matriz_maquina.aniadir_listas_a_la_maquina(cantidad_lineas_produccion, lista_lineas_produccion, lista_de_productos)
    mostrar_menu()




fsimulacion = ''
def cargar_archivo_simulacion():
    
    Tk().withdraw()
    global fsimulacion
    
    fsimulacion = askopenfilename()
    
    tree = ET.parse(fsimulacion)
    root = tree.getroot()
    
    for elemento in root:
        nombre_simulacion = elemento.text
        lista_de_productos_simular = LKProducto()
        
        for subelement in elemento.iter('ListadoProductos'):
            producto_nombre = subelement.find('Producto').text
            lista_de_productos_simular.aniadir_productos_a_simular(producto_nombre.strip())
        simulacion.aniadir_lista_a_simular(nombre_simulacion.strip(), lista_de_productos_simular)
    mostra_btn()


def graficar_cola_de_elaboracion(nombre):
    clicked()
    matriz_maquina.graficar_cola_de_un_producto(nombre)


def reporte_en_html():
    clicked()
    componente_maximo = matriz_maquina.obtener_componente_maximo(seleccion)
    
    
    texto = """
    <html>
        <head>
            <title>Reporte de producto</title>
            <meta charset="utf-8">
            <meta name="Author" content="https://github.com/pablorgarcia" />
            <meta name="description" content="Table Responsive" />
            <meta name="keywords" content="table, responsive" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <link href="table-responsive.css" media="screen" type="text/css" rel="stylesheet" />
        </head>
        <body>
        <h1><span class="blue"></span>Reporte<span class="blue"></span> <span class="yellow"> """+str(seleccion)+"""</pan></h1>
        <table class="container">
            <thead>
                <tr>
                    <th>Tiempo</th>
                    <th>Movimiento</th>
                </tr>
            </thead>
            <tbody>"""
    numeros = 1
    for i in range(componente_maximo):
        texto = texto + """<tr><td>"""+str(numeros)+"""</td><td> Mover brazo a Componente """+str(i+1)+"""</td></tr>"""
        numeros = numeros + 1
    texto2="""
                    </tbody>
                    </table>

                    </body>
                    </html>"""
    texto = texto + texto2
    file = open(str(seleccion).strip()+".html" ,mode='w', encoding='utf-8')
    file.write(texto)
    file.close()

root = Tk()
root.geometry('600x405')
root.title("Digital Intelligence, S. A.")
root.iconbitmap('mind.ico')
#------
menubar = Menu(root)


terminado = Label(root, text="")
terminado.place(x=260, y=330)
root.config(menu=menubar)

seleccion = ''
def obtener_opcion_del_menu(variable):
    global seleccion
    print(variable.get())
    seleccion = variable.get()
    mostrar_componentes()
    mostra_tabla()
    matriz_maquina.generar_archivo_de_simulacion_individual(str(seleccion))
    

def printSeleccion():
    print(seleccion)
    graficar_cola_de_elaboracion(seleccion)

process = 0


def clicked():
    pgbar = Progressbar(root,length=450,orient=HORIZONTAL,maximum = 100,value = 0,mode= 'determinate')
    pgbar.place(x=100, y=305)
    global process
    if process == pgbar['maximum']:
        terminado['text'] = ""
        process = 0
        pgbar['value'] = 0
    process += 10
    pgbar['value'] = process
    terminado['text'] = str(process) + "%"
    if pgbar['value'] >= pgbar['maximum']:
        terminado['text'] = "100% completado"
        return
    root.after(100, clicked)



def mostrar_componentes():
    
    clicked()
    componente_maximo = matriz_maquina.obtener_componente_maximo(seleccion)
    pcom = Label(root, text="Lista de componentes")
    pcom.place(x=150, y=60)
    Lb1 = Listbox(root)
    for i in range(componente_maximo):
        Lb1.insert((i+1), "Componente "+str(i+1))

    Lb1.place(x=150, y=80)

def mostrar_menu():
    global variable
    variable = StringVar(root)
    variable.set('Escoja un producto')

    w = OptionMenu(root, variable, *drop_down)
    B = Button(root, text ="Simular", command = partial(obtener_opcion_del_menu, variable), width = 10)
    
    w.place(x=20, y=10)
    B.place(x= 20, y=40)



def mostra_btn():
    Btn = Button(root, text ="Simulacion\nmasiva", width = 12)
    Btn.place(x=22, y=63)


def print_info():
    messagebox.showinfo(message="Hector Ponsoy\nIPC2 2S 2021", title="Informacion")

def print_acercade():
    messagebox.showinfo(message="Versión: 1.60.0 (user setup)\nConfirmación: e7d7e9a9348\nFecha: 2021-09-01T10:41:52.311Z\nChrome: 91.0.4472.164\nSistema Operativo: Windows_NT x64 10.0.19043", title="Acerca de")


filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Archivo maquina", command=cargar_datos_de_archivo_a_objeto_maquina)
filemenu.add_command(label="Archivo de simulacion", command=cargar_archivo_simulacion)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)

reportmenu = Menu(menubar, tearoff=0)
reportmenu.add_command(label="Reporte de colas", command=printSeleccion)
reportmenu.add_command(label="Reporte HTML", command=reporte_en_html)

infomenu = Menu(menubar, tearoff=0)
infomenu.add_command(label="Informacion", command=print_info)
infomenu.add_separator()
infomenu.add_command(label="Acerca de...", command=print_acercade)

menubar.add_cascade(label="Archivos", menu=filemenu)
menubar.add_cascade(label="Reportes", menu=reportmenu)
menubar.add_cascade(label="Ayuda", menu=infomenu)

#---------------------


def mostra_tabla():
    componente_maximo = matriz_maquina.obtener_componente_maximo(seleccion)
    ptabla = Label(root, text="Tabla de procesos")
    ptabla.place(x=375, y=20)
    table_frame = Frame(root)
    table_frame.place(x=350, y=40)

    table_scrollbarV = Scrollbar(table_frame, orient='vertical')
    table_scrollbarV.pack(side=RIGHT, fill=Y)

    table_scrollbarH = Scrollbar(table_frame,orient='horizontal')
    table_scrollbarH.pack(side= BOTTOM,fill=X)

    my_table = ttk.Treeview(table_frame,yscrollcommand = table_scrollbarV.set,xscrollcommand = table_scrollbarH.set)

    my_table.pack()

    table_scrollbarV.config(command=my_table.yview)
    table_scrollbarH.config(command=my_table.xview)

    my_table['columns'] = ('_tiempo', '_movimiento')

    my_table.column("#0", width=0,  stretch=NO)
    my_table.column("_tiempo",anchor=CENTER, minwidth = 100, width=80)
    my_table.column("_movimiento",anchor=CENTER,minwidth = 100, width=80)

    my_table.heading("_tiempo",text="Tiempo",anchor=CENTER)
    my_table.heading("_movimiento",text="Movimiento",anchor=CENTER)


    for i in range(componente_maximo):
        my_table.insert(parent='',index='end',iid=i,text='',values=(str(i + 1),'mover brazo a C'+str(i + 1)))
    my_table.pack()





    
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
    # cargar_datos_de_archivo_a_objeto_maquina()
    # matriz_maquina.mostrar_todas_los_datos_de_mi_maquina()
    
    root.mainloop()
    # matriz_maquina.obtener_producto_por_nombre('Barbie')
    # graficar_cola_de_elaboracion('Barbie')

    # print(matriz_maquina.obtener_componente_maximo('Barbie'))
    # cargar_archivo_simulacion()
    # simulacion.generar_archivo_de_simulacion_masiva()
    
    
    
    
    
    
