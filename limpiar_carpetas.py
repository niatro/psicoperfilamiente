import os
import shutil

def limpiar_carpetas():
    carpetas = [
        "analisis_json",
        "analisis_photo",
        "captura_1",
        "capturas_linkedin",
        "json_profiles",
        "mails",
        "perfiles_completos",
        "profile_photos",
        "web_analysis_results",
        "web_search_results"
    ]

    for carpeta in carpetas:
        if os.path.exists(carpeta):
            try:
                # Eliminar todos los archivos y subcarpetas
                for filename in os.listdir(carpeta):
                    file_path = os.path.join(carpeta, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                print(f"Contenido de la carpeta '{carpeta}' eliminado con éxito.")
            except Exception as e:
                print(f"Error al limpiar la carpeta '{carpeta}': {e}")
        else:
            print(f"La carpeta '{carpeta}' no existe.")

if __name__ == "__main__":
    print("Iniciando limpieza de carpetas...")
    limpiar_carpetas()
    print("Proceso de limpieza completado.")
