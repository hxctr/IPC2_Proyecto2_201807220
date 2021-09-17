from archivos import *

class NodoCola():
    def __init__(self, siguiente, valor):
        self.setSiguiente(siguiente)
        self.setValor(valor)

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def setValor(self, valor):
        self.valor = valor

    def getSiguiente(self):
        return self.siguiente

    def getValor(self):
        return self.valor

class ListaSimple():
    dot = ""
    
    def __init__(self):
        self.inicio = None
        self.fin = None
    
    def estaVacia(self):
        return self.inicio == None
    
    def enqueue(self, valor):
        if self.estaVacia():
            self.inicio = self.fin = NodoCola(None, valor)
        else:
            self.fin = NodoCola(self.fin, valor)
    
    def graficar(self, nombre):
        global dot
        
        dot = "digraph grafico{\nnode [style = \"filled\" shape = \"box\"]\n"
        
        dot += "rankdir = \"LR\"\n"
        
        if not self.estaVacia():
            aux = self.fin
            while aux != None:
                if aux == self.inicio:
                    dot += "\"" + str(aux) + "\" [label = \"" + str(aux.valor) + "\" fillcolor = \"white\"]\n"
                elif aux == self.fin:
                    dot += "\"" + str(aux) + "\" [label = \"" + str(aux.valor) + "\" fillcolor = \"white\"]\n"
                else:
                    dot += "\"" + str(aux) + "\" [label = \"" + str(aux.valor) + "\" fillcolor = \"white\"]\n"
                if aux.getSiguiente() != None:
                    dot += "\"" + str(aux) + "\" -> \"" + str(aux.getSiguiente()) + "\"\n" 
                
                aux = aux.getSiguiente()
        dot += "}"

        graficar_cola(dot, nombre)

if __name__ == "__main__":
    cola = ListaSimple()
    cola.enqueue(5)
    cola.enqueue(10)
    cola.enqueue(20)
    cola.graficar('hola')
    
    
    