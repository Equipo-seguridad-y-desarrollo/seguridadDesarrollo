"""
Script para recopilar datos de seguridad en México

Este script descarga dos conjuntos de datos principales:
1. Indicador de percepción de inseguridad (INEGI/ENVIPE) 2011-2025
2. Incidencia delictiva estatal (SESNSP) 2015-2025

Requisitos:
- Token de API de INEGI (pasar como argumento o configurar en .env)
- Librerías: requests, pandas, python-dotenv

Uso:
    python datos_seguridad_mexico.py --token TU_TOKEN_AQUI
    
    o con .env:
    python datos_seguridad_mexico.py
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import requests

# Cargar variables de entorno
load_dotenv()

# Configurar rutas del proyecto
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Crear directorio data/raw si no existe
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)


def generar_log_descarga(log_entries, output_file):
    """
    Genera un archivo de log con información de la descarga
    
    Args:
        log_entries: Lista de diccionarios con información de descarga
        output_file: Ruta del archivo de salida
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LOG DE DESCARGA DE DATOS DE SEGURIDAD - MÉXICO\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for i, entry in enumerate(log_entries, 1):
            f.write(f"\n{'=' * 80}\n")
            f.write(f"FUENTE {i}: {entry['nombre']}\n")
            f.write(f"{'=' * 80}\n\n")
            
            f.write(f"Descripción:\n{entry['descripcion']}\n\n")
            f.write(f"Fuente: {entry['fuente']}\n")
            f.write(f"URL/API: {entry['url']}\n\n")
            
            if 'enlace_documentacion' in entry:
                f.write(f"Documentación:\n{entry['enlace_documentacion']}\n\n")
            
            f.write(f"Periodicidad: {entry['periodicidad']}\n")
            f.write(f"Cobertura temporal: {entry['cobertura_temporal']}\n")
            f.write(f"Cobertura geográfica: {entry['cobertura_geografica']}\n")
            f.write(f"Unidad de medida: {entry['unidad_medida']}\n\n")
            
            f.write(f"Archivo guardado: {entry['archivo_salida']}\n")
            f.write(f"Registros descargados: {entry['registros']}\n")
            f.write(f"Estado: {entry['estado']}\n")
            
            if 'observaciones' in entry:
                f.write(f"\nObservaciones:\n{entry['observaciones']}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("FIN DEL LOG\n")
        f.write("=" * 80 + "\n")


def descargar_percepcion_inseguridad(token):
    """
    Descarga datos de percepción de inseguridad de INEGI
    
    Args:
        token: Token de API de INEGI
        
    Returns:
        tuple: (DataFrame con datos, diccionario con metadata para log)
    """
    clave_indicador = "6204327085"

    entidades = {
        "00": "Nacional", "01": "Aguascalientes", "02": "Baja California", 
        "03": "Baja California Sur", "04": "Campeche", "05": "Coahuila", 
        "06": "Colima", "07": "Chiapas", "08": "Chihuahua", "09": "Ciudad de México", 
        "10": "Durango", "11": "Guanajuato", "12": "Guerrero", "13": "Hidalgo", 
        "14": "Jalisco", "15": "México", "16": "Michoacán", "17": "Morelos", 
        "18": "Nayarit", "19": "Nuevo León", "20": "Oaxaca", "21": "Puebla", 
        "22": "Querétaro", "23": "Quintana Roo", "24": "San Luis Potosí", 
        "25": "Sinaloa", "26": "Sonora", "27": "Tabasco", "28": "Tamaulipas", 
        "29": "Tlaxcala", "30": "Veracruz", "31": "Yucatán", "32": "Zacatecas",
    }
    claves_entidades = list(entidades.keys())
    all_data = []

    print("Descargando datos de percepción de inseguridad...")
    for clave in claves_entidades:
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
                df["entidad"] = entidades[clave]
                df["clave"] = clave
                df = df[["año", "valor", "entidad", "clave"]]
                all_data.append(df)
                print(f"  + Exito en {entidades[clave]}") # MODIFICADO
            else:
                print(f"  - Sin datos para {entidades[clave]}") # MODIFICADO
        except Exception as e:
            print(f"  X Error en la entidad {clave}: {e}") # MODIFICADO

    df_final = pd.concat(all_data, ignore_index=True)
    
    metadata = {
        'nombre': 'Indicador de Percepción de Inseguridad',
        'descripcion': '''Número estimado de personas de 18 años y más que perciben su entidad 
federativa como insegura, expresado como tasa por cada 100,000 habitantes del 
mismo grupo de edad. Los datos provienen de la Encuesta Nacional de Victimización 
y Percepción sobre Seguridad Pública (ENVIPE) realizada por INEGI.''',
        'fuente': 'INEGI - Banco de Indicadores (ENVIPE/CNI)',
        'url': 'https://www.inegi.org.mx/app/api/indicadores/',
        'enlace_documentacion': '''https://www.inegi.org.mx/programas/envipe/
https://www.inegi.org.mx/app/indicadores/?tm=0''',
        'periodicidad': 'Anual',
        'cobertura_temporal': '2011-2025',
        'cobertura_geografica': 'Nacional y 32 entidades federativas',
        'unidad_medida': 'Personas de 18+ años por cada 100,000 habitantes del mismo grupo',
        'archivo_salida': 'indicador_inseguridad_estados.csv',
        'registros': len(df_final),
        'estado': 'Exitoso',
        'observaciones': f'''- Clave del indicador: {clave_indicador}
- Total de entidades: 33 (32 estados + nacional)
- Este indicador mide PERCEPCIÓN, no incidencia real
- Basado en encuestas probabilísticas representativas'''
    }
    
    return df_final, metadata


def descargar_incidencia_delictiva():
    """
    Descarga datos de incidencia delictiva del SESNSP
    
    Returns:
        tuple: (DataFrame con datos, diccionario con metadata para log)
    """
    print("\nDescargando datos de incidencia delictiva...")
    url_crimen = "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv"
    
    try:
        df_crimen = pd.read_csv(url_crimen)
        estado = 'Exitoso'
        registros = len(df_crimen)
        print(f"+ Descargado: {registros} registros") # MODIFICADO
    except Exception as e:
        print(f"X Error descargando incidencia delictiva: {e}") # MODIFICADO
        df_crimen = pd.DataFrame()
        estado = f'Error: {str(e)}'
        registros = 0
    
    metadata = {
        'nombre': 'Incidencia Delictiva Estatal',
        'descripcion': '''Registro oficial de hechos delictivos ocurridos en México, desagregados 
por entidad federativa, tipo de delito y mes. Los datos son reportados por las 
procuradurías y fiscalías estatales al Secretariado Ejecutivo del Sistema Nacional 
de Seguridad Pública (SESNSP) y representan los delitos del fuero común y federal 
registrados oficialmente.''',
        'fuente': 'SESNSP - Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública',
        'url': url_crimen,
        'enlace_documentacion': '''https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva
https://www.gob.mx/sesnsp/''',
        'periodicidad': 'Mensual (publicación alrededor del día 20 de cada mes)',
        'cobertura_temporal': 'Enero 2015 - Agosto 2025',
        'cobertura_geografica': 'Nacional y 32 entidades federativas',
        'unidad_medida': 'Hechos delictivos (conteos absolutos mensuales)',
        'archivo_salida': 'incidencia_delictiva_estatal_2015_2025.csv',
        'registros': registros,
        'estado': estado,
        'observaciones': '''- Incluye delitos del fuero común y federal
- Solo incluye delitos denunciados y registrados oficialmente (cifra obscura no incluida)
- Los datos más recientes pueden ser preliminares
- Clasificación de delitos según criterios SESNSP'''
    }
    
    return df_crimen, metadata


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description='Descarga datos de seguridad en México desde INEGI y SESNSP'
    )
    parser.add_argument(
        '--token',
        type=str,
        help='Token de API de INEGI (si no se proporciona, se busca en .env)'
    )
    args = parser.parse_args()
    
    token = args.token or os.getenv("INEGI_API_TOKEN")
    if not token:
        print("ERROR: INEGI_API_TOKEN no está configurado.")
        print("Por favor, proporciona el token usando:")
        print("  1. Argumento --token: python datos_seguridad_mexico.py --token TU_TOKEN")
        print("  2. Variable de entorno INEGI_API_TOKEN en archivo .env")
        sys.exit(1)
    
    print("=" * 80)
    print("DESCARGA DE DATOS DE SEGURIDAD - MÉXICO")
    print("=" * 80)
    print(f"\nDirectorio de salida: {DATA_RAW_DIR}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    log_entries = []
    
    try:
        df_percepcion, metadata_percepcion = descargar_percepcion_inseguridad(token)
        output_file = DATA_RAW_DIR / metadata_percepcion['archivo_salida']
        df_percepcion.to_csv(output_file, index=False)
        print(f"\n+ Guardado: {output_file} ({len(df_percepcion)} registros)") # MODIFICADO
        log_entries.append(metadata_percepcion)
    except Exception as e:
        print(f"\n- Error en descarga de percepción de inseguridad: {e}") # MODIFICADO
        log_entries.append({
            'nombre': 'Indicador de Percepción de Inseguridad',
            'estado': f'Error: {str(e)}',
            'registros': 0
        })
    
    try:
        df_delictiva, metadata_delictiva = descargar_incidencia_delictiva()
        if not df_delictiva.empty:
            output_file = DATA_RAW_DIR / metadata_delictiva['archivo_salida']
            df_delictiva.to_csv(output_file, index=False)
            print(f"+ Guardado: {output_file} ({len(df_delictiva)} registros)") # MODIFICADO
        log_entries.append(metadata_delictiva)
    except Exception as e:
        print(f"- Error en descarga de incidencia delictiva: {e}") # MODIFICADO
        log_entries.append({
            'nombre': 'Incidencia Delictiva Estatal',
            'estado': f'Error: {str(e)}',
            'registros': 0
        })
    
    log_file = DATA_RAW_DIR / "log_descarga_seguridad.txt"
    generar_log_descarga(log_entries, log_file)
    print(f"\n+ Log de descarga guardado: {log_file}") # MODIFICADO
    
    print("\n" + "=" * 80)
    print("¡PROCESO COMPLETADO!")
    print("=" * 80)
    print(f"\nArchivos generados en: {DATA_RAW_DIR}")
    print("- indicador_inseguridad_estados.csv")
    print("- incidencia_delictiva_estatal_2015_2025.csv")
    print("- log_descarga_seguridad.txt")


if __name__ == "__main__":
    main()