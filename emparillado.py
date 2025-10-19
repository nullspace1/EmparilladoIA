from typing import Type
import numpy as np
import pandas as pd

from relacion import Relacion
from nodo import Nodo
from arbol import Arbol
from tqdm import tqdm


class Emparillador():
    
    datos: pd.DataFrame
    metadata: dict
    relacion: Relacion
    
    def __init__(self, datos: pd.DataFrame, tipo_relacion: Relacion, label_points: bool = False) -> None:
        
        if datos.index.name in datos.columns:
            datos = datos.drop(columns=[datos.index.name])
        
        if not tipo_relacion.es_relacion_valida(datos):
            raise Exception("La relacion no es valida para el conjunto de datos propuesto")
        
        self.datos, self.metadata = tipo_relacion.procesar_relacion(datos)
        self.relacion = tipo_relacion
        self.label_points = label_points
        
    def clasificar_elementos(self) -> Arbol:
        
        arbol = [Nodo([x], 0, []) for x in range(self.datos.shape[0])]
        matriz = self._matriz_diferencias_elementos()
        arbol = self._generar_arbol(arbol, matriz)
        
        return Arbol("Elementos",arbol[0], self.datos.index, self.label_points)


    def clasificar_caracteristicas(self) -> Arbol:
        
        arbol = [Nodo([x], 0, []) for x in range(self.datos.shape[1])]
        matriz = self._matriz_diferencias_elementos()
        arbol = self._generar_arbol(arbol, matriz)
        
        return Arbol("Caracteristicas",arbol[0], self.datos.columns, self.label_points)
        
    def _generar_arbol(self, arbol, matriz):
        from tqdm import tqdm
        
        for _ in tqdm(range(len(arbol)-1), desc="Reduciendo arbol"):
            arbol = self._reducir_arbol(arbol, matriz)
        return arbol

    def _matriz_diferencias_elementos(self) -> np.ndarray:
        
        n = self.datos.shape[0]
        matriz = np.zeros((n, n))
        
        for i in tqdm(range(n), desc="Generando matriz"):
            for j in range(i+1, n):
                matriz[i][j] = np.sum(np.abs(self.datos.iloc[i] - self.datos.iloc[j]))
                matriz[j][i] = matriz[i][j]
                
        return matriz
    
    def _matriz_diferencias_caracteristicas(self) -> np.ndarray:
        
        n = self.datos.shape[1]
        matriz_aux = np.zeros((n, n))
        matriz = np.zeros((n, n))
        
        inverted_datos = self.datos.max().max() - self.datos + self.datos.min().min()
         
        for i in range(n):
            for j in range(i+1, n):
                matriz_aux[i][j] = np.sum(np.abs(self.datos.iloc[i] - self.datos.iloc[j]))
                matriz_aux[j][i] = np.sum(np.abs(inverted_datos.iloc[i] - self.datos.iloc[j]))
                
        for i in range(n):
            for j in range(i+1, n):
                matriz[i][j] = min(matriz_aux[i][j], matriz_aux[j][i])
                matriz[j][i] = matriz[i][j]
                        
        return matriz
    
    def _comparar_nodos(self, nodo1, nodo2, matriz: np.ndarray):
    
        
        nodo_pairs = [(v1, v2, matriz[v1][v2]) for v1 in nodo1.elementos for v2 in nodo2.elementos]
        nodo_pairs.sort(key=lambda x: x[2])

        return nodo_pairs[0][2]
        

    def _reducir_arbol(self, arbol: list[Nodo], matriz: np.ndarray) -> list[Nodo]:
        
        nodos_pairs = [(arbol[i], arbol[j], self._comparar_nodos(arbol[i], arbol[j], matriz)) for i in range(len(arbol)) for j in range(1, len(arbol)) if i < j]
        nodos_pairs.sort(key=lambda x: x[2])
        
        nodo1 = nodos_pairs[0][0]
        nodo2 = nodos_pairs[0][1]
        valor = nodos_pairs[0][2]
        
        
        arbol.remove(nodo1)
        arbol.remove(nodo2)
        
        
        if nodo1.valor == valor or nodo2.valor == valor:
            h1 = nodo1.hijos if len(nodo1.hijos) > 0 else [nodo1]
            h2 = nodo2.hijos if len(nodo2.hijos) > 0 else [nodo2]
            n = Nodo(nodo1.elementos + nodo2.elementos, valor, h1 + h2) 
        else:
            n = Nodo(nodo1.elementos + nodo2.elementos, valor, [nodo1, nodo2])
            
        arbol.append(n)
        return arbol