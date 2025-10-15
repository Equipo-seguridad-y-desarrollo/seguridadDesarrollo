# Diccionario de Datos: Rezago Educativo por Estado

Este archivo describe las variables del conjunto de datos sobre el rezago educativo en las entidades federativas de México. Los datos provienen de estimaciones del INEA (Instituto Nacional para la Educación de los Adultos). Los datos se pueden encontrar en la carpeta rezago_educativo_consolidado,csv

##  estimacion de rezago educativo en mayores de 15 años del 2019 - 2024

- **Archivo fuente**: `rezago_educativo.csv`
- **Filas x columnas**: 204 filas × 19 columnas
- **Posibles columnas temporales**: Año
- **Posibles variables categóricas**: Entidad federativa

| Columna | Nombre de la Variable | Descripción | Tipo de Dato |
|---|---|---|---|
| 0 | `entidad_federativa` | Nombre de la entidad federativa. | Texto |
| 1 | `Población de 15 años y más` | Cifra total de la población de 15 años o más en la entidad. | Flotante |
| 2 | `Analfabetas` | Cifra absoluta de personas que no saben leer ni escribir. | Flotante |
| 3 | `Lugar` | Posición (ranking) de la entidad a nivel nacional en número de analfabetas. | Flotante |
| 4 | `%` | Porcentaje de la población de 15 años y más que es analfabeta. | Flotante |
| 5 | `Lugar.1` | Posición (ranking) de la entidad a nivel nacional por porcentaje de analfabetismo. | Flotante |
| 6 | `Sin primaria terminada` | Cifra absoluta de personas que no completaron la educación primaria. | Flotante |
| 7 | `Lugar.2` | Posición (ranking) de la entidad a nivel nacional en número de personas sin primaria terminada. | Flotante |
| 8 | `%.1` | Porcentaje de la población que no completó la educación primaria. | Flotante |
| 9 | `Lugar.3` | Posición (ranking) de la entidad a nivel nacional por porcentaje de personas sin primaria terminada. | Flotante |
| 10 | `Sin secundaria terminada`| Cifr absoluta de personas que no completaron la educación secundaria. | Flotante |
| 11 | `Lugar.4` | Posición (ranking) de la entidad a nivel nacional en número de personas sin secundaria terminada. | Flotante |
| 12 | `%.2` | Porcentaje de la población que no completó la educación secundaria. | Flotante |
| 13 | `Lugar.5` | Posición (ranking) de la entidad a nivel nacional por porcentaje de personas sin secundaria terminada. | Flotante |
| 14 | `Rezago total` | Cifra absoluta total de personas en rezago educativo (suma de analfabetas, sin primaria y sin secundaria). | Flotante |
| 15 | `Lugar.6` | Posición (ranking) de la entidad a nivel nacional por número total de personas en rezago educativo. | Flotante |
| 16 | `%.3` | Porcentaje total de la población en rezago educativo. | Flotante |
| 17 | `Lugar.7` | Posición (ranking) de la entidad a nivel nacional por porcentaje total de rezago educativo. | Flotante |
| 18 | `Año` | Año de la estimación de los datos. | Entero |