import os
import shutil

def file_make_dir(nombre):
    os.makedirs(nombre, exist_ok=True)

def file_make(nombre, nombre2, contenido, id, cod_error):
    if os.path.exists(nombre):
        with open(os.path.join(nombre, nombre2),"w") as id:
            id.write(contenido)
    else:
        print(cod_error)

def file_delete(nombre):
    os.chmod(nombre, 0o777)
    if os.path.isfile(nombre):
        try:
            os.remove(nombre)
            print(f"Archivo '{nombre}' eliminado.")
        except PermissionError:
            print(f"No tienes permisos para eliminar el archivo: {nombre}")
        except Exception as e:
            print(f"Ocurrió un error al eliminar el archivo: {nombre}. Error: {e}")
    elif os.path.isdir(nombre):
        try:
            shutil.rmtree(nombre)
            print(f"Directorio '{nombre}' eliminado.")
        except PermissionError:
            print(f"No tienes permisos para eliminar el directorio: {nombre}")
        except Exception as e:
            print(f"Ocurrió un error al eliminar el directorio: {nombre}. Error: {e}")
    else:
        print(f"La ruta '{nombre}' no existe.")

