import cv2
import dlib
import os
import numpy as np
from PIL import Image

class LinkedInProfileImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.face_detector_dlib = dlib.get_frontal_face_detector()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.body_detector = cv2.HOGDescriptor()
        self.body_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def process_images(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(self.input_folder, filename)
                self.process_single_image(input_path)

    def process_single_image(self, image_path):
        print(f"Procesando {os.path.basename(image_path)}...")
        # Abrir la imagen original
        original_image = Image.open(image_path).convert('RGB')

        # Realizar recorte vertical por la mitad y quedarse con la parte izquierda
        width, height = original_image.size
        left_half = original_image.crop((0, 0, width // 2, height))

        # Realizar recorte horizontal por la mitad y quedarse con la parte superior
        upper_left_quarter = left_half.crop((0, 0, left_half.width, left_half.height // 2))

        # Intentar detectar rostro en la imagen recortada (Método 1 - Dlib)
        face = self.detect_face_dlib(upper_left_quarter)
        if face:
            cropped_image = self.crop_face_rectangle_dlib(upper_left_quarter, face)
        else:
            # Intentar detectar rostro en la imagen recortada (Método 2 - Haar Cascades)
            face_haar = self.detect_face_haar(upper_left_quarter)
            if face_haar is not None:
                cropped_image = self.crop_face_rectangle_haar(upper_left_quarter, face_haar)
            else:
                # Si no se detecta rostro, intentar detectar cuerpo en la imagen recortada
                body = self.detect_body(upper_left_quarter)
                if body is not None:
                    cropped_image = self.crop_body_rectangle(upper_left_quarter, body)
                else:
                    # Si no se detecta rostro ni cuerpo, usar el recorte de coordenadas en la imagen original
                    cropped_image = self.crop_profile_area_fixed(original_image)
                    if cropped_image is None:
                        print(f"No se pudo recortar la foto de perfil en {image_path}.")
                        return

        # Redimensionar la imagen a un tamaño estándar sin agregar bordes blancos
        cropped_image = cropped_image.resize((256, 256), Image.LANCZOS)

        output_path = self.get_output_path(image_path)
        cropped_image.save(output_path)
        print(f"Foto de perfil guardada en: {output_path}")

    def detect_face_dlib(self, image):
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector_dlib(gray, 1)
        return faces[0] if faces else None

    def detect_face_haar(self, image):
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return faces[0] if len(faces) > 0 else None

    def detect_body(self, image):
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        bodies, _ = self.body_detector.detectMultiScale(img_cv2, winStride=(8, 8), padding=(32, 32), scale=1.05)
        return bodies[0] if len(bodies) > 0 else None

    def crop_face_rectangle_dlib(self, image, face):
        x, y, width, height = face.left(), face.top(), face.width(), face.height()
        # Aumentar el área alrededor del rostro
        padding = int(max(width, height) * 0.8)
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.width, x + width + padding)
        y2 = min(image.height, y + height + padding)
        return image.crop((x1, y1, x2, y2))

    def crop_face_rectangle_haar(self, image, face):
        x, y, width, height = face
        # Aumentar el área alrededor del rostro
        padding = int(max(width, height) * 0.8)
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.width, x + width + padding)
        y2 = min(image.height, y + height + padding)
        return image.crop((x1, y1, x2, y2))

    def crop_body_rectangle(self, image, body):
        x, y, width, height = body
        # Aumentar el área alrededor del cuerpo
        padding = int(max(width, height) * 0.2)
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.width, x + width + padding)
        y2 = min(image.height, y + height + padding)
        return image.crop((x1, y1, x2, y2))

    def crop_profile_area_fixed(self, image):
        # Coordenadas de recorte ajustadas para la imagen original
        x1 = 270
        y1 = 150
        x2 = 540
        y2 = 420

        # Verificar que las coordenadas estén dentro de la imagen
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)

        if x2 > x1 and y2 > y1:
            cropped_img = image.crop((x1, y1, x2, y2))
            return cropped_img
        else:
            return None

    def get_output_path(self, input_path):
        filename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(filename)[0]
        return os.path.join(self.output_folder, f"{name_without_ext}_profile.jpg")

def main():
    input_folder = "captura_1"
    output_folder = "profile_photos"

    processor = LinkedInProfileImageProcessor(input_folder, output_folder)
    processor.process_images()

if __name__ == "__main__":
    main()
