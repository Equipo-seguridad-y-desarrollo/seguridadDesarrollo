<<<<<<< HEAD
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
=======
"""
Pipeline ejecutable desde main.py
Parte 1: Descarga de datos (notebooks/*)
Parte 2: Procesamiento y normalización de salidas a data/interim
"""

import sys
import os
import subprocess
from pathlib import Path
import shutil
import glob

# ============================================================
# Configuración base
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Utilidades comunes
# ============================================================
def ejecutar_script(ruta_script: str, timeout: int | None = None) -> bool:
    """
    Ejecuta un script de Python y muestra su salida. 
    Usa el mismo intérprete y fija cwd=BASE_DIR para que las rutas relativas 
    dentro de los scripts funcionen como si se ejecutaran desde la raíz del repo.
    """
    script_path = Path(ruta_script)
    if not script_path.exists():
>>>>>>> 0461075 (Modificaciones parciales main.py)
        print(f"Error: No se encontró el archivo en la ruta '{ruta_script}'.")
        return False

    print(f"Iniciando ejecucion de: {ruta_script}")
    try:
<<<<<<< HEAD
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

=======
        resultado = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR),     # importante para que data/... funcione
            timeout=timeout        # opcional
        )
        if resultado.stdout:
            print(resultado.stdout)
>>>>>>> 0461075 (Modificaciones parciales main.py)
        print(f"Finalizado: {ruta_script} se ejecuto correctamente.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {ruta_script}.")
        print(f"El script finalizo con un error (codigo de salida {e.returncode}).")
        print("Salida de error (stderr):")
<<<<<<< HEAD
        # Intenta decodificar el mensaje de error para hacerlo legible
        try:
            error_message = e.stderr.decode('utf-8')
        except UnicodeDecodeError:
            error_message = e.stderr.decode('cp1252', errors='replace')
        print(error_message)
        return False
=======
        print(e.stderr)
        return False
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout ejecutando {ruta_script}")
        return False
>>>>>>> 0461075 (Modificaciones parciales main.py)
    except Exception as e:
        print(f"Ocurrio un error inesperado con {ruta_script}: {e}")
        return False

<<<<<<< HEAD
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
=======

# Directorios candidatos para buscar scripts si solo se da el nombre
CANDIDATE_DIRS = [
    BASE_DIR,                          # raíz
    BASE_DIR / "scripts",
    BASE_DIR / "notebooks",
    BASE_DIR / "src",
    BASE_DIR / "etl",
    BASE_DIR / "processing",
]

def resolve_script_path(name_or_rel: str) -> Path | None:
    """
    Busca un script por nombre (p. ej. 'procesar_datos_rezago.py') o ruta relativa.
    Retorna Path si lo encuentra; None si no.
    """
    p = Path(name_or_rel)
    # Si ya es una ruta válida:
    if p.is_file():
        return p.resolve()

    # Prueba directorios candidatos
    for d in CANDIDATE_DIRS:
        cand = d / name_or_rel
        if cand.is_file():
            return cand.resolve()

    # Búsqueda recursiva por nombre exacto (excluye carpetas pesadas)
    exclude = {".git", ".venv", "venv", "__pycache__", "data"}
    for q in BASE_DIR.rglob("*"):
        try:
            if q.is_file() and q.name == Path(name_or_rel).name and not any(part in exclude for part in q.parts):
                return q.resolve()
        except Exception:
            pass
    return None

def suggest_similar_scripts(basename: str) -> list[str]:
    """
    Si no se encuentra el script, sugiere coincidencias por subcadena.
    """
    hits = []
    exclude = {".git", ".venv", "venv", "__pycache__"}
    needle = basename.lower()
    for p in BASE_DIR.rglob("*.py"):
        if any(part in exclude for part in p.parts):
            continue
        if needle in p.name.lower():
            try:
                hits.append(str(p.relative_to(BASE_DIR)))
            except Exception:
                hits.append(str(p))
    return sorted(hits)[:12]

def run_script_list(scripts: list[str], stop_on_fail: bool = True, label: str = "Ejecución") -> bool:
    """
    Resuelve rutas y ejecuta una lista de scripts en orden.
    """
    print(f"\n=== {label} ===")
    for fname in scripts:
        ruta = resolve_script_path(fname)
        if ruta is None:
            print(f"✗ No se encontró '{fname}' en el proyecto.")
            sugerencias = suggest_similar_scripts(Path(fname).name)
            if sugerencias:
                print("   ¿Te refieres a alguno de estos?")
                for s in sugerencias:
                    print(f"   - {s}")
            if stop_on_fail:
                return False
            else:
                continue

        ok = ejecutar_script(str(ruta))
        if not ok and stop_on_fail:
            print(f"✗ Falló la ejecución en: {ruta}")
            return False
    return True

# ============================================================
# PARTE 1: Descarga de datos (usa tu lista original)
# ============================================================
SCRIPTS_DESCARGA = [
    # Mantiene tu lista original exactamente como en tu main.py
    "notebooks/1_variables_economicas_descarga_datos_crudos.py",
    "notebooks/descarga_datos_rezago.py",
    "notebooks/importacion_inegi_edu.py",
    "notebooks/datos_seguridad_mexico.py",
]

# ============================================================
# PARTE 2: Procesamiento y normalización en data/interim
# ============================================================
SCRIPTS_PROCESAMIENTO = [
    "procesar_datos_rezago.py",
    "2_variables_economicas_procesar_datos_formateados.py",
    "procesado_inegi_edu.py",
    "procesar_datos_seguridad.py",
]

def copiar_a_interim(origen: Path, destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origen, destino)

def forzar_salida_en_interim():
    """
    Copia a data/interim TODO lo que haya quedado en:
      - data/processed/**/*.csv
      - data/raw/*procesad*.csv  (p.ej. gini_desigualdad_procesado.csv)
      - data/interim/**/*.csv
    No borra origen; solo duplica en interim.
    """
    patrones = [
        str(PROCESSED_DIR / "**" / "*.csv"),
        str(RAW_DIR / "*procesad*.csv"),   # coincide con *_procesado* / *_processed*
        str(INTERIM_DIR / "**" / "*.csv"),
    ]
    vistos = set()
    for patron in patrones:
        for ruta in glob.glob(patron, recursive=True):
            p = Path(ruta)
            if p.is_file():
                destino = INTERIM_DIR / p.name
                clave = (p.resolve(), destino.resolve())
                if clave in vistos:
                    continue
                copiar_a_interim(p, destino)
                vistos.add(clave)
                print(f"→ Copiado a interim: {p}  →  {destino}")

def ejecutar_procesamiento() -> bool:
    print("\n=== [2/2] Ejecutando scripts de procesamiento ===")
    ok = run_script_list(SCRIPTS_PROCESAMIENTO, stop_on_fail=True, label="[2/2] Procesamiento")
    if not ok:
        return False
    forzar_salida_en_interim()
    print("✓ Procesamiento terminado y salidas estandarizadas en data/interim")
    return True

# ============================================================
# Punto de entrada
# ============================================================
if __name__ == "__main__":
    # ---- Parte 1: DESCARGA ----
    print("=============================================")
    print("INICIANDO PROCESO DE DESCARGA DE DATOS")
    print("=============================================\n")

    ok_descarga = run_script_list(SCRIPTS_DESCARGA, stop_on_fail=True, label="[1/2] Descarga")
    if not ok_descarga:
        print("\nProceso detenido debido a un error en la descarga.")
        sys.exit(1)

    print("=============================================")
    print("Exito: Todos los scripts de DESCARGA se ejecutaron correctamente.")
    print("=============================================\n")

    # ---- Parte 2: PROCESAMIENTO ----
    ok_proc = ejecutar_procesamiento()
    if not ok_proc:
        print("\nProceso detenido debido a un error en el procesamiento.")
        sys.exit(1)

    print("\n=============================================")
    print("Pipeline completado (Parte 1 + Parte 2).")
    print("Archivos intermedios consolidados en: data/interim/")
    print("=============================================")
>>>>>>> 0461075 (Modificaciones parciales main.py)
