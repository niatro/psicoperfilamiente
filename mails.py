import openai
import anthropic
import os
from dotenv import load_dotenv

# Cargar claves API desde .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')

# Configuración de modelos
models = {
    "openai": [
        "gpt-4o",
        "gpt-4o-mini"
    ],

    "anthropic": [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
}

def select_model():
    print("Selecciona el tipo de modelo:")
    model_types = list(models.keys())
    for i, key in enumerate(model_types, 1):
        print(f"{i}. {key}")
    model_type_index = int(input("Tipo de modelo (número): ").strip()) - 1
    
    if model_type_index < 0 or model_type_index >= len(model_types):
        print("Tipo de modelo inválido. Elige un número válido.")
        return select_model()
    
    model_type = model_types[model_type_index]
    
    print(f"Selecciona un modelo de {model_type}:")
    model_list = models[model_type]
    for j, model in enumerate(model_list, 1):
        print(f"{j}. {model}")
    model_name_index = int(input("Nombre del modelo (número): ").strip()) - 1
    
    if model_name_index < 0 or model_name_index >= len(model_list):
        print("Nombre del modelo inválido. Elige un número válido.")
        return select_model()
    
    model_name = model_list[model_name_index]
    
    return model_type, model_name

def generate_email_with_gpt4(profile_text, model_name):
    prompt = f"""
    Eres un experto en redactar emails empresariales. Quiero que generes un email altamente persuasivo, amigable y único para un gerente de una empresa, presentando nuestra startup AInstein. Aquí está el perfil de la persona a la que va dirigido:

    {profile_text}

    Nuestra empresa se llama AInstein, y es un startup de IA que ofrece servicios a organizaciones para automatizar sus procesos mediante IA. Utilizamos herramientas como OpenAI, Anthropic, Autogen, y Llamaparse, y nos especializamos en Prompting, RAG, y agentes. Nuestro objetivo es convertirnos en el departamento de I+D de estas organizaciones.

    El email debe ser redactado como si lo estuviera escribiendo un antiguo compañero de la escuela, debe ser amigable, único y persuasivo. No debe sonar genérico ni amiguo, pero sí debe causar una excelente impresión.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que genera emails personalizados de manera amigable y persuasiva."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error al generar el email con GPT-4: {str(e)}")
        return None
    
def generate_email_with_anthropic(profile_text, model_name):
    client = anthropic.Anthropic()
    prompt = f"Quiero que generes un email altamente persuasivo, amigable y único para un gerente de una empresa, presentando nuestra startup AInstein. Aquí está el perfil de la persona a la que va dirigido:\n\n{profile_text}\n\nNuestra empresa se llama AInstein, y es un startup de IA que ofrece servicios a organizaciones para automatizar sus procesos mediante IA. Utilizamos herramientas como OpenAI, Anthropic, Autogen, y Llamaparse, y nos especializamos en Prompting, RAG, y agentes. Nuestro objetivo es convertirnos en el departamento de I+D de estas organizaciones.\n\nEl email debe ser redactado como si lo estuviera escribiendo un antiguo compañero de la escuela, debe ser amigable, único y persuasivo. No debe sonar genérico ni ambiguo, pero sí debe causar una excelente impresión."

    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=1024,
            system="Eres un asistente que genera emails personalizados de manera amigable y persuasiva.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Verificamos si la respuesta es una lista y tomamos el primer elemento si lo es
        if isinstance(response.content, list):
            return response.content[0].text
        # Si no es una lista, asumimos que es un objeto con un atributo 'text'
        return response.content.text
    except Exception as e:
        print(f"Error al generar el email con Anthropic: {str(e)}")
        return None

def save_email(email_text, output_file):
    with open(output_file, 'w') as text_file:
        text_file.write(email_text)
    print(f"Email guardado en {output_file}")

def main():
    carpeta_perfiles = "perfiles"
    carpeta_mails = "mails"
    
    if not os.path.exists(carpeta_mails):
        os.makedirs(carpeta_mails)
    
    model_type, model_name = select_model()
    
    for filename in os.listdir(carpeta_perfiles):
        if filename.endswith(".txt"):
            with open(os.path.join(carpeta_perfiles, filename), 'r') as perfil_file:
                profile_text = perfil_file.read()
                
            print(f"Generando email para {filename} usando {model_type}:{model_name}...")
            
            if model_type == "openai":
                email_text = generate_email_with_gpt4(profile_text, model_name)  # Aquí pasamos model_name
            else:
                email_text = generate_email_with_anthropic(profile_text, model_name)
            
            if email_text:
                output_file = os.path.join(carpeta_mails, f"{os.path.splitext(filename)[0]}_email.txt")
                save_email(email_text, output_file)

if __name__ == "__main__":
    main()