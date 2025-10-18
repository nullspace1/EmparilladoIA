import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relacion import Relacion, Dicotomica, Clasificatoria, Evaluativa

class TestDicotomica(unittest.TestCase):
    
    def setUp(self):
        
        self.datos_dicotomica_numerico = pd.DataFrame({
            'A': [0, 1, 1, 0],
            'B': [1, 0, 1, 0],
            'C': [1, 0, 1, 1]
        })

        self.datos_dicotomica_texto = pd.DataFrame({
            'A': ['yes','no','yes','no'],
            'B': ['yes','yes','no','no'],
            'C': ['yes','yes','yes','no']
        })
        
        self.datos_relaciones_invalida = [pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, 4, 5, 6]
        }), pd.DataFrame({
            'A': ['yes','yes','yes','yes'],
            'B': ['yes','yes','yes','no'],
            'C': ['yes','yes','oui','non']
        })]

        self.dicotomica = Dicotomica()
    
    def tearDown(self):
        pass
    
    def test_es_relacion_valida_numerico(self):
        self.assertTrue(self.dicotomica.es_relacion_valida(self.datos_dicotomica_numerico))
    
    def test_es_relacion_valida_texto(self):
        self.assertTrue(self.dicotomica.es_relacion_valida(self.datos_dicotomica_texto))
    
    def test_es_relacion_invalida(self):
        for datos in self.datos_relaciones_invalida:
            self.assertFalse(self.dicotomica.es_relacion_valida(datos))

    def test_procesar_relacion_numerico(self):
        
        datos, dict_valores = self.dicotomica.procesar_relacion(self.datos_dicotomica_numerico)
        self.assertEqual(datos['A'].tolist(), [0, 1, 1, 0])
        self.assertEqual(dict_valores, {0: 0, 1: 1})
        
    def test_procesar_relacion_texto(self):
        
        datos, dict_valores = self.dicotomica.procesar_relacion(self.datos_dicotomica_texto)
        self.assertTrue(
            (datos['A'].tolist() == [1, 0, 1, 0] and dict_valores == {'yes': 1, 'no': 0}) or 
            (datos['A'].tolist() == [0, 1, 0, 1] and dict_valores == {'yes': 0, 'no': 1})
        )
        
        
class TestClasificatoria(unittest.TestCase):
    
    def setUp(self):
        self.datos_clasificatoria_numerico = pd.DataFrame({
            'A': [0.4, 0.3, 0.2, 0.1],
            'B': [0.3, 0.2, 0.1, 0.4],
            'C': [0.2, 0.1, 0.4, 0.3]
        })
        
        self.datos_clasificatoria_ranking = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [4, 3, 2, 1],
            'C': [1, 2, 3, 4]
        })
        
        self.datos_clasificatoria_ranking_invalida = [pd.DataFrame({
            'A': [1, 3, 3, 4],
            'B': [4, 3, 2, 1],
            'C': [1, 2, 3, 4]
        }), pd.DataFrame({
            'A': [1, 2, 3, 5],
            'B': [4, 3, 2, 1],
            'C': [1, 2, 3, 4]
        })]
        
        self.clasificatoria_with_ranking = Clasificatoria(generar_ranking=True)
        self.clasificatoria_without_ranking = Clasificatoria(generar_ranking=False)
        
    def tearDown(self):
        pass
    
    def test_es_relacion_valida_numerico(self):
        self.assertTrue(self.clasificatoria_with_ranking.es_relacion_valida(self.datos_clasificatoria_numerico))
        
    def test_es_relacion_valida_ranking(self):
        self.assertTrue(self.clasificatoria_without_ranking.es_relacion_valida(self.datos_clasificatoria_ranking))
        
    def test_es_relacion_invalida(self):
        for datos in self.datos_clasificatoria_ranking_invalida:
            self.assertFalse(self.clasificatoria_without_ranking.es_relacion_valida(datos))
            
class TestEvaluativa(unittest.TestCase):
    
    def setUp(self):
        self.datos_evaluativa_numerico = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, 4, 5, 6]
        })
        
        self.datos_evaluativa_invalida = [pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 5],
            'C': [3, '2', 5, 6]
        }), pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [2, 3, 4, 'bad_value'],
            'C': [3, 4, 5, 6]
        })]
        
        self.evaluativa = Evaluativa(max_value=5)
        
    def tearDown(self):
        pass
    
    def test_es_relacion_valida_numerico(self):
        self.assertTrue(self.evaluativa.es_relacion_valida(self.datos_evaluativa_numerico))
        
    def test_es_relacion_invalida(self):
        for datos in self.datos_evaluativa_invalida:
            self.assertFalse(self.evaluativa.es_relacion_valida(datos))
            
    def test_procesar_relacion_numerico(self):
        datos, dict_valores = self.evaluativa.procesar_relacion(self.datos_evaluativa_numerico)
        self.assertEqual(datos['A'].tolist(), [1, 1, 2, 3])
        self.assertEqual(dict_valores, {"interval_max": 5, "min_val": 1, "max_val": 6})
        
        
if __name__ == '__main__':
    unittest.main()
    