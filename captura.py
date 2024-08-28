import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from PIL import Image
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver_con_perfil_y_extension():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Ruta del perfil donde se encuentra la extensión
    profile_path = "C:/TempChromeProfile"
    options.add_argument(f"user-data-dir={profile_path}")
    
    # Asegurar que las extensiones se carguen
    options.add_argument("--load-extension=/ruta/de/la/extension")  # Reemplaza esta ruta con la ruta de tu extensión

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Maximizar la ventana del navegador
    driver.maximize_window()
    
    return driver

def espera_aleatoria(min_segundos, max_segundos):
    time.sleep(random.uniform(min_segundos, max_segundos))

def iniciar_sesion(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    espera_aleatoria(2, 4)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        for char in email:
            email_input.send_keys(char)
            espera_aleatoria(0.1, 0.3)

        password_input = driver.find_element(By.ID, "password")
        for char in password:
            password_input.send_keys(char)
            espera_aleatoria(0.1, 0.3)
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        espera_aleatoria(5, 7)

    except Exception as e:
        print(f"Error al iniciar sesión: {str(e)}")

def capturar_pantalla_completa(driver, file_path):
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Mantener el tamaño original de la ventana ya maximizada
    original_size = driver.get_window_size()
    
    stitched_image = Image.new('RGB', (total_width, total_height))
    
    y_position = 0
    part = 0
    while y_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {y_position})")
        time.sleep(0.3)
        
        screenshot_path = f"screenshot_part_{part}.png"
        driver.save_screenshot(screenshot_path)
        screenshot = Image.open(screenshot_path)

        stitched_image.paste(screenshot, (0, y_position))
        
        y_position += original_size['height']
        part += 1

        os.remove(screenshot_path)
    
    stitched_image.save(file_path)
    print(f"Captura de pantalla completa guardada en {file_path}")

def capturar_pantalla_parcial(driver, file_path):
    try:
        # Asegurarse de que la página esté en la parte superior antes de capturar
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)  # Dar tiempo para que la página se acomode en la parte superior

        # Capturar la pantalla completa en ese punto sin cambiar el tamaño
        screenshot = driver.get_screenshot_as_png()
        with open(file_path, "wb") as f:
            f.write(screenshot)
        print(f"Captura parcial (parte superior) guardada en {file_path}")
    except Exception as e:
        print(f"Error al capturar la pantalla parcial: {str(e)}")

def obtener_perfiles_linkedin(desde_archivo, email, password, output_dir_completo, output_dir_parcial):
    # Leer el archivo Excel con las URLs
    df = pd.read_excel(desde_archivo)

    # Asegurarse de que existe la columna 'URL'
    if 'URL' not in df.columns:
        print("Error: No se encontró la columna 'URL' en el archivo Excel.")
        return
    
    # Configurar el driver
    driver = configurar_driver_con_perfil_y_extension()
    
    try:
        # Iniciar sesión en LinkedIn
        iniciar_sesion(driver, email, password)
        
        # Iterar sobre cada URL en el archivo
        for index, row in df.iterrows():
            url = row['URL']
            print(f"Procesando {url}")
            driver.get(url)
            espera_aleatoria(3, 5)
            
            # Crear el nombre del archivo basándose en el identificador de LinkedIn
            file_name = f"{url.split('/')[-2]}.png"
            
            # Captura completa
            file_path_completo = os.path.join(output_dir_completo, file_name)
            capturar_pantalla_completa(driver, file_path_completo)
            
            # Captura parcial (solo la primera pantalla)
            file_path_parcial = os.path.join(output_dir_parcial, file_name)
            capturar_pantalla_parcial(driver, file_path_parcial)

    except Exception as e:
        print(f"Error al procesar los perfiles: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    desde_archivo = "prueba_url.xlsx"  # Archivo Excel con las URLs de LinkedIn
    email = input("Introduce tu correo electrónico de LinkedIn: ")
    password = input("Introduce tu contraseña de LinkedIn: ")
    
    # Carpetas de salida
    output_dir_completo = "capturas_linkedin"
    output_dir_parcial = "captura_1"
    
    # Crear carpetas si no existen
    if not os.path.exists(output_dir_completo):
        os.makedirs(output_dir_completo)
    
    if not os.path.exists(output_dir_parcial):
        os.makedirs(output_dir_parcial)
    
    obtener_perfiles_linkedin(desde_archivo, email, password, output_dir_completo, output_dir_parcial)

