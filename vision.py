import openai
import pandas as pd
import os
import json
from dotenv import load_dotenv
from PIL import Image
import base64
import requests
from models import select_model
from prompt import prompt_r1
from anthropic import Anthropic

# Cargar claves API desde .env
load_dotenv()
Anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

def load_and_encode_image(image_path):
    file_extension = os.path.splitext(image_path)[1].lower()
    media_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base64_encoded_data = base64.b64encode(binary_data)
    base64_string = base64_encoded_data.decode('utf-8')
    return base64_string, media_type

def send_to_anthropic(model_name, image_path, prompt_text):
    base64_string, media_type = load_and_encode_image(image_path)
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_string}},
                {"type": "text", "text": prompt_text}
            ]
        }
    ]
    try:
        client = Anthropic()
        response = client.messages.create(
            model=model_name,
            max_tokens=2048,
            messages=message_list
        )
        return json.loads(response.content[0].text)
    except Exception as e:
        print(f"Error processing Anthropic API response: {str(e)}")
        return {}

def send_to_openai(model_name, image_path, prompt_text):
    base64_string, _ = load_and_encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            },
            {
                "role": "user",
                "content": f"data:image/jpg;base64,{base64_string}"
            }
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error processing OpenAI response: {str(e)}")
        return {}

def process_image(model_type, model_name, image_path):
    if model_type == 'anthropic':
        return send_to_anthropic(model_name, image_path, prompt_r1)
    elif model_type == 'openai':
        return send_to_openai(model_name, image_path, prompt_r1)
    else:
        print("Invalid model type selected.")
        return {}

def save_data_to_excel(data_records, output_file):
    df = pd.DataFrame(data_records)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

def main():
    carpeta_capturas = "capturas_linkedin"
    output_file = "datos_perfiles_linkedin.xlsx"
    
    data_records = []
    
    model_type, model_name = select_model()
    
    for filename in os.listdir(carpeta_capturas):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(carpeta_capturas, filename)
            print(f"Processing {filename} with model {model_name} ({model_type})...")
            result = process_image(model_type, model_name, image_path)
            if result:
                result['Imagen'] = filename
                data_records.append(result)
    
    if data_records:
        save_data_to_excel(data_records, output_file)
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
