#Importacion de librerias
import requests
import pandas as pd
import pprint
import os
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
    response = requests.get(inegi_url)
    data = response.json()
    for indicador in data['Series']: 
        for observacion in indicador['OBSERVATIONS']:
            indicador_actual = indicador['INDICADOR']
            fecha = observacion['TIME_PERIOD']
            valor = observacion['OBS_VALUE']
            valores.append({"estado": estado, "indicador": indicador_actual, "indicador_nombre": id_ind[indicador_actual], "año" : fecha, "valor" : valor})

#Creacion del dataframe
df_edu = pd.DataFrame(valores)


#Guardado de dataframe en archivo CSV como raw
nombre_carpeta = '../.data/raw/'
nombre_archivo = 'educacionysalud.csv'

if not os.path.exists(nombre_carpeta):
    os.makedirs(nombre_carpeta)
    print("Se creó la carpeta .data/raw/")

ruta_guardado = os.path.join(nombre_carpeta, nombre_archivo)
df_edu.to_csv(ruta_guardado, index=False, encoding='utf-8')
print("Archivo con dataframe de educacion y salud creado")
