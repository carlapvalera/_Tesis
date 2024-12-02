import shutil
import os

# Ruta del directorio donde se guardó el modelo
model_directory = "./saved_model"

# Verificar si la carpeta existe antes de intentar borrarla
if os.path.exists(model_directory):
    shutil.rmtree(model_directory)  # Eliminar la carpeta y su contenido
    print(f"Modelo eliminado de {model_directory}.")
else:
    print("El directorio no existe.")