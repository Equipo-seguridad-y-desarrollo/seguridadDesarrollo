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
Parte 2: Procesamiento y normalizacion de salidas a data/interim
Todos los prints estan en ASCII (sin acentos ni emojis) para evitar caracteres raros en Windows.
"""

import sys
import os
import subprocess
from pathlib import Path
import shutil
import glob
import time
from typing import List, Optional, Tuple

# ============================================================
# Configuracion base
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
def ejecutar_script(ruta_script: str, timeout: Optional[int] = None) -> bool:
    """
    Ejecuta un script de Python y muestra su salida.
    Ejecuta con cwd la carpeta del script, para que sus rutas relativas funcionen.
    Fuerza UTF-8 en el subproceso para que no truene por UnicodeEncodeError,
    pero todos nuestros prints estan en ASCII por compatibilidad.
    """
    script_path = Path(ruta_script)
    if not script_path.exists():
<<<<<<< HEAD
>>>>>>> 0461075 (Modificaciones parciales main.py)
        print(f"Error: No se encontró el archivo en la ruta '{ruta_script}'.")
=======
        print(f"Error: No se encontro el archivo en la ruta '{ruta_script}'.")
>>>>>>> 8ef7b5c (Modificaciones finales para el pipeline de main.py, datos crudos y formateo de datos en datos intermedios)
        return False

    print(f"Iniciando ejecucion de: {ruta_script}")
    try:
<<<<<<< HEAD
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
=======
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

>>>>>>> 8ef7b5c (Modificaciones finales para el pipeline de main.py, datos crudos y formateo de datos en datos intermedios)
        resultado = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(script_path.parent),  # ejecutar desde la carpeta del script
            timeout=timeout,
            env=env,
        )
        if resultado.stdout:
            # stdout puede traer acentos desde los scripts; lo imprimimos tal cual.
            # La consola puede no renderizar, pero no deberia fallar.
            print(resultado.stdout)
<<<<<<< HEAD
>>>>>>> 0461075 (Modificaciones parciales main.py)
=======
        if resultado.stderr:
            # Mostrar warnings si los hay
            print(resultado.stderr, file=sys.stderr)
>>>>>>> 8ef7b5c (Modificaciones finales para el pipeline de main.py, datos crudos y formateo de datos en datos intermedios)
        print(f"Finalizado: {ruta_script} se ejecuto correctamente.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {ruta_script}.")
        print(f"El script finalizo con un error (codigo de salida {e.returncode}).")
        print("Salida de error (stderr):")
<<<<<<< HEAD
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
=======
        try:
            print(e.stderr)
        except Exception:
            print(str(e.stderr).encode("utf-8", "replace").decode("utf-8", "replace"))
>>>>>>> 8ef7b5c (Modificaciones finales para el pipeline de main.py, datos crudos y formateo de datos en datos intermedios)
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout ejecutando {ruta_script}")
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
    BASE_DIR,                          # raiz
    BASE_DIR / "scripts",
    BASE_DIR / "notebooks",
    BASE_DIR / "src",
    BASE_DIR / "etl",
    BASE_DIR / "processing",
]

def resolve_script_path(name_or_rel: str) -> Optional[Path]:
    """
    Busca un script por nombre (por ej. 'procesar_datos_rezago.py') o ruta relativa.
    Retorna Path si lo encuentra; None si no.
    """
    p = Path(name_or_rel)
    if p.is_file():
        return p.resolve()

    for d in CANDIDATE_DIRS:
        cand = d / name_or_rel
        if cand.is_file():
            return cand.resolve()

    exclude = {".git", ".venv", "venv", "__pycache__", "data"}
    try:
        for q in BASE_DIR.rglob("*"):
            if q.is_file() and q.name == Path(name_or_rel).name and not any(part in exclude for part in q.parts):
                return q.resolve()
    except Exception:
        pass
    return None

def suggest_similar_scripts(basename: str) -> List[str]:
    """
    Si no se encuentra el script, sugiere coincidencias por subcadena.
    """
    hits: List[str] = []
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

def run_script_list(scripts: List[str], stop_on_fail: bool = True, label: str = "Ejecucion") -> bool:
    """
    Resuelve rutas y ejecuta una lista de scripts en orden.
    """
    print(f"\n=== {label} ===")
    for fname in scripts:
        ruta = resolve_script_path(fname)
        if ruta is None:
            print(f"No se encontro '{fname}' en el proyecto.")
            sugerencias = suggest_similar_scripts(Path(fname).name)
            if sugerencias:
                print("Sugerencias:")
                for s in sugerencias:
                    print(f" - {s}")
            if stop_on_fail:
                return False
            else:
                continue

        # Paso especifico antes de ejecutar 'procesado_inegi_edu.py'
        if Path(fname).name == "procesado_inegi_edu.py":
            if not alias_inegi_edu_input():
                print("No se pudo preparar data/raw/educacionysalud.csv")
                return False

        ok = ejecutar_script(str(ruta))
        if not ok and stop_on_fail:
            print(f"Fallo la ejecucion en: {ruta}")
            return False
    return True

# ============================================================
# Parte 1: Descarga de datos (tu lista original)
# ============================================================
SCRIPTS_DESCARGA = [
    "notebooks/1_variables_economicas_descarga_datos_crudos.py",
    "notebooks/descarga_datos_rezago.py",
    "notebooks/importacion_inegi_edu.py",
    "notebooks/datos_seguridad_mexico.py",
]

# ============================================================
# Parte 2: Procesamiento y normalizacion en data/interim
# ============================================================
SCRIPTS_PROCESAMIENTO = [
    "procesar_datos_rezago.py",
    "2_variables_economicas_procesar_datos_formateados.py",
    "procesado_inegi_edu.py",
    "procesar_datos_seguridad.py",
]

def alias_inegi_edu_input() -> bool:
    """
    Si existe data/raw/educacionysalud_raw.csv, crea/actualiza
    data/raw/educacionysalud.csv (el nombre que espera 'procesado_inegi_edu.py').
    """
    raw_dir = RAW_DIR
    src = raw_dir / "educacionysalud_raw.csv"
    dst = raw_dir / "educacionysalud.csv"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
            print(f"Alias creado para INEGI EDU:\n  {src}\n  -> {dst}")
            return True
        except Exception as e:
            print(f"No se pudo crear alias {dst} desde {src}: {e}")
            return False
    else:
        print(f"No se encontro {src}. Verifica que la parte 1 lo genero.")
        return False

def _same_file(src: Path, dst: Path) -> bool:
    if not dst.exists():
        return False
    try:
        s = src.stat()
        d = dst.stat()
        # Mismo tamano y misma precision de mtime (redondeada a 1 seg)
        return (s.st_size == d.st_size) and (int(s.st_mtime) == int(d.st_mtime))
    except Exception:
        return False

def safe_copy(src: Path, dst: Path, retries: int = 6, delay: float = 0.8) -> None:
    """
    Copia de forma robusta en Windows con reintentos.
    - Omite si destino ya es identico (tamano y mtime).
    - Reintenta ante PermissionError (archivo en uso).
    - Ultimo recurso: copia a .tmp y os.replace.
    """
    if src.resolve() == dst.resolve():
        # Mismo archivo exacto
        print(f"Salto copia, origen y destino son iguales: {src}")
        return

    if _same_file(src, dst):
        # Ya esta igual, no copiamos
        print(f"Salto copia, destino ya coincide: {dst}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)

    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            # Intento directo
            shutil.copy2(src, dst)
            return
        except PermissionError as e:
            last_err = e
            print(f"Advertencia: destino en uso, reintentando copia ({attempt}/{retries}) -> {dst}")
            time.sleep(delay)
        except Exception as e:
            last_err = e
            print(f"Advertencia: error copiando (intento {attempt}/{retries}) -> {dst}: {e}")
            time.sleep(delay)

    # Ultimo recurso: copiar a temporal y reemplazar
    try:
        tmp = dst.with_suffix(dst.suffix + ".tmp_copy")
        if tmp.exists():
            try:
                tmp.unlink()
            except Exception:
                pass
        shutil.copyfile(src, tmp)
        try:
            shutil.copystat(src, tmp)
        except Exception:
            pass
        os.replace(tmp, dst)
    except Exception as e:
        # Si aun falla, levantamos el ultimo error conocido
        raise last_err if last_err else e

def copiar_a_interim(origen: Path, destino: Path) -> None:
    safe_copy(origen, destino)

def forzar_salida_en_interim():
    """
    Copia a data/interim TODO lo que haya quedado en:
      - data/processed/**/*.csv
      - data/raw/*procesad*.csv  (ej. gini_desigualdad_procesado.csv)
      - data/interim/**/*.csv
    No borra origen; solo duplica en interim.
    Evita recopiados innecesarios y maneja archivos bloqueados con reintentos.
    """
    patrones = [
        str(PROCESSED_DIR / "**" / "*.csv"),
        str(RAW_DIR / "*procesad*.csv"),
        str(INTERIM_DIR / "**" / "*.csv"),
    ]
    vistos = set()
    for patron in patrones:
        for ruta in glob.glob(patron, recursive=True):
            p = Path(ruta)
            if not p.is_file():
                continue
            destino = INTERIM_DIR / p.name
            clave = (str(p.resolve()), str(destino.resolve()))
            if clave in vistos:
                continue
            try:
                copiar_a_interim(p, destino)
                print(f"Copiado a interim: {p} -> {destino}")
            except PermissionError as e:
                print(f"No se pudo copiar (permiso): {p} -> {destino}: {e}")
            except Exception as e:
                print(f"No se pudo copiar: {p} -> {destino}: {e}")
            vistos.add(clave)

    print("Limpiando carpeta data/processed ...")
    for file in PROCESSED_DIR.glob("**/*"):
        try:
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(f"Advertencia: no se pudo borrar {file}: {e}")
    print("Carpeta data/processed vaciada.")

def ejecutar_procesamiento() -> bool:
    print("\n=== [2/2] Ejecutando scripts de procesamiento ===")
    ok = run_script_list(SCRIPTS_PROCESAMIENTO, stop_on_fail=True, label="[2/2] Procesamiento")
    if not ok:
        return False
    forzar_salida_en_interim()
    print("Procesamiento terminado y salidas estandarizadas en data/interim")
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
<<<<<<< HEAD
    print("Pipeline completado (Parte 1 + Parte 2).")
    print("Archivos intermedios consolidados en: data/interim/")
    print("=============================================")
>>>>>>> 0461075 (Modificaciones parciales main.py)
=======
    print("Pipeline completado")
    print("=============================================")
>>>>>>> 8ef7b5c (Modificaciones finales para el pipeline de main.py, datos crudos y formateo de datos en datos intermedios)
