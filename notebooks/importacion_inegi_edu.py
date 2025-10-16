#Importacion de librerias
import requests
import pandas as pd
import datetime
import os
import json
from dotenv import load_dotenv
from pathlib import Path # Importar la librería pathlib


# .parent se mueve un nivel hacia arriba (a la carpeta 'notebooks').
# .parent otra vez se mueve a la carpeta raíz del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# --- FIN DE LA CORRECCIÓN ---

#Lectura e importacion de datos
#Indicadores de educacion y salud
id_ind = {'3108001001' : 'Porcentaje analfabetismo',
          '1005000038' : 'Promedio escolaridad',
          '6200205239' : 'Poblacion con educacion basica',
          '6200205241' : 'Poblacion con bachillerato',
          '6200205242' : 'Poblacion con estudios superiores',
          '6207019020' : 'Porcentaje sin escolaridad',
          '1004000001' : 'Derechohabientes'
          }
#Identificadores de estados
id_estado = {
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

#API KEY de INEGI
load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, '.env')) # Carga el .env desde la raíz
token_inegi = os.getenv("token_inegi")

if not token_inegi:
    print("[ERROR] No se encontró el token 'token_inegi' en el archivo .env")
    exit()

indicadores = (",".join(list(id_ind.keys()))).strip()
valores = []

#Obtencion de datos para cada estado
for estado_nombre, estado_id in id_estado.items():
    inegi_url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicadores}/es/{estado_id}/false/BISE/2.0/{token_inegi}?type=json"
    
    print(f"Consultando datos para el estado: {estado_nombre}...")
    
    try:
        response = requests.get(inegi_url)
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.HTTPError as http_err:
        print(f" -> ERROR HTTP para '{estado_nombre}': {http_err}")
        continue
    except requests.exceptions.RequestException as req_err:
        print(f" -> ERROR de conexión para '{estado_nombre}': {req_err}")
        continue
    except json.JSONDecodeError:
        print(f" -> ADVERTENCIA: La respuesta para '{estado_nombre}' no es un JSON válido.")
        continue

    if not isinstance(data, dict) or 'Series' not in data:
        print(f" -> ADVERTENCIA: Los datos para '{estado_nombre}' no tienen la estructura esperada (diccionario con clave 'Series').")
        continue

    for indicador in data['Series']:
        observaciones = indicador.get('OBSERVATIONS', [])
        for observacion in observaciones:
            indicador_actual = indicador.get('INDICADOR')
            fecha = observacion.get('TIME_PERIOD')
            valor = observacion.get('OBS_VALUE')

            if all([indicador_actual, fecha, valor]):
                valores.append({
                    "id_estado": estado_id, 
                    "estado": estado_nombre, 
                    "indicador": indicador_actual, 
                    "indicador_nombre": id_ind.get(indicador_actual, "Desconocido"), 
                    "año": fecha, 
                    "valor": valor
                })

print("\nConsulta de datos a la API finalizada.")

def generar_registro_datos(fuentes, directorio_salida):
    os.makedirs(directorio_salida, exist_ok=True)
    ruta_completa = os.path.join(directorio_salida, "registro_fuentes_educacionysalud.txt")
    fecha_acceso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write("="*50 + "\nREGISTRO DE FUENTES DE DATOS\n" + "="*50 + "\n\n")
            for i, fuente in enumerate(fuentes, 1):
                f.write("-"*50 + f"\n--- Fuente de Datos #{i} ---\n")
                f.write(f"Nombre: {fuente.get('nombre', 'No especificado')}\n")
                f.write(f"Tipo: API\n")
                f.write(f"Fecha de Query: {fecha_acceso}\n")
                f.write(f"Endpoint: {fuente.get('endpoint', 'No especificado')}\n")
                params = fuente.get('parametros', {})
                if params:
                    f.write("Parámetros de Query:\n")
                    f.write(json.dumps(params, indent=4))
                    f.write("\n")
                f.write(f"URL Documentación: {fuente.get('url_documentacion', 'No especificada')}\n")
                f.write(f"Descripción: {fuente.get('descripcion', 'No especificada')}\n\n")
        print(f"Se ha generado el archivo en la ruta '{ruta_completa}' correctamente.")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

mis_fuentes = []
for codigo, nombre in id_ind.items():
    fuente = {
        "nombre": f"Indicador: {nombre} (Todos los estados)", "tipo": "API",
        "endpoint": f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{codigo}/es/{{id_estado}}/false/BISE/2.0/token_inegi",
        "parametros": {
            "indicador": codigo,
            "area_geografica": "Claves '01' a '32' (Todos los estados de la Republica Mexicana)",
            "reciente": "false", "fuente_datos": "BISE", "version_api": "2.0"
        },
        "url_documentacion": "https://www.inegi.org.mx/servicios/api_indicadores.html",
        "descripcion": f"Consulta a la API de INEGI para obtener la serie de datos sobre '{nombre}' para cada uno de los 32 estados de México."
    }
    mis_fuentes.append(fuente)

# --- CORRECCIÓN: Usar la ruta absoluta al proyecto ---
directorio_log = os.path.join(PROJECT_ROOT, 'references')
generar_registro_datos(mis_fuentes, directorio_log)

df_edu = pd.DataFrame(valores)

def descarga_csv(dataframe, nombre_carpeta, nombre_archivo):
    try:
        os.makedirs(nombre_carpeta, exist_ok=True)
        ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)
        dataframe.to_csv(ruta_completa, index=False, encoding='utf-8')
        print(f"Archivo con dataframe de educacion y salud creado en: '{ruta_completa}'")
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo: {e}")

# --- CORRECCIÓN: Usar la ruta absoluta al proyecto ---
carpeta_destino = os.path.join(PROJECT_ROOT, 'data', 'raw')
archivo_destino = 'educacionysalud_raw.csv'
descarga_csv(df_edu, carpeta_destino, archivo_destino)