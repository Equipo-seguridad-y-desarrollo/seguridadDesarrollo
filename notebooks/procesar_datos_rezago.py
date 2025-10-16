# procesar_datos.py

import pandas as pd
import re
from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define la ruta base del proyecto y las carpetas de datos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

def crear_directorios():
    """Crea los directorios de datos si no existen."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def procesar_datos_gini():
    """Lee los datos crudos de GINI, los limpia, guarda la nueva versión en 'raw' y elimina la original."""
    logging.info("Procesando datos de GINI...")
    input_path = DATA_RAW_DIR / "coeficiente_gini_desigualdad.csv"
    output_path = DATA_RAW_DIR / "gini_desigualdad_procesado.csv"

    if not input_path.exists():
        logging.warning(f"No se encontró el archivo de GINI en {input_path}. Saltando procesamiento.")
        return

    df = pd.read_csv(input_path)
    
    df = df.rename(columns={
        "Year": "anio", "State ID": "id_estado", "State": "estado", "GINI": "gini"
    })
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df["gini"] = pd.to_numeric(df["gini"], errors="coerce")
    df = df.sort_values(["estado", "anio"]).reset_index(drop=True)
    
    # Guardar el archivo procesado
    df.to_csv(output_path, index=False)
    logging.info(f"Datos de GINI procesados y guardados en: {output_path}")

    # Eliminar el archivo original
    try:
        os.remove(input_path)
        logging.info(f"Archivo original '{input_path.name}' eliminado exitosamente.")
    except OSError as e:
        logging.error(f"Error al eliminar el archivo {input_path.name}: {e}")

def main():
    logging.info("--- INICIO DEL SCRIPT DE PROCESAMIENTO ---")
    crear_directorios()
    
    procesar_datos_gini()
    
    logging.info("--- FIN DEL SCRIPT DE PROCESAMIENTO ---")

if __name__ == "__main__":
    main()