import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from lista_enlazada import ListaEnlazada
import zipfile
import requests

class RecomendadorPeliculas:
    def __init__(self):
        self.lista_peliculas = ListaEnlazada()

    def cargar_datos(self):
        # Descargar y descomprimir el dataset de MovieLens
        url = 'https://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
        r = requests.get(url)
        with open('ml-latest-small.zip', 'wb') as f:
            f.write(r.content)

        with zipfile.ZipFile('ml-latest-small.zip', 'r') as zip_ref:
            zip_ref.extractall('ml-latest-small')

        # Leer el archivo 'movies.csv'
        movielens = pd.read_csv('ml-latest-small/ml-latest-small/movies.csv', usecols=['title', 'genres'])
        movielens['description'] = movielens['genres'].apply(lambda x: ' '.join(x.split('|')))
        self.data = movielens

    def entrenar_modelo(self):
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.data['description'])
        self.similitudes = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def recomendar(self, genero):
        try:
            peliculas_genero = self.data[self.data['genres'].str.contains(genero, case=False)]
            print(f"Películas encontradas para el género {genero}: {len(peliculas_genero)}")
            idxs = peliculas_genero.index
            simil_scores = []

            for idx in idxs:
                simil_scores += list(enumerate(self.similitudes[idx]))

            simil_scores = sorted(simil_scores, key=lambda x: x[1], reverse=True)
            recomendadas = []

            for i in simil_scores:
                if len(recomendadas) >= 3:  # Generar hasta 3 recomendaciones
                    break
                if self.data['title'].iloc[i[0]] not in peliculas_genero['title'].values:
                    recomendadas.append(self.data['title'].iloc[i[0]])
                    self.lista_peliculas.insertar(self.data['title'].iloc[i[0]])  # Agregar a la lista enlazada

            print(f"Recomendaciones generadas: {len(recomendadas)}")
            return recomendadas
        except Exception as e:
            print(f"Error al generar recomendaciones para el género {genero}: {e}")
            return []

    def mostrar_generos(self):
        generos = set()
        for gen in self.data['genres']:
            for g in gen.split('|'):
                generos.add(g)
        return list(generos)

def main():
    recomendador = RecomendadorPeliculas()
    print("Cargando datos...")
    recomendador.cargar_datos()
    print("Datos cargados. Entrenando modelo...")
    recomendador.entrenar_modelo()
    print("Modelo entrenado.")

    while True:
        # Mostrar los géneros disponibles
        generos = recomendador.mostrar_generos()
        print("\nGéneros disponibles:")
        for idx, genero in enumerate(generos):
            print(f"{idx + 1}. {genero}")

        # Permitir al usuario seleccionar un género
        try:
            opcion_usuario = int(input("\nSeleccione el número del género de su preferencia (o 0 para salir): "))
            if opcion_usuario == 0:
                print("Saliendo del sistema. ¡Hasta luego!")
                break
            elif 1 <= opcion_usuario <= len(generos):
                genero_usuario = generos[opcion_usuario - 1]
                print(f"Género seleccionado: {genero_usuario}")

                # Generar y mostrar recomendaciones
                recomendaciones = recomendador.recomendar(genero_usuario)
                print(f"\nRecomendaciones para el género '{genero_usuario}':")
                if not recomendaciones:
                    print("No se generaron recomendaciones.")
                else:
                    for pelicula in recomendaciones:
                        print(pelicula)

                # Mostrar recomendaciones almacenadas en la lista enlazada
                print("\nPelículas recomendadas almacenadas:")
                recomendador.lista_peliculas.mostrar_peliculas()
            else:
                print("Número de opción fuera de rango. Por favor, intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

if __name__ == "__main__":
    main()









