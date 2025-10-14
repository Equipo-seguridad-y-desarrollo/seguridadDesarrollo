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
3. Ejecutar: python datos_seguridad_mexico.py
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

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
        "INEGI_API_TOKEN no está configurado. "
        "Por favor, configura tu token en el archivo .env"
    )

clave_indicador = "6204327085"  # CNI: percepción de inseguridad por cada 100 000 (18+).

entidades = {
    "00": "Nacional",
    "01": "Aguascalientes", "02": "Baja California", "03": "Baja California Sur", 
    "04": "Campeche", "05": "Coahuila", "06": "Colima", "07": "Chiapas", 
    "08": "Chihuahua", "09": "Ciudad de México", "10": "Durango", "11": "Guanajuato",
    "12": "Guerrero", "13": "Hidalgo", "14": "Jalisco", "15": "México", 
    "16": "Michoacán", "17": "Morelos", "18": "Nayarit", "19": "Nuevo León", 
    "20": "Oaxaca", "21": "Puebla", "22": "Querétaro", "23": "Quintana Roo",
    "24": "San Luis Potosí", "25": "Sinaloa", "26": "Sonora", "27": "Tabasco", 
    "28": "Tamaulipas", "29": "Tlaxcala", "30": "Veracruz", "31": "Yucatán", 
    "32": "Zacatecas"
}
claves_entidades = list(entidades.keys())
all_data = []

print("Descargando datos de percepción de inseguridad...")
for clave in claves_entidades:
    url = (f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/"
           f"{clave_indicador}/es/{clave}/false/BISE/2.0/{token}?type=json")  # API del Banco de Indicadores.
    try:
        response = requests.get(url, timeout=7)
        json_data = response.json()
        if "Series" in json_data and json_data["Series"]:
            serie = json_data["Series"][0]["OBSERVATIONS"]
            df = pd.DataFrame(serie)
            df["año"] = df["TIME_PERIOD"].astype(int)  # Años en la serie (2011–2025).
            df["valor"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")  # Personas 18+ por cada 100 000 que perciben inseguridad.
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
# Sugerencia de metadatos del archivo:
# periodicidad=anual; unidad=personas 18+ por cada 100 000; cobertura_temporal=2011–2025; fuente=INEGI ENVIPE/CNI.
df_final.to_csv("indicador_inseguridad_estados.csv", index=False)
print(f"\n✓ Guardado: indicador_inseguridad_estados.csv ({len(df_final)} registros)")

# ====== (2) Incidencia Delictiva Estatal 2015-2025 (CSV directo) ======
# Periodicidad: mensual; suele publicarse alrededor del día 20 de cada mes con cifras del mes inmediato anterior.
# Qué se mide: hechos delictivos ocurridos, con desagregación por entidad federativa (serie estatal).
# Ventana temporal del recurso: enero 2015 a agosto 2025 (corte vigente del dataset estatal).
# Fuente: Datos abiertos del SESNSP (portal institucional de incidencia delictiva).

print("\nDescargando datos de incidencia delictiva...")
url_crimen = "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv"  # Corte a agosto 2025.
try:
    df_crimen = pd.read_csv(url_crimen)
    # Sugerencia de metadatos del archivo:
    # periodicidad=mensual; unidad=hechos delictivos (conteos mensuales por tipo y entidad); 
    # cobertura_temporal=2015–ago 2025; fuente=SESNSP datos abiertos.
    df_crimen.to_csv("incidencia_delictiva_estatal_2015_2025.csv", index=False)
    print(f"✓ Guardado: incidencia_delictiva_estatal_2015_2025.csv ({len(df_crimen)} registros)")
except Exception as e:
    print(f"✗ Error descargando incidencia delictiva: {e}")

print("\n¡Proceso completado!")
