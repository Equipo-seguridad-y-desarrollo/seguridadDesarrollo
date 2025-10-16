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
from typing import List, Optional, Dict

# ============================================================
# Configuracion base
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
for d in (RAW_DIR, INTERIM_DIR, PROCESSED_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# Mapeo de CWD por script (override)
#   - BASE  : ejecutar con cwd = BASE_DIR (raiz del repo)
#   - SCRIPT: ejecutar con cwd = carpeta del script
#   - omitido/otros -> SCRIPT por defecto
# ============================================================
CWD_OVERRIDE: Dict[str, str] = {
    "1_variables_economicas_descarga_datos_crudos.py": "BASE",
    "2_variables_economicas_procesar_datos_formateados.py": "BASE",
    "procesado_inegi_edu.py": "SCRIPT",      # requiere ../data/...
    # "procesar_datos_seguridad.py": "SCRIPT",  # por defecto
}

# ============================================================
# Utilidades comunes
# ============================================================
def _get_cwd_for_script(script_path: Path) -> str:
    name = script_path.name
    mode = CWD_OVERRIDE.get(name, "SCRIPT")
    return str(BASE_DIR) if mode == "BASE" else str(script_path.parent)

def ejecutar_script(ruta_script: str, timeout: Optional[int] = None) -> bool:
    """
    Ejecuta un script de Python y muestra su salida.
    Aplica override de CWD segun CWD_OVERRIDE.
    Fuerza UTF-8 en el subproceso para evitar problemas de encoding.
    """
    script_path = Path(ruta_script)
    if not script_path.exists():
        print(f"Error: No se encontro el archivo en la ruta '{ruta_script}'.")
        return False

    run_cwd = _get_cwd_for_script(script_path)
    print(f"Iniciando ejecucion de: {ruta_script}")
    print(f" - cwd: {run_cwd}")
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

        resultado = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            cwd=run_cwd,
            timeout=timeout,
            env=env,
        )
        if resultado.stdout:
            print(resultado.stdout)
        if resultado.stderr:
            print(resultado.stderr, file=sys.stderr)
        print(f"Finalizado: {ruta_script} se ejecuto correctamente.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {ruta_script}.")
        print(f"El script finalizo con un error (codigo de salida {e.returncode}).")
        print("Salida de error (stderr):")
        try:
            print(e.stderr)
        except Exception:
            print(str(e.stderr).encode("utf-8", "replace").decode("utf-8", "replace"))
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout ejecutando {ruta_script}")
        return False
    except Exception as e:
        print(f"Ocurrio un error inesperado con {ruta_script}: {e}")
        return False


# Directorios candidatos para buscar scripts si solo se da el nombre
CANDIDATE_DIRS = [
    BASE_DIR,
    BASE_DIR / "scripts",
    BASE_DIR / "notebooks",
    BASE_DIR / "src",
    BASE_DIR / "etl",
    BASE_DIR / "processing",
]

def resolve_script_path(name_or_rel: str) -> Optional[Path]:
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
# Parte 1: Descarga de datos
# ============================================================
SCRIPTS_DESCARGA = [
    "notebooks/1_variables_economicas_descarga_datos_crudos.py",
    "notebooks/descarga_datos_rezago.py",
    "notebooks/importacion_inegi_edu.py",
    "notebooks/datos_seguridad_mexico.py",
]

# ============================================================
# Parte 2: Procesamiento y normalizacion
# ============================================================
SCRIPTS_PROCESAMIENTO = [
    "procesar_datos_rezago.py",
    "2_variables_economicas_procesar_datos_formateados.py",
    "procesado_inegi_edu.py",
    "procesar_datos_seguridad.py",
]

# ============================================================
# Utilidades de archivos: alias y copias robustas
# ============================================================
def alias_inegi_edu_input() -> bool:
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
        return (s.st_size == d.st_size) and (int(s.st_mtime) == int(d.st_mtime))
    except Exception:
        return False

def safe_copy(src: Path, dst: Path, retries: int = 6, delay: float = 0.8) -> None:
    if src.resolve() == dst.resolve():
        print(f"Salto copia, origen y destino son iguales: {src}")
        return
    if _same_file(src, dst):
        print(f"Salto copia, destino ya coincide: {dst}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
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
        raise last_err if last_err else e

def copiar_a_interim(origen: Path, destino: Path) -> None:
    safe_copy(origen, destino)

# ============================================================
# Normalizacion de data/ sombreados (*/data/...)
# ============================================================
def _iter_shadow_data_dirs(kind: str):
    """
    Itera sobre rutas del tipo */data/<kind> que no sean la raiz BASE_DIR/data/<kind>.
    kind: 'raw' | 'processed' | 'interim'
    """
    target_root = (DATA_DIR / kind).resolve()
    for p in BASE_DIR.rglob(f"data/{kind}"):
        try:
            if p.resolve() == target_root:
                continue
        except Exception:
            pass
        yield p

def _move_all(from_dir: Path, to_dir: Path, exts: Optional[List[str]] = None, remove_source: bool = True, label: str = ""):
    """
    Mueve todos los archivos (filtrando por extensiones si se dan) de from_dir a to_dir.
    Si existe conflicto, conserva el mas reciente en destino.
    """
    to_dir.mkdir(parents=True, exist_ok=True)
    patterns = ["*"] if not exts else [f"*{e}" for e in exts]
    found = False
    for pat in patterns:
        for src in from_dir.glob(pat):
            if not src.is_file():
                continue
            found = True
            dst = to_dir / src.name
            try:
                if dst.exists():
                    s_m = src.stat().st_mtime
                    d_m = dst.stat().st_mtime
                    if s_m <= d_m:
                        print(f"{label} - Omitido (ya existe mas nuevo en destino): {src}")
                        if remove_source:
                            try:
                                src.unlink()
                            except Exception:
                                pass
                        continue
                shutil.copy2(src, dst)
                print(f"{label} - {src} -> {dst}")
                if remove_source:
                    try:
                        src.unlink()
                    except Exception:
                        pass
            except Exception as e:
                print(f"{label} - Advertencia: no se pudo mover {src} -> {dst}: {e}")
    # limpia directorios vacios
    if found and remove_source:
        try:
            for sub in sorted(from_dir.glob("**/*"), reverse=True):
                if sub.is_dir():
                    try:
                        sub.rmdir()
                    except Exception:
                        pass
            from_dir.rmdir()
        except Exception:
            pass

def mover_raw_extraviados():
    """
    Tras Parte 1: mueve cualquier archivo crudo que haya quedado en */data/raw
    hacia data/raw en raiz (csv, xlsx, parquet, txt, log).
    """
    print("Normalizando ubicacion de data/raw ...")
    for shadow in _iter_shadow_data_dirs("raw"):
        _move_all(
            from_dir=shadow,
            to_dir=RAW_DIR,
            exts=[".csv", ".xlsx", ".xls", ".parquet", ".feather", ".txt", ".log"],
            label="RAW"
        )

def normalizar_processed_e_interim_sombreados():
    """
    Tras Parte 2: mueve archivos de */data/processed y */data/interim a las
    carpetas raiz correspondientes antes de copiar a data/interim final.
    """
    print("Normalizando ubicacion de data/processed ...")
    for shadow in _iter_shadow_data_dirs("processed"):
        _move_all(
            from_dir=shadow,
            to_dir=PROCESSED_DIR,
            exts=[".csv", ".xlsx", ".parquet", ".feather", ".txt", ".log"],
            label="PROC"
        )
    print("Normalizando ubicacion de data/interim ...")
    for shadow in _iter_shadow_data_dirs("interim"):
        _move_all(
            from_dir=shadow,
            to_dir=INTERIM_DIR,
            exts=[".csv", ".xlsx", ".parquet", ".feather", ".txt", ".log"],
            label="INTM",
            remove_source=False  # mantenemos espejos si ya estaban en root
        )

# ============================================================
# Copia final a data/interim y limpieza de processed
# ============================================================
def forzar_salida_en_interim():
    """
    1) Normaliza directorios sombreados (*/data/processed, */data/interim).
    2) Copia a data/interim todo lo que haya en processed (raiz) y los *_procesad*.csv del raw.
    3) Limpia data/processed (archivos y subcarpetas vacias).
    """
    normalizar_processed_e_interim_sombreados()

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

    # Limpieza de la carpeta processed (raiz)
    print("Limpiando carpeta data/processed ...")
    for file in sorted(PROCESSED_DIR.glob("**/*"), reverse=True):
        try:
            if file.is_file():
                file.unlink()
            elif file.is_dir():
                file.rmdir()
        except Exception as e:
            print(f"Advertencia: no se pudo borrar {file}: {e}")
    print("Carpeta data/processed vaciada.")

# ============================================================
# Ejecucion principal
# ============================================================
def ejecutar_procesamiento() -> bool:
    print("\n=== [2/2] Ejecutando scripts de procesamiento ===")
    ok = run_script_list(SCRIPTS_PROCESAMIENTO, stop_on_fail=True, label="[2/2] Procesamiento")
    if not ok:
        return False
    forzar_salida_en_interim()
    print("Procesamiento terminado y salidas estandarizadas en data/interim")
    return True

if __name__ == "__main__":
    # ---- Parte 1 ----
    print("=============================================")
    print("INICIANDO PROCESO DE DESCARGA DE DATOS")
    print("=============================================\n")

    ok_descarga = run_script_list(SCRIPTS_DESCARGA, stop_on_fail=True, label="[1/2] Descarga")
    if not ok_descarga:
        print("\nProceso detenido debido a un error en la descarga.")
        sys.exit(1)

    # Reubicar cualquier archivo que haya quedado en */data/raw (incluye logs)
    mover_raw_extraviados()

    print("=============================================")
    print("Exito: Todos los scripts de DESCARGA se ejecutaron correctamente.")
    print("=============================================\n")

    # ---- Parte 2 ----
    ok_proc = ejecutar_procesamiento()
    if not ok_proc:
        print("\nProceso detenido debido a un error en el procesamiento.")
        sys.exit(1)

    print("\n=============================================")
    print("Pipeline completado")
    print("=============================================")