import cv2
import dlib
import os
import numpy as np
from PIL import Image, ImageDraw

def recortar_circular(imagen, x, y, r):
    mask = Image.new("L", imagen.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
    output = Image.new("RGB", imagen.size)
    output.paste(imagen, mask=mask)
    return output.crop((x - r, y - r, x + r, y + r))

def recortar_mitad_izquierda(imagen_path):
    img = Image.open(imagen_path)
    ancho, alto = img.size
    mitad = ancho // 2
    img_izquierda = img.crop((0, 0, mitad, alto))
    return img_izquierda

def detectar_y_recortar_foto_perfil(imagen_original, output_dir):
    img_izquierda = recortar_mitad_izquierda(imagen_original)
    
    # Convertir la imagen a un formato compatible con OpenCV
    img_cv2 = cv2.cvtColor(np.array(img_izquierda), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    
    detector = dlib.get_frontal_face_detector()
    
    # Probar con diferentes ajustes para una búsqueda más exhaustiva
    rostros = detector(gray, 1)  # El segundo parámetro ajusta la búsqueda más exhaustiva

    if len(rostros) > 0:
        rostro = rostros[0]
        x, y, ancho, alto = rostro.left(), rostro.top(), rostro.width(), rostro.height()
        
        # Incrementar el radio para capturar una región más amplia
        radio = max(ancho, alto) * 1.3  # Aumentamos el radio al 150% del tamaño del rostro
        centro_x = x + ancho // 2
        centro_y = y + alto // 2
        
        imagen_recortada = recortar_circular(img_izquierda, centro_x, centro_y, int(radio))
        
        nombre_archivo = os.path.basename(imagen_original)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        ruta_guardado = os.path.join(output_dir, f"{nombre_sin_ext}_perfil.png")
        imagen_recortada.save(ruta_guardado)
        print(f"Foto de perfil guardada en: {ruta_guardado}")
    else:
        print(f"No se detectó ningún rostro en la imagen {imagen_original}.")

if __name__ == "__main__":
    carpeta_captura_1 = "captura_1"
    output_dir = "fotos_perfil"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(carpeta_captura_1):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            ruta_imagen = os.path.join(carpeta_captura_1, filename)
            print(f"Procesando {filename}...")
            detectar_y_recortar_foto_perfil(ruta_imagen, output_dir)
