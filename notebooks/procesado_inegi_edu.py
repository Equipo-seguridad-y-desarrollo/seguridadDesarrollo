import pandas as pd
import os

def descarga_csv(dataframe, nombre_carpeta, nombre_archivo):
    """
    Guarda el DataFrame en un archivo CSV en la carpeta destino.

    Args:
        dataframe (pd.DataFrame): El DataFrame a guardar.
        nombre_carpeta (str): La ruta de la carpeta donde se guarda el archivo.
        nombre_archivo (str): El nombre del archivo CSV.
    """
    try:
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            print(f"Se creó la carpeta: '{nombre_carpeta}'")

        ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)
        dataframe.to_csv(ruta_completa, index=False, encoding='utf-8')
        
        print(f"Archivo con dataframe de educacion y salud creado en: '{ruta_completa}'")

    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo: {e}")

# Carga de datos raw
df_raw = pd.read_csv('../data/raw/educacionysalud.csv')

#Cambio de formato long a wide usando pivot_table
df_raw['valor'] = pd.to_numeric(df_raw['valor'], errors='coerce')
df_wide = df_raw.pivot_table(index=['id_estado','estado', 'año'], columns = 'indicador_nombre', values = 'valor').reset_index()
df_wide.columns = ['id_estado','estado', 'fecha', 'derhab', 'pob_bac', 'pob_edbas', 'pob_edsup', 'porc_analf', 'porc_sined', 'promedio_ed']

# Diagnóstico rápido
print("--- Dimensiones del DataFrame ---")
print(df_wide.shape)

print("\n--- Primeras filas ---")
print(df_wide.head())

print("\n--- Tipos de datos y nulos ---")
print(df_wide.info())

print("\n--- Estadísticas descriptivas ---")
print(df_wide.describe())

#Creacion de copia para limpieza de datos
df_interim = df_wide.copy()

#LIMPIEZA DE DATOS

#Tipo de dato
df_interim['estado'] = df_interim['estado'].astype('category')
df_interim['id_estado'] = df_interim['id_estado'].astype('category')

#Filtramos por fecha, solo se utilizaran datos del 2000 en adelante
df_interim = df_interim[df_interim['fecha'] >= 2000].copy()

#Guardado de datos /interim/
descarga_csv(df_interim, nombre_carpeta='../data/interim/', nombre_archivo='educacionysalud_2000_filtrado.csv')

#Datos nulos
# Calcula el porcentaje de nulos por columna, si es mayor a 60, eliminaremos la columna
porcentaje_nulos = df_interim.isnull().sum() / len(df_interim) * 100
umbral = 60
drop_columnas = porcentaje_nulos[porcentaje_nulos >= umbral].index.tolist()
df_limpio = df_interim.drop(columns= drop_columnas)


#Imputación con interpolación lineal
#Ordena los datos por estado y año
df_limpio = df_limpio.sort_values(by=['estado', 'fecha'])

#Creación de columna indicadora de imputación
columnas_a_imputar = ['derhab', 'porc_analf', 'promedio_ed']
for col in columnas_a_imputar:
    # Solo crea la columna si existe en df_limpio
    if col in df_limpio.columns:
        nombre_col_indicador = f'{col}_imputado'
        df_limpio[nombre_col_indicador] = df_limpio[col].isnull().astype(int)

# Agrupa por estado y aplica la interpolación a cada grupo
df_limpio[columnas_a_imputar] = df_limpio.groupby('estado', observed=False)[columnas_a_imputar].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both')
)

print("Datos nulos después de la interpolación:")
print(df_limpio.isnull().sum())

#PRUEBAS DE CALIDAD
# Regla 1: No debe haber valores nulos en columnas clave.
assert df_limpio['estado'].isnull().sum() == 0, "La columna 'estado' no puede tener nulos."
assert df_limpio['fecha'].isnull().sum() == 0, "La columna 'fecha' no puede tener nulos."

# Regla 2: Los valores de los indicadores deben estar en un rango lógico.
# (Ej. los porcentajes deben estar entre 0 y 100)
assert df_limpio['porc_analf'].between(0, 100).all(), "Hay porcentajes de analfabetismo fuera del rango 0-100."

# Regla 3: Consistencia categórica de estados, el número de estados únicos debe ser 32
assert df_limpio['estado'].nunique() == 32, f"Se esperaban 32 estados únicos, pero se encontraron {df_a_validar['estado'].nunique()}."
assert df_limpio['id_estado'].nunique() == 32, f"Se esperaban 32 estados únicos, pero se encontraron {df_a_validar['estado'].nunique()}."

# Regla 4: Unicidad de registros.
# (Ej. no debe haber filas duplicadas para la misma combinación de estado y año)
assert not df_limpio.duplicated(subset=['estado', 'fecha']).any(), "Existen registros duplicados de estado-fecha."

print("Todas las reglas de calidad han pasado exitosamente.")

# Guardado final de datos usando la función que creamos
descarga_csv(df_limpio, nombre_carpeta='../data/processed/', nombre_archivo='educacionysalud_procesado.csv')