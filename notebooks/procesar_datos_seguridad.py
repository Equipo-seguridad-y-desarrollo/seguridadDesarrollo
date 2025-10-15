"""
Script para procesar datos de seguridad en México

Este script transforma los datos crudos descargados en conjuntos de datos tidy
listos para análisis. Incluye validación de calidad de datos.

Requisitos:
- Haber ejecutado primero datos_seguridad_mexico.py para descargar los datos raw

Uso:
    python notebooks/procesar_datos_seguridad.py
"""

from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

# Definir rutas
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
INTERIM_DATA_DIR = BASE_DIR / "data" / "interim"

# Crear directorios si no existen
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PROCESAMIENTO DE DATOS DE SEGURIDAD EN MÉXICO")
print("=" * 70)

# ====== PROCESAR INDICADOR DE PERCEPCIÓN DE INSEGURIDAD ======
print("\n[1/2] Procesando indicador de percepción de inseguridad...")

input_file1 = RAW_DATA_DIR / "indicador_inseguridad_estados.csv"

if not input_file1.exists():
    print(f"  ✗ ERROR: No se encuentra {input_file1}")
    print("  Por favor ejecuta primero datos_seguridad_mexico.py")
else:
    df_inseguridad = pd.read_csv(input_file1)
    
    # Validaciones de calidad
    print(f"  - Registros originales: {len(df_inseguridad)}")
    
    # 1. Verificar valores nulos
    nulos_antes = df_inseguridad.isnull().sum().sum()
    print(f"  - Valores nulos encontrados: {nulos_antes}")
    
    # 2. Verificar que los años estén en el rango esperado
    años_invalidos = df_inseguridad[
        (df_inseguridad['año'] < 2011) | (df_inseguridad['año'] > 2025)
    ]
    if len(años_invalidos) > 0:
        print(f"  ⚠ Advertencia: {len(años_invalidos)} registros con años fuera de rango 2011-2025")
    
    # 3. Verificar que los valores sean positivos
    valores_negativos = df_inseguridad[df_inseguridad['valor'] < 0]
    if len(valores_negativos) > 0:
        print(f"  ⚠ Advertencia: {len(valores_negativos)} registros con valores negativos")
    
    # 4. Eliminar duplicados si existen
    duplicados_antes = df_inseguridad.duplicated().sum()
    if duplicados_antes > 0:
        print(f"  - Duplicados encontrados y eliminados: {duplicados_antes}")
        df_inseguridad = df_inseguridad.drop_duplicates()
    
    # Transformación a formato tidy (ya está en formato tidy, solo ordenar)
    df_inseguridad_tidy = df_inseguridad.sort_values(['entidad', 'año']).reset_index(drop=True)
    
    # Guardar datos procesados
    output_file1 = PROCESSED_DATA_DIR / "percepcion_inseguridad_tidy.csv"
    df_inseguridad_tidy.to_csv(output_file1, index=False)
    print(f"  ✓ Guardado: {output_file1} ({len(df_inseguridad_tidy)} registros)")

# ====== PROCESAR INCIDENCIA DELICTIVA ======
print("\n[2/2] Procesando incidencia delictiva estatal...")

input_file2 = RAW_DATA_DIR / "incidencia_delictiva_estatal_2015_2025.csv"

if not input_file2.exists():
    print(f"  ✗ ERROR: No se encuentra {input_file2}")
    print("  Por favor ejecuta primero datos_seguridad_mexico.py")
else:
    # Leer datos crudos
    df_delitos = pd.read_csv(input_file2, encoding='latin1')
    
    print(f"  - Registros originales: {len(df_delitos)}")
    print(f"  - Columnas: {len(df_delitos.columns)}")
    
    # Identificar columnas de meses (las que son numéricas al final)
    # Las columnas típicas son: Año, Clave_Ent, Entidad, Bien jurídico afectado,
    # Tipo de delito, Subtipo de delito, Modalidad, Enero, Febrero, ..., Diciembre
    
    # Obtener nombres de columnas
    cols_info = df_delitos.columns[:7].tolist() if len(df_delitos.columns) >= 7 else df_delitos.columns[:4].tolist()
    cols_meses = [col for col in df_delitos.columns if col not in cols_info]
    
    print(f"  - Columnas de información: {len(cols_info)}")
    print(f"  - Columnas de meses: {len(cols_meses)}")
    
    # Transformar de formato ancho a formato largo (tidy)
    # Cada fila debe ser: año, entidad, tipo_delito, mes, número_delitos
    
    # Primero, crear una versión intermedia con mejores nombres de columnas
    df_interim = df_delitos.copy()
    
    # Renombrar columnas si es necesario (estandarizar)
    col_mapping = {}
    for col in df_interim.columns:
        col_lower = col.lower().strip()
        if 'año' in col_lower or 'ano' in col_lower:
            col_mapping[col] = 'año'
        elif 'clave_ent' in col_lower or 'clave ent' in col_lower:
            col_mapping[col] = 'clave_entidad'
        elif col_lower == 'entidad':
            col_mapping[col] = 'entidad'
        elif 'bien' in col_lower and 'jurídico' in col_lower:
            col_mapping[col] = 'bien_juridico'
        elif col_lower == 'tipo de delito':
            col_mapping[col] = 'tipo_delito'
        elif col_lower == 'subtipo de delito':
            col_mapping[col] = 'subtipo_delito'
        elif col_lower == 'modalidad':
            col_mapping[col] = 'modalidad'
    
    df_interim = df_interim.rename(columns=col_mapping)
    
    # Guardar versión intermedia
    interim_file = INTERIM_DATA_DIR / "incidencia_delictiva_interim.csv"
    df_interim.to_csv(interim_file, index=False)
    print(f"  ✓ Guardado (intermedio): {interim_file}")
    
    # Transformar a formato tidy (largo)
    # Identificar columnas de identificación
    id_cols = [col for col in df_interim.columns if col not in cols_meses]
    
    # Convertir a formato largo
    df_tidy = pd.melt(
        df_interim,
        id_vars=id_cols,
        value_vars=cols_meses,
        var_name='mes',
        value_name='num_delitos'
    )
    
    # Limpiar valores
    # Convertir num_delitos a numérico (puede haber valores no numéricos)
    df_tidy['num_delitos'] = pd.to_numeric(df_tidy['num_delitos'], errors='coerce')
    
    # Validaciones de calidad
    print(f"  - Registros después de transformación: {len(df_tidy)}")
    
    # 1. Verificar valores nulos
    nulos = df_tidy['num_delitos'].isnull().sum()
    if nulos > 0:
        print(f"  ⚠ Advertencia: {nulos} registros con valores nulos en num_delitos")
        # Eliminar filas con valores nulos
        df_tidy = df_tidy.dropna(subset=['num_delitos'])
        print(f"  - Registros después de eliminar nulos: {len(df_tidy)}")
    
    # 2. Verificar valores negativos
    negativos = (df_tidy['num_delitos'] < 0).sum()
    if negativos > 0:
        print(f"  ⚠ Advertencia: {negativos} registros con valores negativos")
        # Convertir negativos a 0 (asumiendo que son errores)
        df_tidy.loc[df_tidy['num_delitos'] < 0, 'num_delitos'] = 0
    
    # 3. Convertir num_delitos a entero
    df_tidy['num_delitos'] = df_tidy['num_delitos'].astype(int)
    
    # 4. Ordenar por año, entidad y mes
    df_tidy = df_tidy.sort_values(['año', 'entidad', 'mes'] if 'año' in df_tidy.columns else ['entidad', 'mes'])
    df_tidy = df_tidy.reset_index(drop=True)
    
    # Guardar datos procesados (tidy)
    output_file2 = PROCESSED_DATA_DIR / "incidencia_delictiva_tidy.csv"
    df_tidy.to_csv(output_file2, index=False)
    print(f"  ✓ Guardado: {output_file2} ({len(df_tidy)} registros)")
    
    # También crear un resumen agregado por entidad y año
    if 'año' in df_tidy.columns:
        df_resumen = df_tidy.groupby(['año', 'entidad'])['num_delitos'].sum().reset_index()
        df_resumen.columns = ['año', 'entidad', 'total_delitos']
        
        output_resumen = PROCESSED_DATA_DIR / "incidencia_delictiva_resumen_anual.csv"
        df_resumen.to_csv(output_resumen, index=False)
        print(f"  ✓ Guardado (resumen): {output_resumen} ({len(df_resumen)} registros)")

# ====== REPORTE FINAL ======
print("\n" + "=" * 70)
print("PROCESAMIENTO COMPLETADO")
print("=" * 70)
print("\nArchivos generados:")
print(f"  - Procesados: {PROCESSED_DATA_DIR}/")
print(f"  - Intermedios: {INTERIM_DATA_DIR}/")
print("\nPróximos pasos:")
print("  - Revisar los diccionarios de datos en ./references/")
print("  - Utilizar los datos procesados para análisis")
print("=" * 70)
