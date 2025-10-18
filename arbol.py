from nodo import Nodo
import matplotlib.pyplot as plt


class Arbol():
    
    nodo: Nodo
    indices: list
    nombre : str
    
    def __init__(self,nombre: str, nodo: Nodo, indices: list, label_points: bool = False):
        self.nombre = nombre
        self.nodo = nodo
        self.indices = indices
        self.label_points = label_points
    
    def plot(self):
        plt.figure(figsize=(10, 10))
        plt.title(f"Clasificacion de {self.nombre}")
        plt.xlabel("Elementos")
        plt.ylabel("Altura")
        self.nodo.plot(self.indices, self.label_points)
        plt.grid(True)
        plt.show()