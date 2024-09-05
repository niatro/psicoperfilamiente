import cv2
import dlib
import os
import numpy as np
from PIL import Image, ImageDraw

class LinkedInProfileImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.face_detector = dlib.get_frontal_face_detector()
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
        left_half = self.crop_left_half(image_path)
        face = self.detect_face(left_half)
        
        if face:
            cropped_image = self.crop_circular_face(left_half, face)
        else:
            body = self.detect_body(left_half)
            if body is not None:
                cropped_image = self.crop_body(left_half, body)
            else:
                print(f"No se detectó ningún rostro ni cuerpo en la imagen {image_path}.")
                return

        # Asegurarse de que la imagen sea cuadrada sin añadir márgenes
        width, height = cropped_image.size
        size = max(width, height)
        new_image = Image.new("RGB", (size, size), (255, 255, 255))
        offset = ((size - width) // 2, (size - height) // 2)
        new_image.paste(cropped_image, offset)
        cropped_image = new_image

        output_path = self.get_output_path(image_path)
        cropped_image.save(output_path)
        print(f"Foto de perfil guardada en: {output_path}")

    @staticmethod
    def crop_left_half(image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            return img.crop((0, 0, width // 2, height))

    def detect_face(self, image):
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray, 1)
        return faces[0] if faces else None

    def detect_body(self, image):
        img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        bodies, _ = self.body_detector.detectMultiScale(img_cv2, winStride=(8, 8), padding=(32, 32), scale=1.05)
        return bodies[0] if len(bodies) > 0 else None

    @staticmethod
    def crop_circular_face(image, face):
        x, y, width, height = face.left(), face.top(), face.width(), face.height()
        radius = int(max(width, height) * 1.3)
        center_x, center_y = x + width // 2, y + height // 2

        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)

        output = Image.new("RGB", image.size)
        output.paste(image, mask=mask)
        return output.crop((center_x - radius, center_y - radius, center_x + radius, center_y + radius))

    @staticmethod
    def crop_body(image, body):
        x, y, width, height = body
        center_x, center_y = x + width // 2, y + height // 2
        size = max(width, height)
        left = max(0, center_x - size // 2)
        top = max(0, center_y - size // 2)
        right = min(image.width, left + size)
        bottom = min(image.height, top + size)

        cropped = image.crop((left, top, right, bottom))
        mask = Image.new("L", cropped.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        output = Image.new("RGB", cropped.size)
        output.paste(cropped, mask=mask)
        return output

    def get_output_path(self, input_path):
        filename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(filename)[0]
        return os.path.join(self.output_folder, f"{name_without_ext}_profile.png")

def main():
    input_folder = "captura_1"
    output_folder = "profile_photos"
    
    processor = LinkedInProfileImageProcessor(input_folder, output_folder)
    processor.process_images()

if __name__ == "__main__":
    main()
