"""
Script para procesar datos de seguridad en México

Este script transforma los datos raw descargados a formato tidy,
realiza validaciones de calidad y guarda los resultados en data/processed/

Requisitos:
- Datos raw previamente descargados en data/raw/
- Librerías: pandas, numpy

Uso:
    python procesar_datos_seguridad.py
"""

import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

# Configurar rutas del proyecto
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DATA_INTERIM_DIR = PROJECT_ROOT / "data" / "interim"

# Crear directorios si no existen
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DATA_INTERIM_DIR.mkdir(parents=True, exist_ok=True)


class ValidadorCalidadDatos:
    """Clase para validar la calidad de los datos"""
    
    def __init__(self):
        self.errores = []
        self.advertencias = []
    
    def validar_valores_nulos(self, df, columnas_criticas, nombre_dataset):
        """Valida que no haya valores nulos en columnas críticas"""
        for col in columnas_criticas:
            if col in df.columns:
                nulos = df[col].isnull().sum()
                pct_nulos = (nulos / len(df)) * 100
                
                if nulos > 0:
                    if pct_nulos > 10:
                        self.errores.append(
                            f"{nombre_dataset}: Columna '{col}' tiene {nulos} nulos ({pct_nulos:.2f}%)"
                        )
                    else:
                        self.advertencias.append(
                            f"{nombre_dataset}: Columna '{col}' tiene {nulos} nulos ({pct_nulos:.2f}%)"
                        )
    
    def validar_rango_valores(self, df, columna, min_val, max_val, nombre_dataset):
        """Valida que los valores estén en un rango esperado"""
        if columna in df.columns:
            fuera_rango = df[
                (df[columna] < min_val) | (df[columna] > max_val)
            ]
            
            if len(fuera_rango) > 0:
                self.advertencias.append(
                    f"{nombre_dataset}: {len(fuera_rango)} valores en '{columna}' fuera del rango [{min_val}, {max_val}]"
                )
    
    def validar_tipos_datos(self, df, columnas_tipos, nombre_dataset):
        """Valida que las columnas tengan los tipos de datos correctos"""
        for col, tipo_esperado in columnas_tipos.items():
            if col in df.columns:
                tipo_actual = df[col].dtype
                
                if tipo_esperado == 'numeric' and not pd.api.types.is_numeric_dtype(tipo_actual):
                    self.errores.append(
                        f"{nombre_dataset}: Columna '{col}' debería ser numérica pero es {tipo_actual}"
                    )
                elif tipo_esperado == 'string' and not pd.api.types.is_string_dtype(tipo_actual) and tipo_actual != 'object':
                    self.advertencias.append(
                        f"{nombre_dataset}: Columna '{col}' debería ser string pero es {tipo_actual}"
                    )
    
    def validar_duplicados(self, df, columnas_clave, nombre_dataset):
        """Valida que no haya registros duplicados"""
        duplicados = df.duplicated(subset=columnas_clave, keep=False)
        num_duplicados = duplicados.sum()
        
        if num_duplicados > 0:
            self.advertencias.append(
                f"{nombre_dataset}: {num_duplicados} registros duplicados encontrados"
            )
    
    def validar_completitud_temporal(self, df, col_año, años_esperados, col_grupo, nombre_dataset):
        """Valida que haya datos para todos los años esperados por grupo"""
        if col_grupo in df.columns and col_año in df.columns:
            grupos_incompletos = []
            
            for grupo in df[col_grupo].unique():
                años_disponibles = set(df[df[col_grupo] == grupo][col_año].unique())
                años_faltantes = set(años_esperados) - años_disponibles
                
                if años_faltantes:
                    grupos_incompletos.append(f"{grupo} (faltan años: {sorted(años_faltantes)})")
            
            if grupos_incompletos and len(grupos_incompletos) <= 5:
                self.advertencias.append(
                    f"{nombre_dataset}: Grupos con datos incompletos: {', '.join(grupos_incompletos[:5])}"
                )
            elif grupos_incompletos:
                self.advertencias.append(
                    f"{nombre_dataset}: {len(grupos_incompletos)} grupos con datos incompletos"
                )
    
    def mostrar_resultados(self):
        """Muestra los resultados de las validaciones"""
        print("\n" + "=" * 80)
        print("RESULTADOS DE VALIDACIÓN DE CALIDAD")
        print("=" * 80)
        
        if self.errores:
            print(f"\n❌ ERRORES CRÍTICOS ({len(self.errores)}):")
            for error in self.errores:
                print(f"  • {error}")
        
        if self.advertencias:
            print(f"\n⚠️  ADVERTENCIAS ({len(self.advertencias)}):")
            for advertencia in self.advertencias:
                print(f"  • {advertencia}")
        
        if not self.errores and not self.advertencias:
            print("\n✅ Todas las validaciones pasaron correctamente")
        
        print("\n" + "=" * 80)
        
        return len(self.errores) == 0


def procesar_percepcion_inseguridad(validador):
    """
    Procesa datos de percepción de inseguridad
    
    Args:
        validador: Instancia de ValidadorCalidadDatos
        
    Returns:
        DataFrame procesado
    """
    print("\n📊 Procesando datos de percepción de inseguridad...")
    
    # Cargar datos raw
    input_file = DATA_RAW_DIR / "indicador_inseguridad_estados.csv"
    if not input_file.exists():
        print(f"❌ Error: No se encontró {input_file}")
        return None
    
    df = pd.read_csv(input_file)
    print(f"  ✓ Cargados {len(df)} registros")
    
    # 1. Limpieza básica
    df_clean = df.copy()
    
    # Renombrar columnas para consistencia
    df_clean = df_clean.rename(columns={
        'clave': 'cve_entidad'
    })
    
    # 2. Convertir tipos de datos
    df_clean['año'] = df_clean['año'].astype(int)
    df_clean['valor'] = pd.to_numeric(df_clean['valor'], errors='coerce')
    df_clean['cve_entidad'] = df_clean['cve_entidad'].astype(str).str.zfill(2)
    
    # 3. Agregar columnas calculadas
    # Categorizar nivel de percepción
    df_clean['nivel_percepcion'] = pd.cut(
        df_clean['valor'],
        bins=[0, 50000, 70000, 85000, 100000],
        labels=['Bajo', 'Medio', 'Alto', 'Muy Alto'],
        include_lowest=True
    )
    
    # Indicador de entidad nacional
    df_clean['es_nacional'] = df_clean['entidad'] == 'Nacional'
    
    # 4. Ordenar datos
    df_clean = df_clean.sort_values(['cve_entidad', 'año']).reset_index(drop=True)
    
    # 5. Validaciones de calidad
    print("  → Ejecutando validaciones de calidad...")
    
    validador.validar_valores_nulos(
        df_clean,
        columnas_criticas=['año', 'valor', 'entidad', 'cve_entidad'],
        nombre_dataset='Percepción de Inseguridad'
    )
    
    validador.validar_tipos_datos(
        df_clean,
        columnas_tipos={
            'año': 'numeric',
            'valor': 'numeric',
            'entidad': 'string',
            'cve_entidad': 'string'
        },
        nombre_dataset='Percepción de Inseguridad'
    )
    
    validador.validar_rango_valores(
        df_clean,
        columna='valor',
        min_val=0,
        max_val=100000,
        nombre_dataset='Percepción de Inseguridad'
    )
    
    validador.validar_duplicados(
        df_clean,
        columnas_clave=['año', 'cve_entidad'],
        nombre_dataset='Percepción de Inseguridad'
    )
    
    años_esperados = range(2011, 2026)  # 2011-2025
    validador.validar_completitud_temporal(
        df_clean,
        col_año='año',
        años_esperados=años_esperados,
        col_grupo='entidad',
        nombre_dataset='Percepción de Inseguridad'
    )
    
    # 6. Guardar datos procesados
    output_file = DATA_PROCESSED_DIR / "percepcion_inseguridad_procesado.csv"
    df_clean.to_csv(output_file, index=False)
    print(f"  ✓ Guardado: {output_file}")
    
    # Guardar también versión sin nacional (solo estados)
    df_estados = df_clean[df_clean['entidad'] != 'Nacional'].copy()
    output_file_estados = DATA_PROCESSED_DIR / "percepcion_inseguridad_estados.csv"
    df_estados.to_csv(output_file_estados, index=False)
    print(f"  ✓ Guardado: {output_file_estados}")
    
    return df_clean


def procesar_incidencia_delictiva(validador):
    """
    Procesa datos de incidencia delictiva
    
    Args:
        validador: Instancia de ValidadorCalidadDatos
        
    Returns:
        DataFrame procesado
    """
    print("\n📊 Procesando datos de incidencia delictiva...")
    
    # Cargar datos raw
    input_file = DATA_RAW_DIR / "incidencia_delictiva_estatal_2015_2025.csv"
    if not input_file.exists():
        print(f"❌ Error: No se encontró {input_file}")
        return None
    
    df = pd.read_csv(input_file, encoding='latin-1')
    print(f"  ✓ Cargados {len(df)} registros")
    
    # Mostrar columnas para entender la estructura
    print(f"  → Columnas detectadas: {df.columns.tolist()[:5]}...")
    
    # Normalizar nombres de columnas (quitar espacios, minúsculas)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Detectar columnas de año y mes (pueden variar)
    col_año = None
    col_mes = None
    
    for col in df.columns:
        if 'año' in col or 'ano' in col or col == 'año':
            col_año = col
        elif 'mes' in col:
            col_mes = col
    
    if not col_año:
        # Buscar columna numérica que parezca año
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                valores_unicos = df[col].unique()
                if any(2015 <= v <= 2025 for v in valores_unicos if pd.notna(v)):
                    col_año = col
                    break
    
    print(f"  → Columna de año detectada: {col_año}")
    print(f"  → Columna de mes detectada: {col_mes}")
    
    # Guardar versión intermedia con toda la información
    interim_file = DATA_INTERIM_DIR / "incidencia_delictiva_completa.csv"
    df.to_csv(interim_file, index=False)
    print(f"  ✓ Guardado archivo intermedio: {interim_file}")
    
    # Crear versión agregada simple (si es posible)
    if col_año:
        # Intentar crear agregación por año y entidad
        cols_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remover columnas que no son conteos
        cols_excluir = [col_año, col_mes] if col_mes else [col_año]
        cols_conteo = [c for c in cols_numericas if c not in cols_excluir]
        
        if cols_conteo:
            print(f"  → Creando agregación anual...")
            
            # Agrupar por año (y entidad si existe)
            cols_grupo = [col_año]
            col_entidad = None
            
            for col in df.columns:
                if 'entidad' in col or 'estado' in col:
                    col_entidad = col
                    cols_grupo.append(col)
                    break
            
            # Crear DataFrame simple procesado
            df_procesado = df[cols_grupo + cols_conteo].copy()
            
            # Validaciones básicas
            if col_año:
                validador.validar_valores_nulos(
                    df_procesado,
                    columnas_criticas=cols_grupo,
                    nombre_dataset='Incidencia Delictiva'
                )
            
            output_file = DATA_PROCESSED_DIR / "incidencia_delictiva_procesado.csv"
            df_procesado.to_csv(output_file, index=False)
            print(f"  ✓ Guardado: {output_file}")
            
            return df_procesado
    
    print("  ⚠️  Estructura de datos compleja - solo se guardó versión intermedia")
    return df


def generar_reporte_procesamiento(df_percepcion, df_delictiva):
    """
    Genera un reporte del procesamiento realizado
    
    Args:
        df_percepcion: DataFrame procesado de percepción
        df_delictiva: DataFrame procesado de delictiva
    """
    reporte_file = DATA_PROCESSED_DIR / "reporte_procesamiento.txt"
    
    with open(reporte_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE PROCESAMIENTO DE DATOS DE SEGURIDAD\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha de procesamiento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Percepción de Inseguridad
        if df_percepcion is not None:
            f.write("\n" + "=" * 80 + "\n")
            f.write("DATASET 1: Percepción de Inseguridad\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total de registros: {len(df_percepcion)}\n")
            f.write(f"Período: {df_percepcion['año'].min()} - {df_percepcion['año'].max()}\n")
            f.write(f"Entidades: {df_percepcion['entidad'].nunique()}\n")
            f.write(f"\nColumnas generadas:\n")
            for col in df_percepcion.columns:
                f.write(f"  - {col}: {df_percepcion[col].dtype}\n")
            
            f.write(f"\nEstadísticas del indicador 'valor':\n")
            f.write(f"  - Media: {df_percepcion['valor'].mean():.2f}\n")
            f.write(f"  - Mediana: {df_percepcion['valor'].median():.2f}\n")
            f.write(f"  - Desv. Std: {df_percepcion['valor'].std():.2f}\n")
            f.write(f"  - Mínimo: {df_percepcion['valor'].min():.2f}\n")
            f.write(f"  - Máximo: {df_percepcion['valor'].max():.2f}\n")
            
            f.write(f"\nDistribución por nivel de percepción:\n")
            if 'nivel_percepcion' in df_percepcion.columns:
                for nivel, count in df_percepcion['nivel_percepcion'].value_counts().items():
                    pct = count / len(df_percepcion) * 100
                    f.write(f"  - {nivel}: {count} ({pct:.1f}%)\n")
        
        # Incidencia Delictiva
        if df_delictiva is not None:
            f.write("\n" + "=" * 80 + "\n")
            f.write("DATASET 2: Incidencia Delictiva\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total de registros: {len(df_delictiva)}\n")
            f.write(f"Columnas: {len(df_delictiva.columns)}\n")
            f.write(f"\nPrimeras columnas:\n")
            for col in df_delictiva.columns[:10]:
                f.write(f"  - {col}: {df_delictiva[col].dtype}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("FIN DEL REPORTE\n")
        f.write("=" * 80 + "\n")
    
    print(f"\n✓ Reporte de procesamiento guardado: {reporte_file}")


def main():
    """Función principal del script"""
    print("=" * 80)
    print("PROCESAMIENTO DE DATOS DE SEGURIDAD - MÉXICO")
    print("=" * 80)
    print(f"\nDirectorio de datos raw: {DATA_RAW_DIR}")
    print(f"Directorio de datos procesados: {DATA_PROCESSED_DIR}")
    print(f"Directorio de datos intermedios: {DATA_INTERIM_DIR}")
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Verificar que existan los datos raw
    archivos_requeridos = [
        "indicador_inseguridad_estados.csv",
        "incidencia_delictiva_estatal_2015_2025.csv"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not (DATA_RAW_DIR / archivo).exists():
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(" ERROR: Faltan archivos raw necesarios:")
        for archivo in archivos_faltantes:
            print(f"  • {archivo}")
        print("\nPor favor, ejecuta primero el script de descarga:")
        print("  python datos_seguridad_mexico.py --token TU_TOKEN")
        sys.exit(1)
    
    # Crear validador de calidad
    validador = ValidadorCalidadDatos()
    
    # Procesar datasets
    df_percepcion = procesar_percepcion_inseguridad(validador)
    df_delictiva = procesar_incidencia_delictiva(validador)
    
    # Mostrar resultados de validación
    validacion_exitosa = validador.mostrar_resultados()
    
    # Generar reporte
    generar_reporte_procesamiento(df_percepcion, df_delictiva)
    
    print("\n" + "=" * 80)
    print("¡PROCESAMIENTO COMPLETADO!")
    print("=" * 80)
    print(f"\nArchivos generados:")
    print(f"\nProcesados (data/processed/):")
    print("  • percepcion_inseguridad_procesado.csv")
    print("  • percepcion_inseguridad_estados.csv")
    print("  • incidencia_delictiva_procesado.csv")
    print("  • reporte_procesamiento.txt")
    print(f"\nIntermedios (data/interim/):")
    print("  • incidencia_delictiva_completa.csv")
    
    if not validacion_exitosa:
        print("\n⚠️  ATENCIÓN: Se encontraron errores de calidad. Revisa el reporte arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
