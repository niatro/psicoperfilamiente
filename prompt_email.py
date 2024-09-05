def get_email_generation_prompt(profile_text):
    return f"""
    Eres un experto en redactar emails empresariales. Quiero que generes un email altamente persuasivo, amigable y único para un gerente de una empresa, presentando nuestra startup AInstein. Aquí está el perfil de la persona a la que va dirigido:

    {profile_text}

    Nuestra empresa se llama AInstein, y es un startup de IA que ofrece servicios a organizaciones para automatizar sus procesos mediante IA. Utilizamos herramientas como OpenAI, Anthropic, Autogen, y Llamaparse, y nos especializamos en Prompting, RAG, y agentes. Nuestro objetivo es convertirnos en el departamento de I+D de estas organizaciones.

    El email debe ser redactado como si lo estuviera escribiendo un antiguo compañero de la escuela, debe ser amigable, único y persuasivo. No debe sonar genérico ni ambiguo, pero sí debe causar una excelente impresión.
    """
