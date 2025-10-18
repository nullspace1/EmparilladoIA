# Emparillado

Una librería de Python para clustering jerárquico y análisis de datos usando diferentes tipos de relaciones basado en la teoria de 'Emparillado'.

## Descripción General

La tecnica de emparillado proporciona herramientas para agrupar elementos y características usando varios tipos de relaciones incluyendo relaciones dicotómicas, clasificatorias y evaluativas. La librería implementa estos algoritmos de clustering jerárquicos para analizar patrones y relaciones en los datos.

## Características

- **Múltiples Tipos de Relaciones**: Soporte para relaciones dicotómicas, clasificatorias y evaluativas
- **Clustering Jerárquico**: Algoritmos de clustering integrados para elementos y características
- **Procesamiento Flexible de Datos**: Maneja diferentes tipos de datos incluyendo numéricos, categóricos y de ranking
- **Ranking Personalizable**: Opciones para generar rankings con diferentes métodos de desempate

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd Emparillado
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Uso Básico

```python
import pandas as pd
from Relacion import Dicotomica, Clasificatoria, Evaluativa
from emparillado import Emparillador

# Crear datos de ejemplo
data = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [2, 3, 4, 5],
    'C': [3, 4, 5, 6]
})

# Usar diferentes tipos de relaciones
dicotomica = Dicotomica()
clasificatoria = Clasificatoria(generar_ranking=True)
evaluativa = Evaluativa(max_value=5)

# Crear instancia del emparillador
emparillador = Emparillador(data, clasificatoria)

# Clasificar elementos
arbol_elementos = emparillador.clasificar_elementos()

# Clasificar características
arbol_caracteristicas = emparillador.clasificar_caracteristicas()
```

### Tipos de Relaciones

#### Dicotomica
Para datos binarios o dicotómicos:
```python
dicotomica = Dicotomica()
# Convierte automáticamente datos categóricos a valores numéricos (0,1) de ser necesario
```

#### Clasificatoria
Para datos de ranking y clasificación:
```python
clasificatoria = Clasificatoria(generar_ranking=True)
# Puede generar rankings o validar rankings existentes si ya esta en modo ranking
```

#### Evaluativa
Para datos evaluativos con intervalos definidos:
```python
evaluativa = Evaluativa(max_value=5)
# Normaliza datos al rango de intervalo especificado
```

## Estructura del Proyecto

```
Emparillado/
├── Arbol.py              # Estructura de árbol para resultados de clustering
├── Nodo.py               # Clase nodo para nodos del árbol
├── Relacion.py           # Definiciones de tipos de relaciones
├── emparillado.py        # Clase principal Emparillador
├── test/                 # Archivos de prueba
│   ├── test_relacion.py  # Pruebas para tipos de relaciones
│   └── test_emparillado.py # Pruebas para funcionalidad principal
├── requirements.txt      # Dependencias de Python
└── README.md            # Este archivo
```

## Pruebas

Ejecuta las pruebas usando unittest:

```bash
# Ejecutar todas las pruebas
python -m unittest discover test

# Ejecutar archivo de prueba específico
python test/test_relacion.py
python test/test_emparillado.py
```

## Dependencias

- **numpy**: Computación numérica
- **pandas**: Manipulación y análisis de datos
- **tqdm**: Barras de progreso para operaciones de larga duración
- **Matplotlib**: Plotting del arbol jerarquico de relaciones entre elementos / caracteristicas

## TODOs

Optimizar el proceso de creacion de la matriz de diferencia. El metodo naive actual creo que es $O(N^3)$, por lo que es _practicamente_ inutilizable para matrices grandes de $> 100$ elementos.

## Contribuciones

Catedra de Inteligencia Articial de la Universidad Tecnologica Nacional, Facultad Regional Buenos Aires

