"""
Script unificado para descarga de datos de fuentes públicas

Este script descarga datos de diferentes fuentes públicas de variables socioeconómicas
para todos los estados de la república mexicana.

Fuentes de datos:
1. Economía - DataMexico API (IED, Salario, PEA, Gasto Público, Remesas)
2. INEGI - API de indicadores (Educación y Salud)
3. CONEVAL - Rezago educativo
4. Seguridad - Datos de seguridad de México

Autor: Equipo Seguridad y Desarrollo
Fecha: 2025
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# API Key de INEGI desde variable de entorno
INEGI_API_KEY = os.getenv("INEGI_API_KEY", "32805429-135c-9311-70c1-0b963c6f8317")

# Diccionario de estados
ESTADOS_IDS = {
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


def download_ied_data():
    """Descarga datos de Inversión Extranjera Directa (IED) por estado"""
    print("\n" + "="*80)
    print("DESCARGANDO: Inversión Extranjera Directa (IED)")
    print("="*80)
    
    lista_df = []
    
    for id_estado, nombre_estado in ESTADOS_IDS.items():
        url = (f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
               "&cube=fdi_2_state_investment&drilldowns=Quarter,State&locale=es"
               "&measures=Investment&parents=false")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    lista_df.append(pd.DataFrame(data))
                    print(f"  ✓ {nombre_estado}: {len(data)} registros")
            else:
                print(f"  ✗ Error en {nombre_estado}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en {nombre_estado}: {str(e)}")
    
    if lista_df:
        df_ied = pd.concat(lista_df, ignore_index=True)
        filepath = RAW_DATA_DIR / "ied_raw.csv"
        df_ied.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_ied)}")
        return True
    return False


def download_salario_data():
    """Descarga datos de Salario Mensual por estado"""
    print("\n" + "="*80)
    print("DESCARGANDO: Salario Mensual")
    print("="*80)
    
    lista_df = []
    
    for id_estado, nombre_estado in ESTADOS_IDS.items():
        url = (f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
               "&Population+Classification=1&cube=inegi_enoe&drilldowns=State,Quarter"
               "&measures=Monthly+Wage,Workforce&locale=es&parents=false")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    lista_df.append(pd.DataFrame(data))
                    print(f"  ✓ {nombre_estado}: {len(data)} registros")
            else:
                print(f"  ✗ Error en {nombre_estado}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en {nombre_estado}: {str(e)}")
    
    if lista_df:
        df_salario = pd.concat(lista_df, ignore_index=True)
        filepath = RAW_DATA_DIR / "salario_raw.csv"
        df_salario.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_salario)}")
        return True
    return False


def download_pea_data():
    """Descarga datos de Población Económicamente Activa (PEA) por estado"""
    print("\n" + "="*80)
    print("DESCARGANDO: Población Económicamente Activa (PEA)")
    print("="*80)
    
    lista_df = []
    
    for id_estado, nombre_estado in ESTADOS_IDS.items():
        url = (f"http://www.economia.gob.mx/datamexico/api/data?State={id_estado}"
               "&Economically+Active+Population=1&cube=inegi_enoe&drilldowns=State,Quarter"
               "&measures=Workforce&locale=es&parents=false")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    lista_df.append(pd.DataFrame(data))
                    print(f"  ✓ {nombre_estado}: {len(data)} registros")
            else:
                print(f"  ✗ Error en {nombre_estado}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en {nombre_estado}: {str(e)}")
    
    if lista_df:
        df_pea = pd.concat(lista_df, ignore_index=True)
        filepath = RAW_DATA_DIR / "pea_raw.csv"
        df_pea.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_pea)}")
        return True
    return False


def download_gasto_data():
    """Descarga datos de Gasto Público Ejecutado por estado"""
    print("\n" + "="*80)
    print("DESCARGANDO: Gasto Público Ejecutado")
    print("="*80)
    
    lista_df = []
    anos = range(2013, 2024)
    
    for ano in anos:
        url = (f"http://www.economia.gob.mx/datamexico/api/data?cube=budget_transparency"
               f"&drilldowns=State,Functional+Group&measures=Amount+Executed&locale=es&Year={ano}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    df_temp = pd.DataFrame(data)
                    df_temp['Year'] = ano
                    lista_df.append(df_temp)
                    print(f"  ✓ Año {ano}: {len(data)} registros")
            else:
                print(f"  ✗ Error en año {ano}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en año {ano}: {str(e)}")
    
    if lista_df:
        df_gasto = pd.concat(lista_df, ignore_index=True)
        filepath = RAW_DATA_DIR / "gasto_raw.csv"
        df_gasto.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_gasto)}")
        return True
    return False


def download_remesas_data():
    """Descarga datos de Remesas por estado"""
    print("\n" + "="*80)
    print("DESCARGANDO: Remesas")
    print("="*80)
    
    lista_df = []
    
    for id_estado, nombre_estado in ESTADOS_IDS.items():
        url = (f"http://www.economia.gob.mx/datamexico/api/data.jsonrecords?State={id_estado}"
               "&cube=banxico_mun_income_remittances&drilldowns=State,Quarter"
               "&measures=Remittance+Amount&locale=es")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    lista_df.append(pd.DataFrame(data))
                    print(f"  ✓ {nombre_estado}: {len(data)} registros")
            else:
                print(f"  ✗ Error en {nombre_estado}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en {nombre_estado}: {str(e)}")
    
    if lista_df:
        df_remesas = pd.concat(lista_df, ignore_index=True)
        # Seleccionar columnas relevantes si existen
        if 'State' in df_remesas.columns and 'Quarter' in df_remesas.columns:
            cols = ['State', 'Quarter', 'Remittance Amount']
            df_remesas = df_remesas[[col for col in cols if col in df_remesas.columns]]
        
        filepath = RAW_DATA_DIR / "remesas_raw.csv"
        df_remesas.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_remesas)}")
        return True
    return False


def download_inegi_educacion_salud():
    """Descarga indicadores de educación y salud del INEGI"""
    print("\n" + "="*80)
    print("DESCARGANDO: Indicadores INEGI - Educación y Salud")
    print("="*80)
    
    # Indicadores de educación y salud
    indicadores = {
        '6207019048': 'Tasa de analfabetismo',
        '6207020032': 'Grado promedio de escolaridad',
        '6207020033': 'Porcentaje de población con educación básica',
        '6207020034': 'Porcentaje de población con educación media superior',
        '6207020035': 'Porcentaje de población con educación superior',
        '6207003986': 'Esperanza de vida al nacimiento',
        '6207004772': 'Tasa de mortalidad infantil',
    }
    
    resultados = []
    
    for codigo, nombre in indicadores.items():
        url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{codigo}/es/0700/false/BIE/2.0/{INEGI_API_KEY}?type=json"
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'Series' in data:
                    for serie in data['Series']:
                        if 'OBSERVATIONS' in serie:
                            for obs in serie['OBSERVATIONS']:
                                resultados.append({
                                    'indicador_codigo': codigo,
                                    'indicador_nombre': nombre,
                                    'periodo': obs.get('TIME_PERIOD', ''),
                                    'valor': obs.get('OBS_VALUE', ''),
                                    'estado': serie.get('REGION', '')
                                })
                    print(f"  ✓ {nombre}: {len(serie.get('OBSERVATIONS', []))} registros")
            else:
                print(f"  ✗ Error en {nombre}: código {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error en {nombre}: {str(e)}")
    
    if resultados:
        df_inegi = pd.DataFrame(resultados)
        filepath = RAW_DATA_DIR / "inegi_educacion_salud_raw.csv"
        df_inegi.to_csv(filepath, index=False)
        print(f"\n✓ Datos guardados: {filepath}")
        print(f"  Total de registros: {len(df_inegi)}")
        return True
    return False


def generate_metadata():
    """Genera archivo de metadatos con información sobre las fuentes y fechas de descarga"""
    print("\n" + "="*80)
    print("GENERANDO METADATOS")
    print("="*80)
    
    metadata = f"""METADATOS DE DESCARGA DE DATOS
{"="*80}

Fecha de descarga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Proyecto: Seguridad y Desarrollo - Análisis Socioeconómico por Estado

{"="*80}
FUENTES DE DATOS
{"="*80}

1. DATOS ECONÓMICOS - DataMexico API
   URL: http://www.economia.gob.mx/datamexico/
   Descripción: Portal de datos abiertos del gobierno mexicano con información
                económica, demográfica y social.
   
   Datasets descargados:
   - Inversión Extranjera Directa (IED)
     * Archivo: ied_raw.csv
     * Descripción: Montos de inversión extranjera directa por estado y trimestre
     * Periodo: 1999-Q1 hasta la fecha
     * Unidad: Millones de dólares USD
   
   - Salario Mensual
     * Archivo: salario_raw.csv
     * Descripción: Salario mensual promedio por estado y trimestre
     * Fuente original: INEGI - ENOE
     * Unidad: Pesos mexicanos
   
   - Población Económicamente Activa (PEA)
     * Archivo: pea_raw.csv
     * Descripción: Número de personas en la población económicamente activa
     * Fuente original: INEGI - ENOE
     * Unidad: Número de personas
   
   - Gasto Público Ejecutado
     * Archivo: gasto_raw.csv
     * Descripción: Monto del gasto público ejecutado por estado y grupo funcional
     * Periodo: 2013-2023
     * Unidad: Pesos mexicanos
   
   - Remesas
     * Archivo: remesas_raw.csv
     * Descripción: Monto de remesas recibidas por estado y trimestre
     * Fuente original: Banco de México (BANXICO)
     * Unidad: Millones de dólares USD

2. INDICADORES INEGI - Educación y Salud
   URL: https://www.inegi.org.mx/app/api/
   API Key: {INEGI_API_KEY[:10]}...
   Descripción: Instituto Nacional de Estadística y Geografía - Indicadores
                socioeconómicos oficiales de México
   
   Datasets descargados:
   - Indicadores de Educación y Salud
     * Archivo: inegi_educacion_salud_raw.csv
     * Indicadores incluidos:
       - Tasa de analfabetismo
       - Grado promedio de escolaridad
       - Porcentaje de población con educación básica
       - Porcentaje de población con educación media superior
       - Porcentaje de población con educación superior
       - Esperanza de vida al nacimiento
       - Tasa de mortalidad infantil

{"="*80}
INFORMACIÓN ADICIONAL
{"="*80}

Todos los datos están organizados por entidad federativa (estado) de México.
Los datos temporales están organizados por trimestre o año según corresponda.
Los archivos están en formato CSV con codificación UTF-8.

Para procesar estos datos, ejecutar:
    python notebooks/process_data.py

Para más información, consultar los diccionarios de datos en:
    references/

{"="*80}
"""
    
    metadata_path = RAW_DATA_DIR / "metadata.txt"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(metadata)
    
    print(f"✓ Metadatos guardados: {metadata_path}")


def main():
    """Función principal que ejecuta todas las descargas"""
    print("\n" + "="*80)
    print("INICIANDO DESCARGA DE DATOS")
    print("="*80)
    print(f"Directorio de datos: {RAW_DATA_DIR}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    resultados = {
        'IED': False,
        'Salario': False,
        'PEA': False,
        'Gasto Público': False,
        'Remesas': False,
        'INEGI Educación/Salud': False
    }
    
    # Ejecutar descargas
    try:
        resultados['IED'] = download_ied_data()
    except Exception as e:
        print(f"\n✗ Error en IED: {str(e)}")
    
    try:
        resultados['Salario'] = download_salario_data()
    except Exception as e:
        print(f"\n✗ Error en Salario: {str(e)}")
    
    try:
        resultados['PEA'] = download_pea_data()
    except Exception as e:
        print(f"\n✗ Error en PEA: {str(e)}")
    
    try:
        resultados['Gasto Público'] = download_gasto_data()
    except Exception as e:
        print(f"\n✗ Error en Gasto Público: {str(e)}")
    
    try:
        resultados['Remesas'] = download_remesas_data()
    except Exception as e:
        print(f"\n✗ Error en Remesas: {str(e)}")
    
    try:
        resultados['INEGI Educación/Salud'] = download_inegi_educacion_salud()
    except Exception as e:
        print(f"\n✗ Error en INEGI: {str(e)}")
    
    # Generar metadatos
    try:
        generate_metadata()
    except Exception as e:
        print(f"\n✗ Error generando metadatos: {str(e)}")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE DESCARGA")
    print("="*80)
    for nombre, exito in resultados.items():
        status = "✓" if exito else "✗"
        print(f"{status} {nombre}")
    
    exitosos = sum(1 for v in resultados.values() if v)
    print(f"\nTotal: {exitosos}/{len(resultados)} fuentes descargadas exitosamente")
    
    if exitosos == 0:
        print("\n⚠ ADVERTENCIA: No se pudo descargar ninguna fuente de datos")
        sys.exit(1)
    elif exitosos < len(resultados):
        print("\n⚠ ADVERTENCIA: Algunas fuentes no se descargaron correctamente")
        sys.exit(0)
    else:
        print("\n✓ Todas las fuentes descargadas exitosamente")
        sys.exit(0)


if __name__ == "__main__":
    main()
