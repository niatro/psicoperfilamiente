# models.py
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargar claves API desde .env
load_dotenv()

Anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Configuración de modelos
models = {
    "openai": ["gpt-4o"],
    "anthropic": [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
}

def select_model():
    print("Select a model type:")
    model_types = list(models.keys())
    for i, key in enumerate(model_types, 1):
        print(f"{i}. {key}")
    model_type_index = int(input("Model type (number): ").strip()) - 1
    
    if model_type_index < 0 or model_type_index >= len(model_types):
        print("Invalid model type. Please choose a valid number.")
        return select_model()
    
    model_type = model_types[model_type_index]
    
    print(f"Select a model from {model_type}:")
    model_list = models[model_type]
    for j, model in enumerate(model_list, 1):
        print(f"{j}. {model}")
    model_name_index = int(input("Model name (number): ").strip()) - 1
    
    if model_name_index < 0 or model_name_index >= len(model_list):
        print("Invalid model name. Please choose a valid number.")
        return select_model()
    
    model_name = model_list[model_name_index]
    
    return model_type, model_name
