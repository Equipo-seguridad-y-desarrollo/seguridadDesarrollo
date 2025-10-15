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
from datetime import datetime 

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
    Obtiene los datos del coeficiente de GINI.
    Devuelve True si la descarga fue exitosa, False en caso contrario.
    """
    logging.info("Iniciando la descarga de datos del coeficiente de GINI...")
    url = (
        "https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords"
        "?Year=2010%2C2012%2C2014%2C2016%2C2018%2C2020%2C2022"
        "&cube=coneval_gini_ent&drilldowns=Year%2CState&locale=es&measures=GINI"
    )
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        df = pd.DataFrame(data["data"])
        
        df = df.rename(columns={
            "Year": "anio", "State ID": "id_estado", "State": "estado", "GINI": "gini"
        })
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df["gini"] = pd.to_numeric(df["gini"], errors="coerce")
        df = df.sort_values(["estado", "anio"]).reset_index(drop=True)
        
        output_path = DATA_RAW_DIR / "gini_estados_mexico.csv"
        df.to_csv(output_path, index=False)
        logging.info(f"Datos de GINI guardados exitosamente en: {output_path}")
        return True 
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar los datos de GINI: {e}")
        return False

def descargar_datos_rezago_educativo():
    """
    Utiliza Selenium para descargar los archivos de Excel.
    Devuelve True si fue exitoso, False si no.
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
        time.sleep(5)
        botones = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'Estimación del rezago educativo al 31 de diciembre de')]")
        
        if not botones:
            logging.warning("No se encontraron botones de descarga. El XPath puede haber cambiado.")
            return False
            
        for boton in botones:
            driver.execute_script("arguments[0].click();", boton)
            time.sleep(3)
        
        logging.info("Todas las descargas han sido iniciadas. Esperando 10 segundos para que finalicen...")
        time.sleep(10)
        return True 
    except Exception as e:
        logging.error(f"Ocurrió un error durante la descarga con Selenium: {e}")
        return False
    finally:
        driver.quit()

def generar_log_descarga():
    """Genera un archivo de texto con la descripción de las fuentes de datos."""
    contenido_log = f"""
LOG DE DESCARGA DE DATOS DEL PROYECTO
=====================================

Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este archivo documenta las fuentes de datos utilizadas en el proyecto,
la fecha de su descarga y una breve descripción de su naturaleza.

---
### FUENTE 1: Coeficiente de GINI por Entidad Federativa

- **Fuente Original**: API de DataMexico (Secretaría de Economía).
- **Descripción**: El coeficiente de GINI es una medida de la desigualdad económica. Un valor de 0 representa una igualdad de ingresos perfecta, mientras que un valor de 1 representa una desigualdad perfecta (donde una persona concentra todos los ingresos). Estos datos nos ayudan a entender la distribución de la riqueza por estado.
- **Enlace de la Fuente**: https://www.economia.gob.mx/datamexico/
- **Archivo Generado**: data/raw/gini_estados_mexico_raw.csv

---
### FUENTE 2: Rezago Educativo por Entidad Federativa

- **Fuente Original**: Instituto Nacional para la Educación de los Adultos (INEA), a través de la plataforma gob.mx.
- **Descripción**: Los datos miden el porcentaje de la población que no ha completado la educación básica (analfabetismo, sin primaria terminada, sin secundaria terminada). Es un indicador clave del nivel de desarrollo social y acceso a oportunidades.
- **Enlace de la Fuente**: https://www.gob.mx/inea/documentos/rezago-educativo
- **Archivos Generados**: Múltiples archivos de Excel (ej. `est_rez_2024_actualizado.xlsx`) que luego se procesan.

"""
    ruta_log = DATA_RAW_DIR / "log_descarga.txt"
    try:
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write(contenido_log)
        logging.info(f"Archivo de descripción de fuentes generado exitosamente en: {ruta_log}")
    except Exception as e:
        logging.error(f"No se pudo crear el archivo de log: {e}")


def procesar_archivos_rezago():
    """
    Busca archivos de Excel en el directorio 'raw', los procesa,
    los limpia y los consolida en un único archivo CSV.
    """
    logging.info("Iniciando el procesamiento de los archivos de rezago educativo...")
    excel_files = list(DATA_RAW_DIR.glob('est_rez_*.xlsx'))

    if not excel_files:
        logging.warning("No se encontraron archivos de Excel para procesar en la carpeta 'raw'.")
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
    
    output_path = DATA_RAW_DIR / 'rezago_educativo_consolidado.csv'
    merged_df.to_csv(output_path, index=False)
    logging.info(f"El archivo consolidado y limpio se guardó en: '{output_path}'")


def main():
    """
    Función principal que orquesta la obtención y procesamiento de los datos.
    """
    logging.info("--- INICIO DEL SCRIPT DE ANÁLISIS SOCIAL ---")
    

    
    # 1. Ejecutar las descargas y guardar si fueron exitosas
    gini_exitoso = obtener_datos_gini()
    rezago_exitoso = descargar_datos_rezago_educativo()
    
    # 2. Si alguna de las descargas funcionó, se genera el log
    if gini_exitoso or rezago_exitoso:
        generar_log_descarga()
    else:
        logging.warning("Ninguna descarga fue exitosa. No se generará el log.")
    
    # 3. Si la descarga de archivos de rezago fue exitosa, se procesan
    if rezago_exitoso:
        procesar_archivos_rezago()
    
    logging.info("--- FIN DEL SCRIPT ---")


if __name__ == "__main__":
    main()