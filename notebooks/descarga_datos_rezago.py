# descargar_datos.py

import pandas as pd
import requests
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
from datetime import datetime

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define la ruta base del proyecto y las carpetas de datos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATA_REFERENCE_DIR = BASE_DIR  / "references"

def crear_directorios():
    """Crea los directorios de datos si no existen."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def obtener_datos_gini():
    """Obtiene los datos del coeficiente de GINI y los guarda en la carpeta raw."""
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
        
        output_path = DATA_RAW_DIR / "coeficiente_gini_desigualdad.csv"
        df.to_csv(output_path, index=False)
        logging.info(f"Datos de GINI guardados exitosamente en: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar los datos de GINI: {e}")
        return False

def descargar_datos_rezago_educativo():
    """Utiliza Selenium para descargar los archivos de Excel en la carpeta raw."""
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
            logging.info(f"Iniciando descarga del archivo: {boton.text.strip()}")
            time.sleep(3)
        
        logging.info("Todas las descargas han sido iniciadas. Esperando 15 segundos para que finalicen...")
        time.sleep(15)
        return True
    except Exception as e:
        logging.error(f"Ocurrió un error durante la descarga con Selenium: {e}")
        return False
    finally:
        driver.quit()
# genera el archibo de texto que describe las fuentes de datos e indica la fech y hora de la descarga   
def generar_log_descarga():
    """Genera un archivo de texto con la descripción de las fuentes de datos."""
    contenido_log = f"""
LOG DE DESCARGA DE DATOS DEL PROYECTO
=====================================
Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este archivo documenta las fuentes de datos utilizadas en el proyecto.
---
### FUENTE 1: Coeficiente de GINI por Entidad Federativa
- Fuente Original: API de DataMexico (Secretaría de Economía).
- Archivo Generado: data/raw/gini_estados_mexico_raw.csv
---
### FUENTE 2: Rezago Educativo por Entidad Federativa, contiene el estimado de población con rezago educativo mayor de 15 años.
- Fuente Original: Instituto Nacional para la Educación de los Adultos (INEA).
- Archivos Generados: Múltiples archivos de Excel (ej. `est_rez_2024_actualizado.xlsx`) en data/raw/.
- contiene los datos de https://www.gob.mx/inea/documentos/rezago-educativo
"""
    ruta_log = DATA_RAW_DIR / "log_descarga_rezago_y_gini.txt"
    try:
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write(contenido_log)
        logging.info(f"Archivo de descripción de fuentes generado exitosamente en: {ruta_log}")
    except Exception as e:
        logging.error(f"No se pudo crear el archivo de log: {e}")

def main():
    """Función principal que orquesta la descarga de los datos."""
    logging.info("--- INICIO DEL SCRIPT DE DESCARGA ---")
    crear_directorios()
    
    gini_exitoso = obtener_datos_gini()
    rezago_exitoso = descargar_datos_rezago_educativo()
    
    if gini_exitoso or rezago_exitoso:
        generar_log_descarga()
    else:
        logging.warning("Ninguna descarga fue exitosa. No se generará el log.")
        
    logging.info("--- FIN DEL SCRIPT DE DESCARGA ---")

if __name__ == "__main__":
    main()