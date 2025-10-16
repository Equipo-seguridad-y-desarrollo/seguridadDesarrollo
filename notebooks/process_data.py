"""
Script unificado para procesamiento de datos

Este script procesa los datos crudos descargados y genera datasets tidy
listos para análisis.

Procesos realizados:
1. Limpieza y validación de datos
2. Transformación a formato tidy
3. Agregación temporal
4. Control de calidad

Autor: Equipo Seguridad y Desarrollo
Fecha: 2025
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
INTERIM_DATA_DIR = BASE_DIR / "data" / "interim"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Crear directorios si no existen
INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def validate_data(df, nombre, columnas_requeridas):
    """Valida que el DataFrame tenga las columnas necesarias y datos válidos"""
    print(f"\n  Validando {nombre}...")
    
    # Verificar columnas requeridas
    columnas_faltantes = set(columnas_requeridas) - set(df.columns)
    if columnas_faltantes:
        print(f"    ✗ Error: Faltan columnas: {columnas_faltantes}")
        return False
    
    # Verificar que no esté vacío
    if len(df) == 0:
        print(f"    ✗ Error: DataFrame vacío")
        return False
    
    # Verificar valores nulos en columnas críticas
    nulls = df[columnas_requeridas].isnull().sum()
    if nulls.any():
        print(f"    ⚠ Advertencia: Valores nulos encontrados:")
        for col in columnas_requeridas:
            if df[col].isnull().sum() > 0:
                print(f"      - {col}: {df[col].isnull().sum()} nulos")
    
    print(f"    ✓ Validación exitosa: {len(df)} registros")
    return True


def process_ied_data():
    """Procesa datos de Inversión Extranjera Directa"""
    print("\n" + "="*80)
    print("PROCESANDO: Inversión Extranjera Directa (IED)")
    print("="*80)
    
    try:
        # Leer datos crudos
        df = pd.read_csv(RAW_DATA_DIR / "ied_raw.csv")
        
        # Validar
        if not validate_data(df, "IED", ['State', 'Quarter', 'Investment']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir Investment a numérico
        df_clean['Investment'] = pd.to_numeric(df_clean['Investment'], errors='coerce')
        
        # Extraer año y trimestre
        df_clean['Año'] = df_clean['Quarter'].str[:4].astype(int)
        df_clean['Trimestre'] = df_clean['Quarter'].str[-2:]
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'State': 'Estado',
            'Investment': 'IED_millones_usd'
        })
        
        # Seleccionar columnas finales
        df_tidy = df_clean[['Estado', 'Año', 'Trimestre', 'IED_millones_usd']]
        
        # Ordenar
        df_tidy = df_tidy.sort_values(['Estado', 'Año', 'Trimestre'])
        
        # Guardar datos procesados
        filepath = PROCESSED_DATA_DIR / "ied_procesado.csv"
        df_tidy.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados: {filepath}")
        print(f"  Registros: {len(df_tidy)}")
        print(f"  Estados: {df_tidy['Estado'].nunique()}")
        print(f"  Periodo: {df_tidy['Año'].min()}-{df_tidy['Año'].max()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando IED: {str(e)}")
        return False


def process_salario_data():
    """Procesa datos de Salario Mensual"""
    print("\n" + "="*80)
    print("PROCESANDO: Salario Mensual")
    print("="*80)
    
    try:
        # Leer datos crudos
        df = pd.read_csv(RAW_DATA_DIR / "salario_raw.csv")
        
        # Validar
        if not validate_data(df, "Salario", ['State', 'Quarter', 'Monthly Wage']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir salario a numérico
        df_clean['Monthly Wage'] = pd.to_numeric(df_clean['Monthly Wage'], errors='coerce')
        
        # Extraer año y trimestre
        df_clean['Año'] = df_clean['Quarter'].str[:4].astype(int)
        df_clean['Trimestre'] = df_clean['Quarter'].str[-2:]
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'State': 'Estado',
            'Monthly Wage': 'Salario_mensual_pesos'
        })
        
        # Seleccionar columnas finales
        df_tidy = df_clean[['Estado', 'Año', 'Trimestre', 'Salario_mensual_pesos']]
        
        # Ordenar
        df_tidy = df_tidy.sort_values(['Estado', 'Año', 'Trimestre'])
        
        # Guardar datos procesados
        filepath = PROCESSED_DATA_DIR / "salario_procesado.csv"
        df_tidy.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados: {filepath}")
        print(f"  Registros: {len(df_tidy)}")
        print(f"  Estados: {df_tidy['Estado'].nunique()}")
        print(f"  Periodo: {df_tidy['Año'].min()}-{df_tidy['Año'].max()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando Salario: {str(e)}")
        return False


def process_pea_data():
    """Procesa datos de Población Económicamente Activa"""
    print("\n" + "="*80)
    print("PROCESANDO: Población Económicamente Activa (PEA)")
    print("="*80)
    
    try:
        # Leer datos crudos
        df = pd.read_csv(RAW_DATA_DIR / "pea_raw.csv")
        
        # Validar
        if not validate_data(df, "PEA", ['State', 'Quarter', 'Workforce']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir workforce a numérico
        df_clean['Workforce'] = pd.to_numeric(df_clean['Workforce'], errors='coerce')
        
        # Extraer año y trimestre
        df_clean['Año'] = df_clean['Quarter'].str[:4].astype(int)
        df_clean['Trimestre'] = df_clean['Quarter'].str[-2:]
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'State': 'Estado',
            'Workforce': 'PEA_personas'
        })
        
        # Seleccionar columnas finales
        df_tidy = df_clean[['Estado', 'Año', 'Trimestre', 'PEA_personas']]
        
        # Ordenar
        df_tidy = df_tidy.sort_values(['Estado', 'Año', 'Trimestre'])
        
        # Guardar datos procesados
        filepath = PROCESSED_DATA_DIR / "pea_procesado.csv"
        df_tidy.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados: {filepath}")
        print(f"  Registros: {len(df_tidy)}")
        print(f"  Estados: {df_tidy['Estado'].nunique()}")
        print(f"  Periodo: {df_tidy['Año'].min()}-{df_tidy['Año'].max()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando PEA: {str(e)}")
        return False


def process_gasto_data():
    """Procesa datos de Gasto Público"""
    print("\n" + "="*80)
    print("PROCESANDO: Gasto Público Ejecutado")
    print("="*80)
    
    try:
        # Leer datos crudos
        df = pd.read_csv(RAW_DATA_DIR / "gasto_raw.csv")
        
        # Validar
        if not validate_data(df, "Gasto", ['State', 'Year', 'Amount Executed']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir monto a numérico
        df_clean['Amount Executed'] = pd.to_numeric(df_clean['Amount Executed'], errors='coerce')
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'State': 'Estado',
            'Year': 'Año',
            'Functional Group': 'Grupo_Funcional',
            'Amount Executed': 'Gasto_ejecutado_pesos'
        })
        
        # Agregar por estado y año (sumando todos los grupos funcionales)
        df_agregado = df_clean.groupby(['Estado', 'Año']).agg({
            'Gasto_ejecutado_pesos': 'sum'
        }).reset_index()
        
        # Ordenar
        df_agregado = df_agregado.sort_values(['Estado', 'Año'])
        
        # Guardar datos detallados (con grupos funcionales) en interim
        df_detallado = df_clean[['Estado', 'Año', 'Grupo_Funcional', 'Gasto_ejecutado_pesos']]
        filepath_interim = INTERIM_DATA_DIR / "gasto_detallado.csv"
        df_detallado.to_csv(filepath_interim, index=False)
        print(f"\n✓ Datos detallados guardados: {filepath_interim}")
        
        # Guardar datos agregados en processed
        filepath = PROCESSED_DATA_DIR / "gasto_procesado.csv"
        df_agregado.to_csv(filepath, index=False)
        print(f"✓ Datos agregados guardados: {filepath}")
        print(f"  Registros: {len(df_agregado)}")
        print(f"  Estados: {df_agregado['Estado'].nunique()}")
        print(f"  Periodo: {df_agregado['Año'].min()}-{df_agregado['Año'].max()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando Gasto: {str(e)}")
        return False


def process_remesas_data():
    """Procesa datos de Remesas"""
    print("\n" + "="*80)
    print("PROCESANDO: Remesas")
    print("="*80)
    
    try:
        # Leer datos crudos
        df = pd.read_csv(RAW_DATA_DIR / "remesas_raw.csv")
        
        # Validar
        if not validate_data(df, "Remesas", ['State', 'Quarter', 'Remittance Amount']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir monto a numérico
        df_clean['Remittance Amount'] = pd.to_numeric(df_clean['Remittance Amount'], errors='coerce')
        
        # Extraer año y trimestre
        df_clean['Año'] = df_clean['Quarter'].str[:4].astype(int)
        df_clean['Trimestre'] = df_clean['Quarter'].str[-2:]
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'State': 'Estado',
            'Remittance Amount': 'Remesas_millones_usd'
        })
        
        # Seleccionar columnas finales
        df_tidy = df_clean[['Estado', 'Año', 'Trimestre', 'Remesas_millones_usd']]
        
        # Ordenar
        df_tidy = df_tidy.sort_values(['Estado', 'Año', 'Trimestre'])
        
        # Guardar datos procesados
        filepath = PROCESSED_DATA_DIR / "remesas_procesado.csv"
        df_tidy.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados: {filepath}")
        print(f"  Registros: {len(df_tidy)}")
        print(f"  Estados: {df_tidy['Estado'].nunique()}")
        print(f"  Periodo: {df_tidy['Año'].min()}-{df_tidy['Año'].max()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando Remesas: {str(e)}")
        return False


def process_inegi_data():
    """Procesa datos de INEGI - Educación y Salud"""
    print("\n" + "="*80)
    print("PROCESANDO: Indicadores INEGI - Educación y Salud")
    print("="*80)
    
    try:
        filepath = RAW_DATA_DIR / "inegi_educacion_salud_raw.csv"
        if not filepath.exists():
            print(f"  ⚠ Archivo no encontrado: {filepath}")
            return False
        
        # Leer datos crudos
        df = pd.read_csv(filepath)
        
        # Validar
        if not validate_data(df, "INEGI", ['indicador_nombre', 'periodo', 'valor']):
            return False
        
        # Limpiar y transformar
        df_clean = df.copy()
        
        # Convertir valor a numérico
        df_clean['valor'] = pd.to_numeric(df_clean['valor'], errors='coerce')
        
        # Renombrar columnas
        df_clean = df_clean.rename(columns={
            'indicador_nombre': 'Indicador',
            'periodo': 'Periodo',
            'valor': 'Valor',
            'estado': 'Estado'
        })
        
        # Pivotar para tener un formato más usable
        df_pivot = df_clean.pivot_table(
            index=['Estado', 'Periodo'],
            columns='Indicador',
            values='Valor',
            aggfunc='first'
        ).reset_index()
        
        # Ordenar
        df_pivot = df_pivot.sort_values(['Estado', 'Periodo'])
        
        # Guardar datos procesados
        filepath = PROCESSED_DATA_DIR / "educacion_salud_procesado.csv"
        df_pivot.to_csv(filepath, index=False)
        print(f"\n✓ Datos procesados guardados: {filepath}")
        print(f"  Registros: {len(df_pivot)}")
        if 'Estado' in df_pivot.columns:
            print(f"  Estados: {df_pivot['Estado'].nunique()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error procesando INEGI: {str(e)}")
        return False


def create_consolidated_dataset():
    """Crea un dataset consolidado con todos los indicadores"""
    print("\n" + "="*80)
    print("CREANDO DATASET CONSOLIDADO")
    print("="*80)
    
    try:
        # Leer todos los datasets procesados
        datasets = {}
        
        files = {
            'ied': PROCESSED_DATA_DIR / "ied_procesado.csv",
            'salario': PROCESSED_DATA_DIR / "salario_procesado.csv",
            'pea': PROCESSED_DATA_DIR / "pea_procesado.csv",
            'gasto': PROCESSED_DATA_DIR / "gasto_procesado.csv",
            'remesas': PROCESSED_DATA_DIR / "remesas_procesado.csv",
        }
        
        for nombre, filepath in files.items():
            if filepath.exists():
                datasets[nombre] = pd.read_csv(filepath)
                print(f"  ✓ Cargado: {nombre}")
            else:
                print(f"  ⚠ No encontrado: {nombre}")
        
        if not datasets:
            print("  ✗ No hay datasets para consolidar")
            return False
        
        # Consolidar datasets trimestrales
        df_consolidado = None
        
        for nombre, df in datasets.items():
            if nombre == 'gasto':  # Gasto es anual, no trimestral
                continue
                
            # Asegurar que tenga las columnas necesarias
            if not all(col in df.columns for col in ['Estado', 'Año', 'Trimestre']):
                continue
            
            if df_consolidado is None:
                df_consolidado = df.copy()
            else:
                # Hacer merge por Estado, Año y Trimestre
                df_consolidado = pd.merge(
                    df_consolidado,
                    df,
                    on=['Estado', 'Año', 'Trimestre'],
                    how='outer'
                )
        
        if df_consolidado is not None:
            # Agregar gasto público (anual)
            if 'gasto' in datasets:
                df_gasto = datasets['gasto'][['Estado', 'Año', 'Gasto_ejecutado_pesos']]
                df_consolidado = pd.merge(
                    df_consolidado,
                    df_gasto,
                    on=['Estado', 'Año'],
                    how='left'
                )
            
            # Ordenar
            df_consolidado = df_consolidado.sort_values(['Estado', 'Año', 'Trimestre'])
            
            # Guardar
            filepath = PROCESSED_DATA_DIR / "datos_consolidados.csv"
            df_consolidado.to_csv(filepath, index=False)
            print(f"\n✓ Dataset consolidado guardado: {filepath}")
            print(f"  Registros: {len(df_consolidado)}")
            print(f"  Estados: {df_consolidado['Estado'].nunique()}")
            print(f"  Variables: {len(df_consolidado.columns)}")
            
            return True
        else:
            print("  ✗ No se pudo crear dataset consolidado")
            return False
        
    except Exception as e:
        print(f"\n✗ Error creando dataset consolidado: {str(e)}")
        return False


def generate_quality_report():
    """Genera un reporte de calidad de los datos procesados"""
    print("\n" + "="*80)
    print("REPORTE DE CALIDAD DE DATOS")
    print("="*80)
    
    report = []
    report.append(f"Fecha de reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("="*80 + "\n")
    
    # Revisar cada archivo procesado
    for filepath in PROCESSED_DATA_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(filepath)
            
            report.append(f"\nArchivo: {filepath.name}")
            report.append(f"  Registros totales: {len(df)}")
            report.append(f"  Columnas: {len(df.columns)}")
            report.append(f"  Columnas: {', '.join(df.columns)}")
            
            # Valores nulos
            nulls = df.isnull().sum()
            if nulls.any():
                report.append("  Valores nulos:")
                for col in nulls[nulls > 0].index:
                    pct = (nulls[col] / len(df)) * 100
                    report.append(f"    - {col}: {nulls[col]} ({pct:.1f}%)")
            else:
                report.append("  ✓ Sin valores nulos")
            
            # Duplicados
            duplicados = df.duplicated().sum()
            if duplicados > 0:
                report.append(f"  ⚠ Duplicados: {duplicados}")
            else:
                report.append("  ✓ Sin duplicados")
            
            report.append("")
            
        except Exception as e:
            report.append(f"\n  ✗ Error procesando {filepath.name}: {str(e)}\n")
    
    # Guardar reporte
    report_text = "\n".join(report)
    report_path = PROCESSED_DATA_DIR / "reporte_calidad.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"✓ Reporte guardado: {report_path}")


def main():
    """Función principal que ejecuta todo el procesamiento"""
    print("\n" + "="*80)
    print("INICIANDO PROCESAMIENTO DE DATOS")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    resultados = {
        'IED': False,
        'Salario': False,
        'PEA': False,
        'Gasto Público': False,
        'Remesas': False,
        'INEGI Educación/Salud': False,
        'Dataset Consolidado': False
    }
    
    # Ejecutar procesamientos
    try:
        resultados['IED'] = process_ied_data()
    except Exception as e:
        print(f"\n✗ Error en IED: {str(e)}")
    
    try:
        resultados['Salario'] = process_salario_data()
    except Exception as e:
        print(f"\n✗ Error en Salario: {str(e)}")
    
    try:
        resultados['PEA'] = process_pea_data()
    except Exception as e:
        print(f"\n✗ Error en PEA: {str(e)}")
    
    try:
        resultados['Gasto Público'] = process_gasto_data()
    except Exception as e:
        print(f"\n✗ Error en Gasto Público: {str(e)}")
    
    try:
        resultados['Remesas'] = process_remesas_data()
    except Exception as e:
        print(f"\n✗ Error en Remesas: {str(e)}")
    
    try:
        resultados['INEGI Educación/Salud'] = process_inegi_data()
    except Exception as e:
        print(f"\n✗ Error en INEGI: {str(e)}")
    
    try:
        resultados['Dataset Consolidado'] = create_consolidated_dataset()
    except Exception as e:
        print(f"\n✗ Error en consolidación: {str(e)}")
    
    # Generar reporte de calidad
    try:
        generate_quality_report()
    except Exception as e:
        print(f"\n✗ Error generando reporte: {str(e)}")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE PROCESAMIENTO")
    print("="*80)
    for nombre, exito in resultados.items():
        status = "✓" if exito else "✗"
        print(f"{status} {nombre}")
    
    exitosos = sum(1 for v in resultados.values() if v)
    print(f"\nTotal: {exitosos}/{len(resultados)} procesos completados exitosamente")
    
    if exitosos == 0:
        print("\n✗ ERROR: No se pudo procesar ningún dataset")
        sys.exit(1)
    elif exitosos < len(resultados):
        print("\n⚠ ADVERTENCIA: Algunos datasets no se procesaron correctamente")
        sys.exit(0)
    else:
        print("\n✓ Todos los datasets procesados exitosamente")
        sys.exit(0)


if __name__ == "__main__":
    main()
