# MLOps-Henry
Proyecto I Henry
=======
readme_content = """
# Proyecto de Recomendación de Videojuegos

## Introducción

Para este proyecto desarrollo un sistema de recomendación de videojuegos en la plataforma Steam. La tarea consiste en partir desde en cero la limpieza y ordenamiento de los datos y actuar ágilmente como Data/ML Engineer para lograr un Producto Mínimo Viable y aprobar el proyecto I de Henry

## Extracción, Transformación y Carga (ETL)


Se desanidaron datasets JSON para facilitar la manipulación de datos, identificando columnas que necesitaban desanidamiento adicional y se guardaron en archivos csv. Así mismo, se gestionaron los datos eliminando columnas innecesarias y eliminando filas con datos nulos.Se simplificaron los campos de fecha al extraer solo el año y se creó una nueva columna con esta información y se creó una nueva columna llamada 'sentiment_analysis' mediante análisis de sentimiento utilizando procesamiento de lenguaje natural (NLP).



## Análisis Exploratorio de Datos (EDA)

Durante el proceso de Exploración de Datos (EDA), llevamos a cabo análisis detallados y evaluaciones específicas para comprender a fondo las relaciones intrínsecas entre los diferentes conjuntos de datos. Nuestro objetivo principal fue identificar patrones significativos que pudieran influir en el diseño y la implementación de las funciones, proporcionando así una comprensión profunda de la naturaleza de los datos esenciales para el modelo de recomendación. Exploramos minuciosamente las interconexiones entre las variables clave y examinamos detalladamente cómo estas relaciones podrían influir en la calidad y eficacia del modelo resultante. Este análisis profundo proporcionó información crucial para la toma de decisiones informadas y el diseño óptimo de las funciones del proyecto.

## Desarrollo API con FastAPI

Se propone la disponibilización de datos mediante FastAPI con funciones que permiten consultas específicas tales como
### 1. Playtime por Género

- **Descripción**: Obtiene el año con más horas jugadas para un género específico.
- **Ejemplo de uso**: `Action`, `Indie`, `Casual`, `Simulation`

### 2. Usuario con Más Horas Jugadas por Género

- **Descripción**: Retorna el usuario que ha acumulado más horas jugadas para un género dado y la cantidad total de horas jugadas.
- **Ejemplo de uso**: `Action`, `Indie`, `Casual`, `Simulation`

### 3. Juegos Más Recomendados por Usuarios

- **Descripción**: Devuelve el top 3 de juegos más recomendados por usuarios para un año determinado.
- **Ejemplo de uso**: `2022`, `2023`, ...

### 4. Juegos Menos Recomendados por Usuarios

- **Descripción**: Obtiene el top 3 de juegos menos recomendados por usuarios para un año específico.
- **Ejemplo de uso**: `2022`, `2023`, ...

### 5. Análisis de Sentimiento por Año

- **Descripción**: Proporciona una lista con la cantidad de reseñas de usuarios categorizadas con análisis de sentimiento para un año de lanzamiento determinado.
- **Ejemplo de uso**: `2022`, `2023`, ...

...

## Modelos de Recomendación

### 1. Recomendación de Juego Similar

- **Descripción**: Proporciona una lista con 5 juegos recomendados similares al ingresado.
- **Uso**: Ingresar el ID del juego como parámetro.
- **Ejemplo de ID para usar**: `761140`, `643980`, `670290`, `767400`

### 2. Recomendación de Juegos para Usuario

- **Descripción**: Obtiene una lista con 5 juegos recomendados para un usuario específico.
- **Uso**: Ingresar el ID del usuario como parámetro.
- **Ejemplo de ID para usar**: `evcentric`, `doctr`

- 

"""


