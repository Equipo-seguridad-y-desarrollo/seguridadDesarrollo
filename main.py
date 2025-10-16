import subprocess
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# FASE 1: EJECUTAR SCRIPTS DE DESCARGA
def ejecutar_script(ruta_script):
    """
    Ejecuta un script de Python ubicado en la ruta especificada.
    """
    if not os.path.exists(ruta_script):
        print(f"Error: No se encontró el archivo en la ruta '{ruta_script}'.")
        return False

    print(f"Iniciando ejecucion de: {ruta_script}")
    try:
        # Captura la salida como bytes para manejar errores de codificación
        resultado = subprocess.run(
            [sys.executable, ruta_script],
            check=True,
            capture_output=True
        )

        # Decodifica la salida para mostrarla en la consola
        if resultado.stdout:
            try:
                print(resultado.stdout.decode('utf-8'))
            except UnicodeDecodeError:
                print(resultado.stdout.decode('cp1252', errors='replace'))

        print(f"Finalizado: {ruta_script} se ejecuto correctamente.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {ruta_script}.")
        print(f"El script finalizo con un error (codigo de salida {e.returncode}).")
        print("Salida de error (stderr):")
        # Intenta decodificar el mensaje de error para hacerlo legible
        try:
            error_message = e.stderr.decode('utf-8')
        except UnicodeDecodeError:
            error_message = e.stderr.decode('cp1252', errors='replace')
        print(error_message)
        return False
    except Exception as e:
        print(f"Ocurrio un error inesperado con {ruta_script}: {e}")
        return False

# ==============================================================================
# FASE 2: PROCESAR Y UNIFICAR DATOS DESCARGADOS
# ==============================================================================
def procesar_y_unificar_datos():
    """
    Carga, procesa y unifica todos los archivos CSV de la carpeta 'data/raw'
    y guarda el resultado en 'data/processed'.
    """
    print("\n=============================================")
    print("INICIANDO PROCESO DE UNIFICACION DE DATOS")
    print("=============================================\n")

    # --- Configuración de Rutas ---
    BASE_DIR = Path.cwd()
    RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
    PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # --- Carga de todos los datasets ---
    try:
        print(f"[INFO] Cargando archivos desde: {RAW_DATA_DIR}")
        salario = pd.read_csv(RAW_DATA_DIR / 'salario_raw.csv')
        remesas = pd.read_csv(RAW_DATA_DIR / 'remesas_raw.csv')
        pea = pd.read_csv(RAW_DATA_DIR / 'pea_raw.csv')
        ied = pd.read_csv(RAW_DATA_DIR / 'ied_raw.csv')
        gasto = pd.read_csv(RAW_DATA_DIR / 'gasto_raw.csv')
        educacion_salud = pd.read_csv(RAW_DATA_DIR / 'educacionysalud_raw.csv')
        inseguridad = pd.read_csv(RAW_DATA_DIR / 'indicador_inseguridad_estados.csv')
        incidencia = pd.read_csv(RAW_DATA_DIR / 'incidencia_delictiva_estatal_2015_2025.csv')
        gini = pd.read_csv(RAW_DATA_DIR / 'coeficiente_gini_desigualdad.csv')
        print("-> Todos los archivos CSV se han cargado correctamente.")
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró el archivo {e.filename}. Asegúrate de que los scripts de descarga hayan funcionado.")
        return False

    print("\n[INFO] Procesando y estandarizando cada dataset...")

    
    salario['año'] = salario['Quarter'].str.split('-').str[0].astype(int)
    salario_anual = salario.groupby(['año', 'State ID', 'State'])['Monthly Wage'].mean().reset_index()
    salario_anual.rename(columns={'State ID': 'id_estado', 'State': 'estado', 'Monthly Wage': 'salario_mensual_promedio'}, inplace=True)

    remesas['año'] = remesas['Quarter'].str.split('-').str[0].astype(int)
    remesas_anual = remesas.groupby(['año', 'State'])['Remittance Amount'].sum().reset_index()
    remesas_anual.rename(columns={'State': 'estado', 'Remittance Amount': 'remesas_anuales'}, inplace=True)

    pea['año'] = pea['Quarter'].str.split('-').str[0].astype(int)
    pea_anual = pea.groupby(['año', 'State ID', 'State'])['Workforce'].mean().reset_index()
    pea_anual.rename(columns={'State ID': 'id_estado', 'State': 'estado', 'Workforce': 'poblacion_economicamente_activa'}, inplace=True)

    ied['año'] = ied['Quarter'].str.split('-').str[0].astype(int)
    ied_anual = ied.groupby(['año', 'State ID', 'State'])['Investment'].sum().reset_index()
    ied_anual.rename(columns={'State ID': 'id_estado', 'State': 'estado', 'Investment': 'inversion_extranjera_anual'}, inplace=True)

    gasto.rename(columns={'Year': 'año', 'State ID': 'id_estado', 'State': 'estado'}, inplace=True)
    gasto_pivot = gasto.pivot_table(index=['año', 'id_estado', 'estado'], columns='Functional Group', values='Amount Executed', aggfunc='sum').reset_index()

    educacion_pivot = educacion_salud.pivot_table(index=['año', 'id_estado', 'estado'], columns='indicador_nombre', values='valor').reset_index()

    inseguridad.rename(columns={'clave': 'id_estado', 'entidad': 'estado', 'valor': 'percepcion_inseguridad'}, inplace=True)
    inseguridad['id_estado'] = pd.to_numeric(inseguridad['id_estado'], errors='coerce')
    inseguridad_procesado = inseguridad[inseguridad['id_estado'] != 0].copy()

    incidencia.rename(columns={'anio': 'año', 'clave_ent': 'id_estado', 'entidad': 'estado'}, inplace=True)
    incidencia_anual = incidencia.groupby(['año', 'id_estado', 'estado'])['incidencia_delictiva'].sum().reset_index()
    incidencia_anual.rename(columns={'incidencia_delictiva': 'total_incidencia_delictiva'}, inplace=True)

    gini.rename(columns={'Year': 'año', 'State ID': 'id_estado', 'State': 'estado', 'GINI': 'gini'}, inplace=True)
    
    print("-> Todos los datasets han sido procesados.")

    # --- Unificación de DataFrames ---
    print("\n[INFO] Creando el DataFrame base para la ventana de tiempo 2015-2020...")
    lista_estados = gini[['id_estado', 'estado']].drop_duplicates()
    lista_anios = pd.DataFrame({'año': range(2015, 2021)})
    base_df = pd.merge(lista_estados.assign(key=1), lista_anios.assign(key=1), on='key').drop('key', axis=1)

    dataframes_a_unir = [gini, salario_anual, pea_anual, ied_anual, gasto_pivot, educacion_pivot, inseguridad_procesado, incidencia_anual]
    
    df_final = base_df.copy()
    for df in dataframes_a_unir:
        df_final = pd.merge(df_final, df.drop(columns='estado', errors='ignore'), on=['año', 'id_estado'], how='left')

    df_final = pd.merge(df_final, remesas_anual, on=['año', 'estado'], how='left')

    # --- Guardado del Resultado ---
    output_filename = 'datos_unificados_2015_2020.csv'
    output_path = PROCESSED_DATA_DIR / output_filename
    df_final.to_csv(output_path, index=False, encoding='utf-8')

    print("\n----------------------------------------------------")
    print("PROCESO DE UNIFICACION COMPLETADO CON EXITO")
    print(f"El dataset final se ha guardado en: {output_path}")
    print(f"Filas x Columnas: {df_final.shape}")
    print("----------------------------------------------------\n")
    return True

if __name__ == "__main__":
    
    # --- FASE 1: DESCARGA ---
    print("=============================================")
    print("INICIANDO PROCESO DE DESCARGA DE DATOS")
    print("=============================================\n")
    
    scripts_a_ejecutar = [
        "notebooks/1_variables_economicas_descarga_datos_crudos.py",
        "notebooks/descarga_datos_rezago.py",
        "notebooks/importacion_inegi_edu.py",
        "notebooks/datos_seguridad_mexico.py"
    ]

    descarga_exitosa = True
    for script in scripts_a_ejecutar:
        exito = ejecutar_script(script)
        if not exito:
            print("\nProceso detenido debido a un error en el script anterior.")
            descarga_exitosa = False
            break

    # --- FASE 2: UNIFICACIÓN ---
    if descarga_exitosa:
        print("\nExito: Todos los scripts de descarga se ejecutaron correctamente.")
        procesar_y_unificar_datos()
    else:
        sys.exit(1)