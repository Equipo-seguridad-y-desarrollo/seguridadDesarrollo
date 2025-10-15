"""
Script para recopilar datos de seguridad en México

Este script descarga dos conjuntos de datos principales:
1. Indicador de percepción de inseguridad (INEGI/ENVIPE) 2011-2025
2. Incidencia delictiva estatal (SESNSP) 2015-2025

Requisitos:
- Token de API de INEGI (configurar en archivo .env como INEGI_API_TOKEN)
- Librerías: requests, pandas, python-dotenv

Uso:
1. Copiar .env.example a .env
2. Configurar INEGI_API_TOKEN en .env
3. Ejecutar: python notebooks/datos_seguridad_mexico.py
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import requests

# Cargar variables de entorno
load_dotenv()

# Definir rutas
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Crear directorio si no existe
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ====== (1) Indicador percepción de inseguridad: TODOS LOS ESTADOS y NACIONAL 2011 a 2025 ======
# Periodicidad: anual (proviene de ENVIPE, serie anual).
# Qué se mide: número de personas de 18 años y más que perciben su entidad federativa como insegura,
# estimadas por cada 100 000 habitantes de ese grupo de edad (unidad del indicador).
# Ventana temporal: serie disponible desde 2011 (primera ENVIPE) hasta 2025 (edición vigente).
# Cobertura geográfica: Nacional y por entidad federativa (desagregación estatal).

# Obtener token desde variable de entorno
token = os.getenv("INEGI_API_TOKEN")
if not token:
    raise ValueError(
        "INEGI_API_TOKEN no está configurado. Por favor, configura tu token en el archivo .env"
    )

clave_indicador = "6204327085"  # CNI: percepción de inseguridad por cada 100 000 (18+).

entidades = {
    "00": "Nacional",
    "01": "Aguascalientes",
    "02": "Baja California",
    "03": "Baja California Sur",
    "04": "Campeche",
    "05": "Coahuila",
    "06": "Colima",
    "07": "Chiapas",
    "08": "Chihuahua",
    "09": "Ciudad de México",
    "10": "Durango",
    "11": "Guanajuato",
    "12": "Guerrero",
    "13": "Hidalgo",
    "14": "Jalisco",
    "15": "México",
    "16": "Michoacán",
    "17": "Morelos",
    "18": "Nayarit",
    "19": "Nuevo León",
    "20": "Oaxaca",
    "21": "Puebla",
    "22": "Querétaro",
    "23": "Quintana Roo",
    "24": "San Luis Potosí",
    "25": "Sinaloa",
    "26": "Sonora",
    "27": "Tabasco",
    "28": "Tamaulipas",
    "29": "Tlaxcala",
    "30": "Veracruz",
    "31": "Yucatán",
    "32": "Zacatecas",
}
claves_entidades = list(entidades.keys())
all_data = []

print("Descargando datos de percepción de inseguridad...")
for clave in claves_entidades:
    url = (
        f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/"
        f"{clave_indicador}/es/{clave}/false/BISE/2.0/{token}?type=json"
    )  # API del Banco de Indicadores.
    try:
        response = requests.get(url, timeout=7)
        json_data = response.json()
        if "Series" in json_data and json_data["Series"]:
            serie = json_data["Series"][0]["OBSERVATIONS"]
            df = pd.DataFrame(serie)
            df["año"] = df["TIME_PERIOD"].astype(int)  # Años en la serie (2011–2025).
            df["valor"] = pd.to_numeric(
                df["OBS_VALUE"], errors="coerce"
            )  # Personas 18+ por cada 100 000 que perciben inseguridad.
            df["entidad"] = entidades[clave]  # Desagregación estatal y nacional.
            df["clave"] = clave
            df = df[["año", "valor", "entidad", "clave"]]
            all_data.append(df)
            print(f"  ✓ {entidades[clave]}")
        else:
            print(f"  ✗ Sin datos para {entidades[clave]}")
    except Exception as e:
        print(f"  ✗ Error en la entidad {clave}: {e}")

df_final = pd.concat(all_data, ignore_index=True)
# Guardar en ./data/raw/
output_file1 = RAW_DATA_DIR / "indicador_inseguridad_estados.csv"
df_final.to_csv(output_file1, index=False)
print(f"\n✓ Guardado: {output_file1} ({len(df_final)} registros)")

# ====== (2) Incidencia Delictiva Estatal 2015-2025 (CSV directo) ======
# Periodicidad: mensual; suele publicarse alrededor del día 20 de cada mes con cifras del mes inmediato anterior.
# Qué se mide: hechos delictivos ocurridos, con desagregación por entidad federativa (serie estatal).
# Ventana temporal del recurso: enero 2015 a agosto 2025 (corte vigente del dataset estatal).
# Fuente: Datos abiertos del SESNSP (portal institucional de incidencia delictiva).

print("\nDescargando datos de incidencia delictiva...")
url_crimen = "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv"  # Corte a agosto 2025.
try:
    df_crimen = pd.read_csv(url_crimen)
    # Guardar en ./data/raw/
    output_file2 = RAW_DATA_DIR / "incidencia_delictiva_estatal_2015_2025.csv"
    df_crimen.to_csv(output_file2, index=False)
    print(f"✓ Guardado: {output_file2} ({len(df_crimen)} registros)")
except Exception as e:
    print(f"✗ Error descargando incidencia delictiva: {e}")

# ====== Generar archivo de metadatos ======
print("\nGenerando archivo de metadatos...")
fecha_descarga = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

metadata_content = f"""
REGISTRO DE DESCARGA DE DATOS - SEGURIDAD EN MÉXICO
====================================================

Fecha de descarga: {fecha_descarga}

Este archivo documenta las fuentes de datos de seguridad utilizadas en el proyecto,
la fecha de descarga y una descripción detallada de su naturaleza.

---
FUENTE 1: Indicador de Percepción de Inseguridad por Entidad Federativa
-------------------------------------------------------------------------

Archivo generado: indicador_inseguridad_estados.csv

Descripción:
  Mide el número de personas de 18 años y más que perciben su entidad federativa 
  como insegura, estimadas por cada 100,000 habitantes de ese grupo de edad.

Fuente original: 
  Instituto Nacional de Estadística y Geografía (INEGI)
  Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública (ENVIPE)
  Catálogo Nacional de Indicadores (CNI)

Enlace de referencia:
  https://www.inegi.org.mx/programas/envipe/
  https://www.inegi.org.mx/app/api/indicadores/

Clave del indicador: 6204327085

Periodicidad: Anual

Cobertura temporal: 2011 - 2025

Cobertura geográfica: Nacional y por entidad federativa (32 estados + nacional)

Unidad de medida: Personas de 18+ años por cada 100,000 habitantes

Columnas del dataset:
  - año: Año de la medición (2011-2025)
  - valor: Número de personas por cada 100,000 que perciben inseguridad
  - entidad: Nombre de la entidad federativa o "Nacional"
  - clave: Clave numérica de la entidad (00 para Nacional, 01-32 para estados)

---
FUENTE 2: Incidencia Delictiva Estatal
---------------------------------------

Archivo generado: incidencia_delictiva_estatal_2015_2025.csv

Descripción:
  Hechos delictivos registrados en averiguaciones previas y carpetas de investigación
  iniciadas por las procuradurías y fiscalías estatales. Contiene el número de delitos
  ocurridos, desagregados por tipo de delito, entidad federativa y mes.

Fuente original:
  Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)
  Datos Abiertos de Incidencia Delictiva

Enlace de descarga:
  https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv

Enlace de referencia:
  https://www.gob.mx/sesnsp/acciones-y-programas/incidencia-delictiva-del-fuero-comun-nueva-metodologia

Periodicidad: Mensual (publicación aproximadamente el día 20 de cada mes)

Cobertura temporal: Enero 2015 - Agosto 2025 (corte vigente)

Cobertura geográfica: Estatal (32 entidades federativas)

Unidad de medida: Número de hechos delictivos (conteos mensuales)

Columnas del dataset (principales):
  - Año: Año del registro
  - Clave_Ent: Clave de la entidad federativa
  - Entidad: Nombre de la entidad federativa
  - Bien jurídico afectado: Categoría del delito
  - Tipo de delito: Subtipo específico del delito
  - Subtipo de delito: Especificación detallada del delito
  - Modalidad: Modalidad en que ocurrió el delito
  - Enero - Diciembre: Número de delitos por mes

---
NOTAS ADICIONALES:
- Los datos se descargan en formato crudo (raw) sin transformaciones
- Para análisis, consultar los datos procesados en ./data/processed/
- Los diccionarios de datos detallados están en ./references/
- Fecha de última actualización de este archivo: {fecha_descarga}
"""

metadata_file = RAW_DATA_DIR / "fuentes_datos_seguridad.txt"
with open(metadata_file, 'w', encoding='utf-8') as f:
    f.write(metadata_content)

print(f"✓ Guardado: {metadata_file}")
print("\n¡Proceso completado!")
