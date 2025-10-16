#Importacion de librerias
import requests
import pandas as pd
import datetime
import os
import json
from dotenv import load_dotenv

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
    "Aguascalientes": "01",
    "Baja California": "02",
    "Baja California Sur": "03",
    "Campeche": "04",
    "Coahuila de Zaragoza": "05",
    "Colima": "06",
    "Chiapas": "07",
    "Chihuahua": "08",
    "Ciudad de México": "09",
    "Durango": "10",
    "Guanajuato": "11",
    "Guerrero": "12",
    "Hidalgo": "13",
    "Jalisco": "14",
    "México": "15",
    "Michoacán de Ocampo": "16",
    "Morelos": "17",
    "Nayarit": "18",
    "Nuevo León": "19",
    "Oaxaca": "20",
    "Puebla": "21",
    "Querétaro": "22",
    "Quintana Roo": "23",
    "San Luis Potosí": "24",
    "Sinaloa": "25",
    "Sonora": "26",
    "Tabasco": "27",
    "Tamaulipas": "28",
    "Tlaxcala": "29",
    "Veracruz": "30",
    "Yucatán": "31",
    "Zacatecas": "32"
}

#API KEY de INEGI
load_dotenv()
token_inegi = os.getenv("token_inegi")

indicadores = (",".join(list(id_ind.keys()))).strip()
valores = []

#Obtencion de datos para cada estado
for estado in id_estado:
    inegi_url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicadores}/es/{id_estado[estado]}/false/BISE/2.0/{token_inegi}?type=json"
    
    print(f"Consultando datos para el estado: {estado}...")
    response = requests.get(inegi_url)
    
    # ------------------------------------------------------------------
    # --- PASO 1: Validar que la solicitud a la API fue exitosa ---
    # ------------------------------------------------------------------
    if response.status_code != 200:
        print(f"  -> ADVERTENCIA: La API devolvió un error para '{estado}'. Código de estado: {response.status_code}")
        print(f"     Respuesta: {response.text[:100]}") # Muestra los primeros 100 caracteres de la respuesta
        continue  # Salta al siguiente estado

    # ------------------------------------------------------------------
    # --- PASO 2: Intentar convertir la respuesta a JSON ---
    # ------------------------------------------------------------------
    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"  -> ADVERTENCIA: La respuesta para '{estado}' no es un JSON válido.")
        continue # Salta al siguiente estado

    # ------------------------------------------------------------------
    # --- PASO 3: Validar que la estructura de datos es la esperada ---
    # ------------------------------------------------------------------
    # Revisa si 'data' es una lista, no está vacía, y el primer elemento es un diccionario con la clave 'Series'
    if not isinstance(data, list) or not data or 'Series' not in data[0]:
        print(f"  -> ADVERTENCIA: Los datos para '{estado}' no tienen la estructura esperada (lista con clave 'Series').")
        continue # Salta al siguiente estado

    # ------------------------------------------------------------------
    # --- Si todas las validaciones pasan, procesamos los datos ---
    # ------------------------------------------------------------------
    for indicador in data[0]['Series']:
        observaciones = indicador.get('OBSERVATIONS', []) # Usar .get() es más seguro
        for observacion in observaciones:
            indicador_actual = indicador.get('INDICADOR')
            fecha = observacion.get('TIME_PERIOD')
            valor = observacion.get('OBS_VALUE')

            if all([indicador_actual, fecha, valor]): # Asegura que ningún valor sea nulo
                valores.append({
                    "id_estado": id_estado[estado], 
                    "estado": estado, 
                    "indicador": indicador_actual, 
                    "indicador_nombre": id_ind.get(indicador_actual, "Desconocido"), 
                    "año": fecha, 
                    "valor": valor
                })

print("\nConsulta de datos a la API finalizada.")

#Función de creación de archivo de información de descarga
def generar_registro_datos(fuentes, directorio_salida = r"..\references"):
    """
    Genera un archivo de texto con la descripción de las fuentes de datos,
    adaptado para manejar tanto archivos estáticos como consultas a APIs.

    Args:
        fuentes (list): Una lista de diccionarios con la info de cada fuente.
        directorio_salida (str): El nombre de la carpeta donde se guardará el archivo.
    """
    os.makedirs(directorio_salida, exist_ok=True)
    ruta_completa = os.path.join(directorio_salida, "registro_fuentes_educacionysalud.txt")
    fecha_acceso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write("="*50 + "\n")
            f.write("REGISTRO DE FUENTES DE DATOS\n")
            f.write("="*50 + "\n\n")

            for i, fuente in enumerate(fuentes, 1):
                f.write("-"*50 + "\n")
                f.write(f"--- Fuente de Datos #{i} ---\n")
                f.write(f"Nombre: {fuente.get('nombre', 'No especificado')}\n")
                
                # Revisa si es una API o un archivo y escribe los campos correspondientes
                if fuente.get('tipo') == 'API':
                    f.write(f"Tipo: API\n")
                    f.write(f"Fecha de Query: {fecha_acceso}\n")
                    f.write(f"Endpoint: {fuente.get('endpoint', 'No especificado')}\n")
                    
                    # Formatea los parámetros para que sean legibles
                    params = fuente.get('parametros', {})
                    if params:
                        f.write("Parámetros de Query:\n")
                        f.write(json.dumps(params, indent=4))
                        f.write("\n")
                        
                    f.write(f"URL Documentación: {fuente.get('url_documentacion', 'No especificada')}\n")
                else: # Asume que es un archivo por defecto
                    f.write(f"Tipo: Archivo Estático\n")
                    f.write(f"Fecha de Descarga: {fecha_acceso}\n")
                    f.write(f"URL de Descarga: {fuente.get('url_descarga', 'No especificada')}\n")
                    f.write(f"Enlace para más información: {fuente.get('url_info', 'No especificado')}\n")
                
                f.write(f"Descripción: {fuente.get('descripcion', 'No especificada')}\n\n")

        print(f"Se ha generado el archivo en la ruta '{ruta_completa}' correctamente.")

    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

mis_fuentes = []

for codigo, nombre in id_ind.items():
    fuente = {
        "nombre": f"Indicador: {nombre} (Todos los estados)",
        "tipo": "API",
        # El endpoint se muestra como una plantilla para indicar que se iteró sobre el estado
        "endpoint": f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{codigo}/es/{{id_estado}}/false/BISE/2.0/token_inegi",
        "parametros": {
            "indicador": codigo,
            # Se especifica el rango geográfico de la consulta
            "area_geografica": "Claves '01' a '32' (Todos los estados de la Republica Mexicana)",
            "reciente": "false",
            "fuente_datos": "BISE",
            "version_api": "2.0"
        },
        "url_documentacion": "https://www.inegi.org.mx/servicios/api_indicadores.html",
        "descripcion": f"Consulta a la API de INEGI para obtener la serie de datos sobre '{nombre}' para cada uno de los 32 estados de México."
    }
    mis_fuentes.append(fuente)

#Creación de archivo de registro de descarga
generar_registro_datos(mis_fuentes)


#Creacion del dataframe
df_edu = pd.DataFrame(valores)

#Función de guardado de dataframe en archivo CSV como raw
def descarga_csv(dataframe, nombre_carpeta, nombre_archivo):
    """
    Guarda el DataFrame en un archivo CSV en la carpeta destino.

    Args:
        dataframe (pd.DataFrame): El DataFrame a guardar.
        nombre_carpeta (str): La ruta de la carpeta donde se guarda el archivo.
        nombre_archivo (str): El nombre del archivo CSV.
    """
    try:
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            print(f"Se creó la carpeta: '{nombre_carpeta}'")

        ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)
        dataframe.to_csv(ruta_completa, index=False, encoding='utf-8')
        
        print(f"Archivo con dataframe de educacion y salud creado en: '{ruta_completa}'")

    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo: {e}")

#Creación de archivo de datos CSV
carpeta_destino = '../data/raw/'
archivo_destino = 'educacionysalud_raw.csv'

descarga_csv(df_edu, carpeta_destino, archivo_destino)
