from abc import abstractmethod
import numpy as np
import pandas as pd



class Relacion():

    @abstractmethod
    def es_relacion_valida(self, datos: pd.DataFrame) -> bool:
        pass
    
    @abstractmethod
    def procesar_relacion(self, datos: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        pass
        
    
    def es_numerico(self, datos: pd.DataFrame) -> bool:
        for col in datos.columns:
            if not pd.api.types.is_numeric_dtype(datos[col]):
                return False
        return True
    
    
    
class Dicotomica(Relacion):
    
    def _get_unique_set(self, datos: pd.DataFrame) -> list:
        unique_set = set()
        for col in datos.columns:
            unique_set = unique_set.union(set(datos[col].unique()))
        return list(unique_set)
    
    def es_relacion_valida(self, datos: pd.DataFrame) -> bool:  
        return len(self._get_unique_set(datos)) == 2
    
    def procesar_relacion(self, datos: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        values_set = self._get_unique_set(datos)
        
        
        if (values_set != [0, 1]):
            values_dict = dict()
            for i in range(len(values_set)):
                values_dict[values_set[i]] = i
        else:
            values_dict = {0: 0, 1: 1}
        
        return datos.map(lambda x: values_dict[x]), values_dict
        
        
class Clasificatoria(Relacion):
    
    generar_ranking: bool
    
    def __init__(self, generar_ranking: bool = True):
        self.generar_ranking = generar_ranking
        
    def turn_into_ranking(self, datos: pd.DataFrame) -> pd.DataFrame:
        return datos.rank(axis=0, method='first', numeric_only=True, ascending=True).astype(int)
           
    def _validar_es_ranking(self, datos: pd.DataFrame) -> bool:
        datos_rankeados = self.turn_into_ranking(datos)
        return (datos == datos_rankeados).all().all()
                  
    def es_relacion_valida(self, datos: pd.DataFrame) -> bool:
        return self.es_numerico(datos) and (self.generar_ranking or self._validar_es_ranking(datos))

    def procesar_relacion(self, datos: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        datos = self.turn_into_ranking(datos)
        return datos, {}
    
    
class Evaluativa(Relacion):
    
    interval_max: int
    
    def __init__(self, max_value: int):
        self.interval_max = max_value
        
    def es_relacion_valida(self, datos: pd.DataFrame) -> bool:
        return self.es_numerico(datos)
    
    def procesar_relacion(self, datos: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        min_val = datos.min().min()
        max_val = datos.max().max()
        datos = datos.map(lambda x: np.floor(1 + (x - min_val) * (self.interval_max - 1) / (max_val - min_val)).astype(int))
        return datos, {"interval_max": self.interval_max, "min_val": min_val, "max_val": max_val}