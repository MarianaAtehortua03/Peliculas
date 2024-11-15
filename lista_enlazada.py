from nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def insertar(self, pelicula):
        nuevo_nodo = Nodo(pelicula)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def mostrar_peliculas(self):
        actual = self.cabeza
        while actual:
            print(actual.pelicula)
            actual = actual.siguiente


