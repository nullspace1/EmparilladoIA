import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relacion import Dicotomica, Clasificatoria, Evaluativa
from emparillado import Emparillador
from arbol import Arbol
from nodo import Nodo


class TestEmparillador(unittest.TestCase):
    
    def setUp(self):
        
        self.datos_dicotomica = pd.DataFrame({
            'A': [0, 1, 1, 0],
            'B': [1, 0, 1, 0],
            'C': [1, 0, 1, 1]
        })
        
        self.datos_clasificatoria = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, 4, 5, 6]
        })
        
        self.datos_evaluativa = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, 4, 5, 6]
        })
        
        self.datos_invalidos = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 'invalid'],
            'C': [3, 4, 5, 6]
        })
        
        self.datos_con_indices = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, 4, 5, 6]
        })
        self.datos_con_indices.index = ['elem1', 'elem2', 'elem3', 'elem4']
        
        self.dicotomica = Dicotomica()
        self.clasificatoria = Clasificatoria(generar_ranking=True)
        self.evaluativa = Evaluativa(max_value=5)
    
    def tearDown(self):
        pass
    
    def test_init_dicotomica_valida(self):
        emparillador = Emparillador(self.datos_dicotomica, self.dicotomica)
        self.assertIsNotNone(emparillador.datos)
        self.assertIsNotNone(emparillador.relacion)
        self.assertIsNotNone(emparillador.metadata)
    
    def test_init_clasificatoria_valida(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        self.assertIsNotNone(emparillador.datos)
        self.assertIsNotNone(emparillador.relacion)
        self.assertIsNotNone(emparillador.metadata)
    
    def test_init_evaluativa_valida(self):
        emparillador = Emparillador(self.datos_evaluativa, self.evaluativa)
        self.assertIsNotNone(emparillador.datos)
        self.assertIsNotNone(emparillador.relacion)
        self.assertIsNotNone(emparillador.metadata)
    
    def test_init_con_indices(self):
        emparillador = Emparillador(self.datos_con_indices, self.evaluativa)
        self.assertEqual(emparillador.datos.index.tolist(), ['elem1', 'elem2', 'elem3', 'elem4'])
    
    def test_init_datos_invalidos(self):
        with self.assertRaises(Exception):
            Emparillador(self.datos_invalidos, self.evaluativa)
    
    def test_clasificar_elementos_dicotomica(self):
        emparillador = Emparillador(self.datos_dicotomica, self.dicotomica)
        arbol = emparillador.clasificar_elementos()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 4)
        self.assertEqual(arbol.indices.tolist(), [0, 1, 2, 3])
    
    def test_clasificar_elementos_clasificatoria(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        arbol = emparillador.clasificar_elementos()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 4)
    
    def test_clasificar_elementos_evaluativa(self):
        emparillador = Emparillador(self.datos_evaluativa, self.evaluativa)
        arbol = emparillador.clasificar_elementos()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 4)
    
    def test_clasificar_caracteristicas_dicotomica(self):
        emparillador = Emparillador(self.datos_dicotomica, self.dicotomica)
        arbol = emparillador.clasificar_caracteristicas()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 3)
        self.assertEqual(arbol.indices.tolist(), ['A', 'B', 'C'])
    
    def test_clasificar_caracteristicas_clasificatoria(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        arbol = emparillador.clasificar_caracteristicas()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 3)
    
    def test_clasificar_caracteristicas_evaluativa(self):
        emparillador = Emparillador(self.datos_evaluativa, self.evaluativa)
        arbol = emparillador.clasificar_caracteristicas()
        
        self.assertIsInstance(arbol, Arbol)
        self.assertIsInstance(arbol.nodo, Nodo)
        self.assertEqual(len(arbol.indices), 3)
    
    def test_matriz_diferencias_elementos(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        matriz = emparillador._matriz_diferencias_elementos()
        
        self.assertIsInstance(matriz, np.ndarray)
        self.assertEqual(matriz.shape, (4, 4))
        self.assertTrue(np.all(np.diag(matriz) == 0))
    
    def test_matriz_diferencias_caracteristicas(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        matriz = emparillador._matriz_diferencias_caracteristicas()
        
        self.assertIsInstance(matriz, np.ndarray)
        self.assertEqual(matriz.shape, (3, 3))
        self.assertTrue(np.all(np.diag(matriz) == 0))
    
    def test_comparar_nodos(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        matriz = emparillador._matriz_diferencias_elementos()
        
        nodo1 = Nodo([0], 0, [])
        nodo2 = Nodo([1], 0, [])
        
        distancia = emparillador._comparar_nodos(nodo1, nodo2, matriz)
        self.assertIsInstance(distancia, (int, float))
        self.assertGreaterEqual(distancia, 0)
    
    def test_reducir_arbol(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        matriz = emparillador._matriz_diferencias_elementos()
        
        arbol_inicial = [Nodo([i], 0, []) for i in range(4)]
        arbol_reducido = emparillador._reducir_arbol(arbol_inicial, matriz)
        
        self.assertIsInstance(arbol_reducido, list)
        self.assertEqual(len(arbol_reducido), 3)
        self.assertTrue(all(isinstance(nodo, Nodo) for nodo in arbol_reducido))
    
    def test_generar_arbol(self):
        emparillador = Emparillador(self.datos_clasificatoria, self.clasificatoria)
        matriz = emparillador._matriz_diferencias_elementos()
        
        arbol_inicial = [Nodo([i], 0, []) for i in range(4)]
        arbol_final = emparillador._generar_arbol(arbol_inicial, matriz)
        
        self.assertIsInstance(arbol_final, list)
        self.assertEqual(len(arbol_final), 1)
        self.assertIsInstance(arbol_final[0], Nodo)


class TestEmparilladorIntegracion(unittest.TestCase):
    
    def setUp(self):
        
        self.datos_grandes = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 3, 4, 5, 6],
            'C': [3, 4, 5, 6, 7],
            'D': [4, 5, 6, 7, 8]
        })
        
        self.datos_pequenos = pd.DataFrame({
            'A': [1, 2],
            'B': [2, 3]
        })
        
        self.clasificatoria = Clasificatoria(generar_ranking=True)
    
    def tearDown(self):
        pass
    
    def test_clasificacion_completa_elementos(self):
        emparillador = Emparillador(self.datos_grandes, self.clasificatoria)
        
        arbol_elementos = emparillador.clasificar_elementos()
        
        self.assertIsInstance(arbol_elementos, Arbol)
        self.assertEqual(len(arbol_elementos.indices), 5)
        self.assertTrue(all(i in arbol_elementos.indices for i in range(5)))
    
    def test_clasificacion_completa_caracteristicas(self):
        emparillador = Emparillador(self.datos_grandes, self.clasificatoria)
        
        arbol_caracteristicas = emparillador.clasificar_caracteristicas()
        
        self.assertIsInstance(arbol_caracteristicas, Arbol)
        self.assertEqual(len(arbol_caracteristicas.indices), 4)
        self.assertTrue(all(col in arbol_caracteristicas.indices for col in ['A', 'B', 'C', 'D']))
    
    def test_datos_pequenos(self):
        emparillador = Emparillador(self.datos_pequenos, self.clasificatoria)
        
        arbol_elementos = emparillador.clasificar_elementos()
        arbol_caracteristicas = emparillador.clasificar_caracteristicas()
        
        self.assertIsInstance(arbol_elementos, Arbol)
        self.assertIsInstance(arbol_caracteristicas, Arbol)
        self.assertEqual(len(arbol_elementos.indices), 2)
        self.assertEqual(len(arbol_caracteristicas.indices), 2)


if __name__ == '__main__':
    unittest.main()