import argparse
import logging
import getpass
from contextlib import contextmanager
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
import time
import random
import json
import shutil
from config import CHROME_PROFILE_PATH, EXTENSION_PATH, MIN_WAIT, MAX_WAIT, LINKEDIN_LOGIN_URL, EMAIL_SELECTOR, PASSWORD_SELECTOR, SUBMIT_BUTTON_SELECTOR

class LinkedInScraper:
    def __init__(self, profile_path, extension_path):
        self.profile_path = profile_path
        self.extension_path = extension_path

    @contextmanager
    def driver_context(self):
        driver = self.configure_driver()
        try:
            yield driver
        finally:
            driver.quit()

    def configure_driver(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-data-dir={self.profile_path}")
        options.add_argument(f"--load-extension={self.extension_path}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.113 Safari/537.36'})
        driver.maximize_window()
        return driver

    def login(self, driver, email, password):
        driver.get(LINKEDIN_LOGIN_URL)
        self.espera_aleatoria()

        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR))
            )
            self.type_slowly(email_input, email)

            password_input = driver.find_element(By.CSS_SELECTOR, PASSWORD_SELECTOR)
            self.type_slowly(password_input, password)
        
            submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR)
            submit_button.click()

            self.espera_aleatoria(5, 7)

        except Exception as e:
            logging.error(f"Error al iniciar sesión: {str(e)}")

    def type_slowly(self, element, text):
        for char in text:
            element.send_keys(char)
            self.espera_aleatoria(0.1, 0.3)

    @staticmethod
    def espera_aleatoria(min_segundos=MIN_WAIT, max_segundos=MAX_WAIT):
        time.sleep(random.uniform(min_segundos, max_segundos))

class ScreenshotManager:
    def __init__(self, output_dir_parcial, output_dir_completo):
        self.output_dir_parcial = output_dir_parcial
        self.output_dir_completo = output_dir_completo

    def capture_partial(self, driver, url):
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        file_name = f"{url.split('/')[-2]}.png"
        file_path = os.path.join(self.output_dir_parcial, file_name)
        driver.save_screenshot(file_path)
        logging.info(f"Captura parcial guardada en {file_path}")
        return file_path

    def prepare_full_capture(self, url):
        file_name = f"{url.split('/')[-2]}.png"
        return os.path.join(self.output_dir_completo, file_name)

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Profile Scraper")
    parser.add_argument("--email", help="LinkedIn login email")
    parser.add_argument("--password", help="LinkedIn login password")
    args = parser.parse_args()

    if not args.email:
        args.email = input("Introduce tu correo electrónico de LinkedIn: ")
    if not args.password:
        args.password = getpass.getpass("Introduce tu contraseña de LinkedIn: ")

    output_dir_completo = "capturas_linkedin"
    output_dir_parcial = "captura_1"
    
    scraper = LinkedInScraper(CHROME_PROFILE_PATH, EXTENSION_PATH)
    screenshot_manager = ScreenshotManager(output_dir_parcial, output_dir_completo)

    # Preguntar al usuario si quiere buscar múltiples personas o una sola
    busqueda_multiple = input("¿Desea buscar múltiples personas? (s/n): ").lower() == 's'

    urls = []

    if busqueda_multiple:
        input_file = "prueba_url.xlsx"
        try:
            df = pd.read_excel(input_file)
            if 'URL' not in df.columns:
                logging.error("Error: No se encontró la columna 'URL' en el archivo Excel.")
                return
        except FileNotFoundError:
            logging.error(f"Error: No se encontró el archivo '{input_file}'. Asegúrate de que el archivo existe y la ruta es correcta.")
            return
        except Exception as e:
            logging.error(f"Error al leer el archivo Excel: {str(e)}")
            return
    else:
        url = input("Introduce la URL del perfil de LinkedIn: ")
        urls = [{"url": url, "filePath": screenshot_manager.prepare_full_capture(url)}]

    with scraper.driver_context() as driver:
        # Iniciar sesión
        scraper.login(driver, args.email, args.password)
        
        # Procesar cada URL
        if busqueda_multiple:
            for _, row in df.iterrows():
                url = row['URL']
                logging.info(f"Procesando {url}")
                
                # Navegar a la URL
                driver.get(url)
                scraper.espera_aleatoria()
                
                # Capturar screenshots
                file_path_parcial = screenshot_manager.capture_partial(driver, url)
                file_path_completo = screenshot_manager.prepare_full_capture(url)
                
                # Capturar screenshot completo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Esperar a que la página se cargue completamente
                driver.save_screenshot(file_path_completo)
                logging.info(f"Captura completa guardada en {file_path_completo}")
                
                # Guardar información para el screenshot completo
                urls.append({"url": url, "filePath": file_path_completo})
        else:
            url = urls[0]['url']
            logging.info(f"Procesando {url}")
            
            # Navegar a la URL
            driver.get(url)
            scraper.espera_aleatoria()
            
            # Capturar screenshots
            file_path_parcial = screenshot_manager.capture_partial(driver, url)
            file_path_completo = urls[0]['filePath']
            
            # Capturar screenshot completo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Esperar a que la página se cargue completamente
            driver.save_screenshot(file_path_completo)
            logging.info(f"Captura completa guardada en {file_path_completo}")

    # El resto del código permanece igual...

    json_filename = 'urls.json'
    with open(json_filename, 'w') as json_file:
        json.dump(urls, json_file)
    logging.info(f"Archivo {json_filename} guardado con {len(urls)} URLs")

    if not shutil.which("node"):
        logging.error("Node.js no está instalado o no está en el PATH")
        return

    if not os.path.exists("screenshot.js"):
        logging.error("screenshot.js no se encuentra en el directorio actual")
        return

    try:
        result = subprocess.run(["node", "screenshot.js", json_filename], check=True, capture_output=True, text=True)
        logging.info("screenshot.js se ejecutó correctamente")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar screenshot.js: {e}")
        logging.error(f"Salida de error: {e.stderr}")

if __name__ == "__main__":
    # Asegurarse de que las carpetas existan
    for dir_path in ["capturas_linkedin", "captura_1"]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
