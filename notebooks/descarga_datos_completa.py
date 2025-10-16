"""
Script Unificado de Descarga de Datos del Proyecto
====================================================
Este script consolida la descarga de todos los datos necesarios para el proyecto:
- Datos de Seguridad (INEGI y SESNSP)
- Datos de Educación y Salud (INEGI)
- Variables Económicas (DataMexico/Secretaría de Economía)
- Coeficiente de GINI (CONEVAL/DataMexico)

Requisitos:
- Token de API de INEGI (configurar en .env o pasar como argumento)
- Librerías: requests, pandas, python-dotenv

Uso:
    python descarga_datos_completa.py --token TU_TOKEN_AQUI
    
    o con .env:
    python descarga_datos_completa.py
"""

import os
import sys
import argparse
import logging
import json
import csv
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import requests

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configurar rutas del proyecto
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_REFERENCES_DIR = PROJECT_ROOT / "references"

# Crear directorios si no existen
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_REFERENCES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# UTILIDADES GENERALES
# ============================================================================

def guardar_json_a_csv(datos_lista, archivo_salida):
    """Convierte una lista de diccionarios JSON a CSV."""
    if not datos_lista:
        return False

    fieldnames = datos_lista[0].keys()
    try:
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(datos_lista)
        return True
    except Exception as e:
        logging.error(f"Error al guardar CSV: {e}")
        return False


# ============================================================================
# MÓDULO 1: DATOS DE SEGURIDAD
# ============================================================================

def descargar_percepcion_inseguridad(token):
    """
    Descarga datos de percepción de inseguridad de INEGI (ENVIPE 2011-2025).
    
    Returns:
        tuple: (DataFrame con datos, diccionario con metadata)
    """
    logging.info("=== Iniciando descarga: Percepción de Inseguridad ===")
    
    clave_indicador = "6204327085"
    entidades = {
        "00": "Nacional", "01": "Aguascalientes", "02": "Baja California",
        "03": "Baja California Sur", "04": "Campeche", "05": "Coahuila",
        "06": "Colima", "07": "Chiapas", "08": "Chihuahua",
        "09": "Ciudad de México", "10": "Durango", "11": "Guanajuato",
        "12": "Guerrero", "13": "Hidalgo", "14": "Jalisco",
        "15": "México", "16": "Michoacán", "17": "Morelos",
        "18": "Nayarit", "19": "Nuevo León", "20": "Oaxaca",
        "21": "Puebla", "22": "Querétaro", "23": "Quintana Roo",
        "24": "San Luis Potosí", "25": "Sinaloa", "26": "Sonora",
        "27": "Tabasco", "28": "Tamaulipas", "29": "Tlaxcala",
        "30": "Veracruz", "31": "Yucatán", "32": "Zacatecas"
    }
    
    all_data = []
    for clave, nombre in entidades.items():
        url = (
            f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/"
            f"{clave_indicador}/es/{clave}/false/BISE/2.0/{token}?type=json"
        )
        try:
            response = requests.get(url, timeout=7)
            json_data = response.json()
            if "Series" in json_data and json_data["Series"]:
                serie = json_data["Series"][0]["OBSERVATIONS"]
                df = pd.DataFrame(serie)
                df["año"] = df["TIME_PERIOD"].astype(int)
                df["valor"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
                df["entidad"] = nombre
                df["clave"] = clave
                df = df[["año", "valor", "entidad", "clave"]]
                all_data.append(df)
                logging.info(f"  ✓ {nombre}")
            else:
                logging.warning(f"  ✗ Sin datos para {nombre}")
        except Exception as e:
            logging.error(f"  ✗ Error en {nombre}: {e}")
    
    df_final = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    
    metadata = {
        'nombre': 'Indicador de Percepción de Inseguridad',
        'fuente': 'INEGI - ENVIPE',
        'archivo': 'indicador_inseguridad_estados.csv',
        'registros': len(df_final),
        'descripcion': 'Tasa de personas 18+ que perciben inseguridad por cada 100,000 habitantes'
    }
    
    return df_final, metadata


def descargar_incidencia_delictiva():
    """
    Descarga datos de incidencia delictiva del SESNSP (2015-2025).
    
    Returns:
        tuple: (DataFrame con datos, diccionario con metadata)
    """
    logging.info("=== Iniciando descarga: Incidencia Delictiva ===")
    
    url = "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv"
    
    try:
        df = pd.read_csv(url)
        estado = 'Exitoso'
        registros = len(df)
        logging.info(f"  ✓ Descargado: {registros} registros")
    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        df = pd.DataFrame()
        estado = f'Error: {str(e)}'
        registros = 0
    
    metadata = {
        'nombre': 'Incidencia Delictiva Estatal',
        'fuente': 'SESNSP',
        'archivo': 'incidencia_delictiva_estatal_2015_2025.csv',
        'registros': registros,
        'descripcion': 'Hechos delictivos mensuales por entidad federativa (ene 2015 - ago 2025)'
    }
    
    return df, metadata


# ============================================================================
# MÓDULO 2: DATOS DE EDUCACIÓN Y SALUD
# ============================================================================

def descargar_educacion_salud(token):
    """
    Descarga indicadores de educación y salud de INEGI.
    
    Returns:
        tuple: (DataFrame con datos, diccionario con metadata)
    """
    logging.info("=== Iniciando descarga: Educación y Salud ===")
    
    indicadores = {
        '3108001001': 'Porcentaje analfabetismo',
        '1005000038': 'Promedio escolaridad',
        '6200205239': 'Poblacion con educacion basica',
        '6200205241': 'Poblacion con bachillerato',
        '6200205242': 'Poblacion con estudios superiores',
        '6207019020': 'Porcentaje sin escolaridad',
        '1004000001': 'Derechohabientes'
    }
    
    estados = {
        "Aguascalientes": "01", "Baja California": "02", "Baja California Sur": "03",
        "Campeche": "04", "Coahuila de Zaragoza": "05", "Colima": "06",
        "Chiapas": "07", "Chihuahua": "08", "Ciudad de México": "09",
        "Durango": "10", "Guanajuato": "11", "Guerrero": "12",
        "Hidalgo": "13", "Jalisco": "14", "México": "15",
        "Michoacán de Ocampo": "16", "Morelos": "17", "Nayarit": "18",
        "Nuevo León": "19", "Oaxaca": "20", "Puebla": "21",
        "Querétaro": "22", "Quintana Roo": "23", "San Luis Potosí": "24",
        "Sinaloa": "25", "Sonora": "26", "Tabasco": "27",
        "Tamaulipas": "28", "Tlaxcala": "29", "Veracruz": "30",
        "Yucatán": "31", "Zacatecas": "32"
    }
    
    indicadores_str = ",".join(indicadores.keys())
    valores = []
    
    for estado, clave in estados.items():
        url = (
            f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
            f"INDICATOR/{indicadores_str}/es/{clave}/false/BISE/2.0/{token}?type=json"
        )
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            for indicador in data['Series']:
                for observacion in indicador['OBSERVATIONS']:
                    valores.append({
                        "id_estado": clave,
                        "estado": estado,
                        "indicador": indicador['INDICADOR'],
                        "indicador_nombre": indicadores[indicador['INDICADOR']],
                        "año": observacion['TIME_PERIOD'],
                        "valor": observacion['OBS_VALUE']
                    })
            logging.info(f"  ✓ {estado}")
        except Exception as e:
            logging.error(f"  ✗ Error en {estado}: {e}")
    
    df = pd.DataFrame(valores)
    
    metadata = {
        'nombre': 'Indicadores de Educación y Salud',
        'fuente': 'INEGI - Banco de Indicadores',
        'archivo': 'educacionysalud_raw.csv',
        'registros': len(df),
        'descripcion': f'{len(indicadores)} indicadores de educación y salud por estado'
    }
    
    return df, metadata


# ============================================================================
# MÓDULO 3: VARIABLES ECONÓMICAS
# ============================================================================

def descargar_ied():
    """Descarga Inversión Extranjera Directa por estado."""
    logging.info("=== Iniciando descarga: Inversión Extranjera Directa ===")
    
    estados_ids = {
        1: 'Aguascalientes', 2: 'Baja California', 3: 'Baja California Sur',
        4: 'Campeche', 5: 'Coahuila de Zaragoza', 6: 'Colima',
        7: 'Chiapas', 8: 'Chihuahua', 9: 'Ciudad de México',
        10: 'Durango', 11: 'Guanajuato', 12: 'Guerrero',
        13: 'Hidalgo', 14: 'Jalisco', 15: 'México',
        16: 'Michoacán de Ocampo', 17: 'Morelos', 18: 'Nayarit',
        19: 'Nuevo León', 20: 'Oaxaca', 21: 'Puebla',
        22: 'Querétaro', 23: 'Quintana Roo', 24: 'San Luis Potosí',
        25: 'Sinaloa', 26: 'Sonora', 27: 'Tabasco',
        28: 'Tamaulipas', 29: 'Tlaxcala', 30: 'Veracruz de Ignacio de la Llave',
        31: 'Yucatán', 32: 'Zacatecas'
    }
    
    datos_totales = []
    for id_estado, nombre in estados_ids.items():
        url = (
            f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
            "&cube=fdi_2_state_investment&drilldowns=Quarter,State&locale=es"
            "&measures=Investment&parents=false"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    datos_totales.extend(data)
                    logging.info(f"  ✓ {nombre}")
        except Exception as e:
            logging.error(f"  ✗ Error en {nombre}: {e}")
    
    metadata = {
        'nombre': 'Inversión Extranjera Directa',
        'fuente': 'DataMexico - Secretaría de Economía',
        'archivo': 'ied_raw.csv',
        'registros': len(datos_totales),
        'descripcion': 'IED trimestral por entidad federativa'
    }
    
    return datos_totales, metadata


def descargar_salario():
    """Descarga salario mensual por estado."""
    logging.info("=== Iniciando descarga: Salario Mensual ===")
    
    estados_ids = {
        1: 'Aguascalientes', 2: 'Baja California', 3: 'Baja California Sur',
        4: 'Campeche', 5: 'Coahuila de Zaragoza', 6: 'Colima',
        7: 'Chiapas', 8: 'Chihuahua', 9: 'Ciudad de México',
        10: 'Durango', 11: 'Guanajuato', 12: 'Guerrero',
        13: 'Hidalgo', 14: 'Jalisco', 15: 'México',
        16: 'Michoacán de Ocampo', 17: 'Morelos', 18: 'Nayarit',
        19: 'Nuevo León', 20: 'Oaxaca', 21: 'Puebla',
        22: 'Querétaro', 23: 'Quintana Roo', 24: 'San Luis Potosí',
        25: 'Sinaloa', 26: 'Sonora', 27: 'Tabasco',
        28: 'Tamaulipas', 29: 'Tlaxcala', 30: 'Veracruz de Ignacio de la Llave',
        31: 'Yucatán', 32: 'Zacatecas'
    }
    
    datos_totales = []
    for id_estado, nombre in estados_ids.items():
        url = (
            f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
            "&Population+Classification=1&cube=inegi_enoe&drilldowns=State,Quarter"
            "&measures=Monthly+Wage,Workforce&locale=es&parents=false"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    datos_totales.extend(data)
                    logging.info(f"  ✓ {nombre}")
        except Exception as e:
            logging.error(f"  ✗ Error en {nombre}: {e}")
    
    metadata = {
        'nombre': 'Salario Mensual',
        'fuente': 'DataMexico - INEGI ENOE',
        'archivo': 'salario_raw.csv',
        'registros': len(datos_totales),
        'descripcion': 'Salario mensual promedio trimestral por estado'
    }
    
    return datos_totales, metadata


def descargar_pea():
    """Descarga Población Económicamente Activa por estado."""
    logging.info("=== Iniciando descarga: Población Económicamente Activa ===")
    
    estados_ids = {
        1: 'Aguascalientes', 2: 'Baja California', 3: 'Baja California Sur',
        4: 'Campeche', 5: 'Coahuila de Zaragoza', 6: 'Colima',
        7: 'Chiapas', 8: 'Chihuahua', 9: 'Ciudad de México',
        10: 'Durango', 11: 'Guanajuato', 12: 'Guerrero',
        13: 'Hidalgo', 14: 'Jalisco', 15: 'México',
        16: 'Michoacán de Ocampo', 17: 'Morelos', 18: 'Nayarit',
        19: 'Nuevo León', 20: 'Oaxaca', 21: 'Puebla',
        22: 'Querétaro', 23: 'Quintana Roo', 24: 'San Luis Potosí',
        25: 'Sinaloa', 26: 'Sonora', 27: 'Tabasco',
        28: 'Tamaulipas', 29: 'Tlaxcala', 30: 'Veracruz de Ignacio de la Llave',
        31: 'Yucatán', 32: 'Zacatecas'
    }
    
    datos_totales = []
    for id_estado, nombre in estados_ids.items():
        url = (
            f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
            "&Economically+Active+Population=1&cube=inegi_enoe&drilldowns=State,Quarter"
            "&measures=Workforce&locale=es&parents=false"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    datos_totales.extend(data)
                    logging.info(f"  ✓ {nombre}")
        except Exception as e:
            logging.error(f"  ✗ Error en {nombre}: {e}")
    
    metadata = {
        'nombre': 'Población Económicamente Activa',
        'fuente': 'DataMexico - INEGI ENOE',
        'archivo': 'pea_raw.csv',
        'registros': len(datos_totales),
        'descripcion': 'PEA trimestral por entidad federativa'
    }
    
    return datos_totales, metadata


def descargar_gasto():
    """Descarga gasto público ejecutado."""
    logging.info("=== Iniciando descarga: Gasto Público Ejecutado ===")
    
    datos_totales = []
    for ano in range(2013, 2024):
        url = (
            f"http://www.economia.gob.mx/datamexico/api/data?cube=budget_transparency"
            f"&drilldowns=State,Functional+Group&measures=Amount+Executed&locale=es&Year={ano}"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    for item in data:
                        item['Year'] = ano
                    datos_totales.extend(data)
                    logging.info(f"  ✓ Año {ano}")
        except Exception as e:
            logging.error(f"  ✗ Error en año {ano}: {e}")
    
    metadata = {
        'nombre': 'Gasto Público Ejecutado',
        'fuente': 'DataMexico - Transparencia Presupuestaria',
        'archivo': 'gasto_raw.csv',
        'registros': len(datos_totales),
        'descripcion': 'Gasto público anual 2013-2023 por estado y grupo funcional'
    }
    
    return datos_totales, metadata


def descargar_remesas():
    """Descarga remesas por estado."""
    logging.info("=== Iniciando descarga: Remesas ===")
    
    estados_ids = {
        1: 'Aguascalientes', 2: 'Baja California', 3: 'Baja California Sur',
        4: 'Campeche', 5: 'Coahuila de Zaragoza', 6: 'Colima',
        7: 'Chiapas', 8: 'Chihuahua', 9: 'Ciudad de México',
        10: 'Durango', 11: 'Guanajuato', 12: 'Guerrero',
        13: 'Hidalgo', 14: 'Jalisco', 15: 'México',
        16: 'Michoacán de Ocampo', 17: 'Morelos', 18: 'Nayarit',
        19: 'Nuevo León', 20: 'Oaxaca', 21: 'Puebla',
        22: 'Querétaro', 23: 'Quintana Roo', 24: 'San Luis Potosí',
        25: 'Sinaloa', 26: 'Sonora', 27: 'Tabasco',
        28: 'Tamaulipas', 29: 'Tlaxcala', 30: 'Veracruz de Ignacio de la Llave',
        31: 'Yucatán', 32: 'Zacatecas'
    }
    
    datos_totales = []
    for id_estado, nombre in estados_ids.items():
        url = (
            f"http://www.economia.gob.mx/datamexico/api/data.jsonrecords?State={id_estado}"
            "&cube=banxico_mun_income_remittances&drilldowns=State,Quarter"
            "&measures=Remittance+Amount&locale=es"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    datos_totales.extend(data)
                    logging.info(f"  ✓ {nombre}")
        except Exception as e:
            logging.error(f"  ✗ Error en {nombre}: {e}")
    
    metadata = {
        'nombre': 'Remesas',
        'fuente': 'DataMexico - Banco de México',
        'archivo': 'remesas_raw.csv',
        'registros': len(datos_totales),
        'descripcion': 'Remesas trimestrales por entidad federativa'
    }
    
    return datos_totales, metadata


# ============================================================================
# MÓDULO 4: COEFICIENTE DE GINI
# ============================================================================

def descargar_gini():
    """Descarga coeficiente de GINI por entidad federativa."""
    logging.info("=== Iniciando descarga: Coeficiente de GINI ===")
    
    url = (
        "https://www.economia.gob.mx/apidatamexico/tesseract/data.jsonrecords"
        "?Year=2010%2C2012%2C2014%2C2016%2C2018%2C2020%2C2022"
        "&cube=coneval_gini_ent&drilldowns=Year%2CState&locale=es&measures=GINI"
    )
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        df = pd.DataFrame(data["data"])
        estado = 'Exitoso'
        registros = len(df)
        logging.info(f"  ✓ Descargado: {registros} registros")
    except Exception as e:
        logging.error(f"  ✗ Error: {e}")
        df = pd.DataFrame()
        estado = f'Error: {str(e)}'
        registros = 0
    
    metadata = {
        'nombre': 'Coeficiente de GINI',
        'fuente': 'DataMexico - CONEVAL',
        'archivo': 'coeficiente_gini_desigualdad.csv',
        'registros': registros,
        'descripcion': 'Coeficiente GINI 2010-2022 por entidad federativa'
    }
    
    return df, metadata


# ============================================================================
# GENERACIÓN DE LOGS
# ============================================================================

def generar_log_completo(metadatos_list):
    """Genera un log consolidado de todas las descargas."""
    
    contenido = f"""
{'=' * 80}
LOG CONSOLIDADO DE DESCARGA DE DATOS DEL PROYECTO
{'=' * 80}
Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este archivo documenta todas las fuentes de datos utilizadas en el proyecto.

"""
    
    # Agrupar por categoría
    categorias = {
        'Seguridad': [],
        'Educación y Salud': [],
        'Variables Económicas': [],
        'Desigualdad': []
    }
    
    for meta in metadatos_list:
        nombre = meta['nombre']
        if 'Inseguridad' in nombre or 'Delictiva' in nombre:
            categorias['Seguridad'].append(meta)
        elif 'Educación' in nombre or 'Salud' in nombre:
            categorias['Educación y Salud'].append(meta)
        elif 'GINI' in nombre:
            categorias['Desigualdad'].append(meta)
        else:
            categorias['Variables Económicas'].append(meta)
    
    contador = 1
    for categoria, items in categorias.items():
        if items:
            contenido += f"\n{'=' * 80}\n"
            contenido += f"CATEGORÍA: {categoria.upper()}\n"
            contenido += f"{'=' * 80}\n\n"
            
            for meta in items:
                contenido += f"--- FUENTE {contador}: {meta['nombre']} ---\n"
                contenido += f"Fuente Original: {meta['fuente']}\n"
                contenido += f"Descripción: {meta['descripcion']}\n"
                contenido += f"Archivo Generado: data/raw/{meta['archivo']}\n"
                contenido += f"Registros Descargados: {meta['registros']:,}\n"
                contenido += f"\n"
                contador += 1
    
    contenido += f"\n{'=' * 80}\n"
    contenido += f"RESUMEN DE DESCARGA\n"
    contenido += f"{'=' * 80}\n"
    contenido += f"Total de fuentes: {len(metadatos_list)}\n"
    contenido += f"Total de registros: {sum(m['registros'] for m in metadatos_list):,}\n"
    contenido += f"\nArchivos generados en: {DATA_RAW_DIR}\n"
    
    ruta_log = DATA_RAW_DIR / "log_descarga_completo.txt"
    try:
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write(contenido)
        logging.info(f"✓ Log completo guardado en: {ruta_log}")
    except Exception as e:
        logging.error(f"✗ Error al generar log: {e}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que orquesta todas las descargas."""
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description='Descarga completa de todos los datos del proyecto'
    )
    parser.add_argument(
        '--token',
        type=str,
        help='Token de API de INEGI (si no se proporciona, se busca en .env)'
    )
    args = parser.parse_args()
    
    # Obtener token
    token = args.token or os.getenv("INEGI_API_TOKEN") or os.getenv("token_inegi")
    if not token:
        logging.error("ERROR: Token de INEGI no configurado.")
        print("\nPor favor, proporciona el token usando:")
        print("  1. Argumento --token: python descarga_datos_completa.py --token TU_TOKEN")
        print("  2. Variable de entorno INEGI_API_TOKEN o token_inegi en archivo .env")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("DESCARGA COMPLETA DE DATOS DEL PROYECTO")
    print("=" * 80)
    print(f"Directorio de salida: {DATA_RAW_DIR}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    metadatos_list = []
    
    # ========================================================================
    # MÓDULO 1: DATOS DE SEGURIDAD
    # ========================================================================
    print("\n" + "█" * 80)
    print("MÓDULO 1: DATOS DE SEGURIDAD")
    print("█" * 80 + "\n")
    
    try:
        df, meta = descargar_percepcion_inseguridad(token)
        if not df.empty:
            df.to_csv(DATA_RAW_DIR / meta['archivo'], index=False)
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en percepción de inseguridad: {e}")
    
    try:
        df, meta = descargar_incidencia_delictiva()
        if not df.empty:
            df.to_csv(DATA_RAW_DIR / meta['archivo'], index=False)
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en incidencia delictiva: {e}")
    
    # ========================================================================
    # MÓDULO 2: EDUCACIÓN Y SALUD
    # ========================================================================
    print("\n" + "█" * 80)
    print("MÓDULO 2: DATOS DE EDUCACIÓN Y SALUD")
    print("█" * 80 + "\n")
    
    try:
        df, meta = descargar_educacion_salud(token)
        if not df.empty:
            df.to_csv(DATA_RAW_DIR / meta['archivo'], index=False)
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en educación y salud: {e}")
    
    # ========================================================================
    # MÓDULO 3: VARIABLES ECONÓMICAS
    # ========================================================================
    print("\n" + "█" * 80)
    print("MÓDULO 3: VARIABLES ECONÓMICAS")
    print("█" * 80 + "\n")
    
    # IED
    try:
        datos, meta = descargar_ied()
        if datos:
            guardar_json_a_csv(datos, DATA_RAW_DIR / meta['archivo'])
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en IED: {e}")
    
    # Salario
    try:
        datos, meta = descargar_salario()
        if datos:
            guardar_json_a_csv(datos, DATA_RAW_DIR / meta['archivo'])
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en salario: {e}")
    
    # PEA
    try:
        datos, meta = descargar_pea()
        if datos:
            guardar_json_a_csv(datos, DATA_RAW_DIR / meta['archivo'])
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en PEA: {e}")
    
    # Gasto
    try:
        datos, meta = descargar_gasto()
        if datos:
            guardar_json_a_csv(datos, DATA_RAW_DIR / meta['archivo'])
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en gasto: {e}")
    
    # Remesas
    try:
        datos, meta = descargar_remesas()
        if datos:
            guardar_json_a_csv(datos, DATA_RAW_DIR / meta['archivo'])
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en remesas: {e}")
    
    # ========================================================================
    # MÓDULO 4: COEFICIENTE DE GINI
    # ========================================================================
    print("\n" + "█" * 80)
    print("MÓDULO 4: INDICADORES DE DESIGUALDAD")
    print("█" * 80 + "\n")
    
    try:
        df, meta = descargar_gini()
        if not df.empty:
            df.to_csv(DATA_RAW_DIR / meta['archivo'], index=False)
            logging.info(f"✓ Guardado: {meta['archivo']}")
            metadatos_list.append(meta)
    except Exception as e:
        logging.error(f"✗ Error en GINI: {e}")
    
    # ========================================================================
    # GENERAR LOG CONSOLIDADO
    # ========================================================================
    print("\n" + "█" * 80)
    print("GENERANDO LOG CONSOLIDADO")
    print("█" * 80 + "\n")
    
    generar_log_completo(metadatos_list)
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("\n" + "=" * 80)
    print("¡DESCARGA COMPLETADA!")
    print("=" * 80)
    print(f"\nArchivos generados: {len(metadatos_list)}")
    print(f"Registros totales: {sum(m['registros'] for m in metadatos_list):,}")
    print(f"\nUbicación: {DATA_RAW_DIR}")
    print("\nArchivos CSV generados:")
    for meta in metadatos_list:
        print(f"  - {meta['archivo']} ({meta['registros']:,} registros)")
    print(f"\nLog consolidado: log_descarga_completo.txt")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
