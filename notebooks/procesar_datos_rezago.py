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

def procesar_archivos_rezago():
    """Busca archivos de Excel en 'raw', los procesa, limpia, consolida y luego elimina los originales."""
    logging.info("Iniciando el procesamiento de los archivos de rezago educativo...")
    excel_files = list(DATA_RAW_DIR.glob('est_rez_*.xlsx'))

    if not excel_files:
        logging.warning("No se encontraron archivos de Excel para procesar en 'raw'.")
        return

    all_data = []
    for file_path in excel_files:
        logging.info(f"Procesando el archivo: {file_path.name}")
        match = re.search(r'(\d{4})', file_path.name)
        if match:
            year = int(match.group(1))
            try:
                df = pd.read_excel(file_path, skiprows=8)
                df['Año'] = year
                all_data.append(df)
            except Exception as e:
                logging.error(f"Error al procesar el archivo {file_path.name}: {e}")

    if not all_data:
        logging.error("No se pudieron procesar los datos de ningún archivo de Excel.")
        return

    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df.dropna(subset=['Entidad federativa'], inplace=True)
    merged_df = merged_df[~merged_df['Entidad federativa'].str.contains('Total', na=False)]
    
    if 'Entidad federativa' in merged_df.columns and 'Unnamed: 1' in merged_df.columns:
        merged_df.drop(columns=['Entidad federativa'], inplace=True)
        merged_df.rename(columns={'Unnamed: 1': 'entidad_federativa'}, inplace=True)
    
    output_path_rezago = DATA_RAW_DIR / 'rezago_educativo.csv'
    merged_df.to_csv(output_path_rezago, index=False)
    logging.info(f"Archivo consolidado de rezago educativo guardado en: '{output_path_rezago}'")

    # : Bucle para eliminar los archivos Excel originales para que no esten estirbando en la carpeta ra
    for file_path in excel_files:
        try:
            os.remove(file_path)
            logging.info(f"  -> Eliminado: {file_path.name}")
        except OSError as e:
            logging.error(f"Error al eliminar el archivo {file_path.name}: {e}")
    logging.info("Todos los archivos Excel han sido eliminados.")


def main():
    logging.info("--- INICIO DEL SCRIPT DE PROCESAMIENTO ---")
    crear_directorios()
    
    procesar_datos_gini()
    procesar_archivos_rezago()
    
    logging.info("--- FIN DEL SCRIPT DE PROCESAMIENTO ---")

if __name__ == "__main__":
    main()