# analisis_social.py

import pandas as pd
import requests
import time
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DEL PROYECTO ---
# Define la ruta base del proyecto y las carpetas de datos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Crear directorios si no existen
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def obtener_datos_gini():
    """
    Obtiene los datos del coeficiente de GINI desde la API de DataMexico.
    """
    logging.info("Iniciando la descarga de datos del coeficiente de GINI...")
    url = (
        "https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords"
        "?Year=2010%2C2012%2C2014%2C2016%2C2018%2C2020%2C2022"
        "&cube=coneval_gini_ent"
        "&drilldowns=Year%2CState"
        "&locale=es"
        "&measures=GINI"
    )
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Lanza un error si la solicitud falla
        data = resp.json()

        df = pd.DataFrame(data["data"])
        
        # Renombrar columnas
        df = df.rename(columns={
            "Year": "anio",
            "State ID": "id_estado",
            "State": "estado",
            "GINI": "gini"
        })

        # Convertir a tipos de datos numéricos
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df["gini"] = pd.to_numeric(df["gini"], errors="coerce")

        # Ordenar y guardar
        df = df.sort_values(["estado", "anio"]).reset_index(drop=True)
        
        output_path = DATA_PROCESSED_DIR / "gini_estados_mexico.csv"
        df.to_csv(output_path, index=False)
        logging.info(f"Datos de GINI guardados exitosamente en: {output_path}")
        
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar los datos de GINI: {e}")
        return None

def descargar_datos_rezago_educativo():
    """
    Utiliza Selenium para navegar a la página del gobierno y descargar
    los archivos de Excel sobre el rezago educativo.
    """
    logging.info(f"Configurando la descarga de archivos en: {DATA_RAW_DIR}")

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": str(DATA_RAW_DIR),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.gob.mx/inea/documentos/rezago-educativo")
        time.sleep(5)  # Espera a que la página cargue completamente

        botones = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'Estimación del rezago educativo al 31 de diciembre de')]")
        
        if not botones:
            logging.warning("No se encontraron botones de descarga. El XPath puede haber cambiado.")
            return

        for boton in botones:
            try:
                onclick_attr = boton.get_attribute("onclick")
                if onclick_attr:
                    logging.info(f"Haciendo clic para descargar: {onclick_attr.split(',')[1].strip()}")
                    driver.execute_script("arguments[0].click();", boton)
                    time.sleep(3)  # Pausa para permitir que la descarga inicie
            except Exception as e:
                logging.error(f"No se pudo hacer clic en un botón de descarga: {e}")
        
        logging.info("Todas las descargas han sido iniciadas. Esperando 10 segundos para que finalicen...")
        time.sleep(10)

    finally:
        driver.quit()

def procesar_archivos_rezago():
    """
    Busca archivos de Excel en el directorio 'raw', los procesa,
    los limpia y los consolida en un único archivo CSV.
    """
    logging.info("Iniciando el procesamiento de los archivos de rezago educativo...")
    excel_files = list(DATA_RAW_DIR.glob('est_rez_*.xlsx'))

    if not excel_files:
        logging.warning("No se encontraron archivos de Excel para procesar en la carpeta 'raw'.")
        return None

    all_data = []
    for file_path in excel_files:
        logging.info(f"Procesando el archivo: {file_path.name}")
        match = re.search(r'(\d{4})', file_path.name)
        if match:
            year = int(match.group(1))
            try:
                # Omitir las primeras 8 filas que contienen metadatos
                df = pd.read_excel(file_path, skiprows=8)
                df['Año'] = year
                all_data.append(df)
            except Exception as e:
                logging.error(f"Error al procesar el archivo {file_path.name}: {e}")

    if not all_data:
        logging.error("No se pudieron procesar los datos de ningún archivo de Excel.")
        return None

    # Consolidar todos los DataFrames
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # Limpieza de datos
    merged_df.dropna(subset=['Entidad federativa'], inplace=True)
    merged_df = merged_df[~merged_df['Entidad federativa'].str.contains('Total', na=False)]
    
    # Eliminar columna 'Entidad federativa' (ID) y renombrar la de nombres
    if 'Entidad federativa' in merged_df.columns and 'Unnamed: 1' in merged_df.columns:
        merged_df.drop(columns=['Entidad federativa'], inplace=True)
        merged_df.rename(columns={'Unnamed: 1': 'entidad_federativa'}, inplace=True)
    
    # Guardar el resultado final
    output_path = DATA_PROCESSED_DIR / 'rezago_educativo_consolidado.csv'
    merged_df.to_csv(output_path, index=False)
    logging.info(f"El archivo consolidado y limpio se guardó en: '{output_path}'")
    
    return merged_df


def main():
    """
    Función principal que orquesta la obtención y procesamiento de los datos.
    """
    logging.info("--- INICIO DEL SCRIPT DE ANÁLISIS SOCIAL ---")
    
    # 1. Obtener y procesar datos de GINI
    obtener_datos_gini()
    
    # 2. Descargar archivos de rezago educativo
    descargar_datos_rezago_educativo()
    
    # 3. Procesar y consolidar los archivos descargados
    procesar_archivos_rezago()
    
    logging.info("--- FIN DEL SCRIPT ---")


if __name__ == "__main__":
    main()