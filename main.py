import subprocess

import sys

import os



def ejecutar_script(ruta_script):

    """

    Ejecuta un script de Python ubicado en la ruta especificada.

    """

    if not os.path.exists(ruta_script):

        print(f"Error: No se encontró el archivo en la ruta '{ruta_script}'.")

        return False



    print(f"Iniciando ejecucion de: {ruta_script}")

    try:

        resultado = subprocess.run(

            [sys.executable, ruta_script],

            check=True,        

            capture_output=True, 

            text=True          

        )


        if resultado.stdout:

            print(resultado.stdout)

       

        print(f"Finalizado: {ruta_script} se ejecuto correctamente.\n")

        return True

    except subprocess.CalledProcessError as e:

        print(f"Error al ejecutar {ruta_script}.")

        print(f"El script finalizo con un error (codigo de salida {e.returncode}).")


        print("Salida de error (stderr):")

        print(e.stderr)

        return False

    except Exception as e:

        print(f"Ocurrio un error inesperado con {ruta_script}: {e}")

        return False



if __name__ == "__main__":

    print("=============================================")

    print("INICIANDO PROCESO DE DESCARGA DE DATOS")

    print("=============================================\n")

    scripts_a_ejecutar = [

        "notebooks/1_variables_economicas_descarga_datos_crudos.py",

        "notebooks/descarga_datos_rezago.py",

        "notebooks/importacion_inegi_edu.py",

        "notebooks/datos_seguridad_mexico.py"

    ]


    for script in scripts_a_ejecutar:

        exito = ejecutar_script(script)

        if not exito:

            print("\nProceso detenido debido a un error en el script anterior.")

            sys.exit(1)



    print("=============================================")

    print("Exito: Todos los scripts se ejecutaron correctamente.")

    print("=============================================")