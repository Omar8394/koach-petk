# KOACH_PETK
Proyecto PETK: Gestión de recursos humanos

### Aspectos sobre el desarrollo del proyecto:

### - **Consideraciones sobre el control de versiones:**
#### 1.-Se tienen solo dos ramas "main" y "test", el commit inicial se realizo a la rama "test"(puede añadirse mas si se requieren).
#### 2.- Todos los cambios deben ir a la rama "test" primero que sera nuestra rama de desarrollo y de prueba, por favor no subir archivos a la rama main. El merge se realizara cuando los tester o el señor ali verifique que funcionan todos los cambios de algun sprint o ciclo, para trabajar en la rama "test" aqui algunos tips git clone para obtener el proyecto luego git fetch para traer todas las ramas y luego git checkout "test" para cambiarse a test, para verificar que esten en "test" git branch.
#### 3.- requeriments.txt debe ser completado con las librerias requeridas, por favor verificar las librerias utilizadas en las importaciones.
#### 4.-En sus archivos .gitignore añadir todas las carpetas de migraciones y pyche entre otros no relevantes por favor no incluir estos archivos en los commit.

### Pasos para ejecutar el proyecto:Pasos para ejecutar el proyecto:
#### Si es la primera vez que clonara el repositorio leer el punto 2 de los aspectos de control de versiones.
##### 1.- Instalar los paquetes que se encuentran en el archivo requiriments.txt puede hacerlo con su gestor de paquete preferido(pip,conda...).
##### 2.-En su manejador de bases de datos crear una base de datos de mysql.
##### 3.-crear un archivo llamado ".env" dentro de la carpeta "core" del proyecto ejemplo KOACH_PETK/core/.env este archivo se encarga de manejar todas las variables de entorno del proyecto como lo son las credenciales de la base de datos entre otros, alli debe definir un conjunto de variables para que el proyecto funcione,cabe destacar que este archivo funciona con la libreria environ. Aqui les dejo un ejemplo de como deberia quedar configurado:
[![environ.png](https://i.postimg.cc/SRQ3t588/environ.png)](https://postimg.cc/ph7smssX)
##### 4.-Debe realizar las migraciones del proyecto con los respectivos comandos.

##### 5- Crear un super usuario para ingresar por primera vez.

### Notas importantes:
#### Si no es la primera vez que ejecuta el proyecto(tiene su repositorio sincronizado con el remote de git) es posible que tenga problemas con las migraciones de ser el caso aqui algunos consejos:
##### 1.-Hacer un dropdabase eliminar su base de datos y crearla de nuevo.
##### 2.-Eliminar todas las migraciones del proyecto para ello existe un archivo llamado remove_migrations.py dentro del directorio raiz del proyecto este debe ejecutarse en modo consola, una vez ejecutado le preguntara si desea borrar las migraciones entonces ingresamos el texto "yes" y damos enter.
