# -*- coding: utf-8 -*-
__author__ = 'alexdzul'

"""
El script identifica las carpetas llamadas "migrations" dentro de nuestro
proyecto y elimina todos los archivos *.py
omitiendo los __init__.py.
Instrucciones:
=============
1. Copia el archivo "remove_migrations.py" dentro de la carpeta de tu proyecto.
    Ejemplo:
        MyProject/
            |-MyProject/
            |-manage.py
            |-README.md
            |-remove_migrations.py <---- Aqui va el archivo
2. Cambia el valor de la variable APPS_FOLDER con la ruta que contiene tus apps
3. Ejecuta el script con "python remove_migrations.py"
Advertencia:
============
-Se cuidadoso al utilizar este script ya que los archivos son eliminados
permanentemente. -Te sugerimos comprobar que has configurado correctamente
la ruta de tu carpeta de aplicaciones en la variable "APPS_FOLDER"
"""
import os
import sys
from distutils.util import strtobool

# Cambiar el valor de acuerdo a la configuración de tu proyecto.
APPS_FOLDER = "modulesApp"  # <- Ruta de nuestra carpeta contenedora de apps


# Obtenemos la ruta de nuestro archivo.
BASE_DIR = os.getcwd()
# Ruta completa para iniciar el proceso de eliminado
FULL_PATH = os.path.join(BASE_DIR, APPS_FOLDER)


def delete_migrations_files():
    """
    Modificado a la version de Python 3.8.10 por tadifred,
    ajustado errores en los comandos print() y raw_input, entre otros detalles de ejecucion
    """
    """
    Author: Alex Dzul @alexjs88
    Función que nos permite recorrer las carpetas de nuestro proyecto y elimina
    archivos que se encuentren en las
    carpetas llamadas "migrations".
    Nota: La función omite la eliminación de los archivos __init__.py
    """
    num_compile_files = num_migrations_files = 0
    print ("\nAnalizing your project .... \n")
    for (path, ficheros, archivos) in os.walk(FULL_PATH):
        # Si existe una carpeta entonces continua el flujo
        if 'migrations' in ficheros:
            for fichero in ficheros:  # <- Recorre los ficheros
                # Si encuentra una carpeta migrations entonces entra a ellas
                if fichero == "migrations":
                    migrations_path = os.path.join(path, fichero)
                    for (child_path, ficheros_2, archivos_2) in os.walk(migrations_path):  # NOQA
                        for archivo in archivos_2:
                            file_path = os.path.join(child_path, archivo)
                            # Si son compilados entonces eliminamos
                            if archivo[-3:] == "pyc":
                                os.remove(file_path)
                                print ("[Compiled File] "), file_path
                                num_compile_files = num_compile_files + 1
                            else:
                                # Excluye los archivos __init__.py
                                if not archivo == "__init__.py":
                                    # Si es un archivo *.py lo elimina
                                    if archivo[-2:] == "py":
                                        os.remove(file_path)
                                        print ("[Migration File] "), file_path
                                        num_migrations_files = \
                                            num_migrations_files + 1
    print ("\n===================== Execution Summary =========================")
    if num_compile_files == 0 and num_migrations_files == 0:
        print ("All your migrations folder are empty. Nothing was deleted")
    else:
        print ("Python files: {0}".format(num_migrations_files))
        print ("Compiled Python files: {0}".format(num_compile_files))
    print ("=================================================================\n")


def user_yes_no_query():
    """
    Author: Alex Dzul @alexjs88
    Función muestra en pantalla un aviso para que el usuario responde YES o NO.
    Si responde YES --> Se ejecuta la función delete_migrations_files()
    Si responde NO ---> La función se detiene sin ninguna acción a ejecutar.
    Si responde algo más --> La función solicita escribir respuesta válida Y/N.
    """
    sys.stdout.write(
        'Are you sure you want to delete all migrations files? [y/n]: ')
    while True:
        try:
            respuesta = strtobool(input().lower())
            if respuesta:
                delete_migrations_files()
            else:
                sys.stdout.write('\nOk, nothing was deleted\n\n')
            return True
        except ValueError:
            sys.stdout.write('Please enter: \'y\' o \'n\'.\n')

user_yes_no_query()
