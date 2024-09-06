def get_email_generation_prompt(profile_text):
    return f"""
# ROL
Soy Nicolás Sanhueza, CEO de la startup AInstein de Chile. Te encargo que redactes un correo electrónico promocional personalizado para nuestra empresa, basado en un perfil detallado del destinatario (Gerentes Generales y CEOS de empresas chilenas de Consultoría). Tu objetivo es crear un correo electrónico atractivo y personalizado que se ajuste a los intereses, las necesidades y los antecedentes del destinatario.

# CONTEXTO    
En primer lugar, revise detenidamente el perfil del destinatario:

{profile_text}

## **Objetivo principal del email:** Que el receptor del email se contacte con nosotros.

## **Objetivos secundarios del email:**
1. Que lea el mail completo.
2. Que entre a nuestra página web.

## **Descripción de la empresa:**  
AInstein es una empresa especializada en aumentar las capacidades cognitivas de personas y organizaciones mediante ASESORÍAs en inteligencia artificial de vanguardia. Dirigida principalmente a empresas de consultoría, ofrece asesorías puntuales y continuas, desarrollos personalizados basados en casos de uso específicos y outsourcing permanente de I+D en IA. Su enfoque único en empresas de consultoría les permite ofrecer soluciones customizadas como la implementación de IA central para negocios y el desarrollo de productos innovadores. La misión de AInstein es potenciar el procesamiento de información de entidades, asegurando que las personas y empresas sigan siendo parte activa del desarrollo del conocimiento. Con un equipo ágil de dos personas, la empresa busca transformar la forma en que se utiliza la IA en el mundo de los negocios.

# **Pautas para redactar el correo electrónico:**

1. Personaliza el contenido en función del perfil del destinatario, destacando aspectos de nuestra startup que se alineen con sus intereses, necesidades o experiencia.
2. Entrega contexto de la situación actual de los avances de la tecnología en IA. Desarrolla brevemente la siguiente idea:
"La adopción temprana de la tecnologías de venguardiar, permiten generar ventajas competitivas inmediatas y en el corto plazo a la entidad. Esto como obligación frente a la amenaza, que la competencia lo implemente primero."
3. Utiliza un tono amable y profesional que coincida con el sector y el puesto del destinatario.
4. Mantén el correo electrónico conciso y directo, con un objetivo de 3 o 4 párrafos breves.
5. Incluye una llamada a la acción clara que anime al destinatario a interactuar con nuestra startup.

# **Estructura del correo electrónico:**

1. **Asunto**: Ventana Temporal Anticipada para Adopción de IA. 
2. **Saludo:** Dirígete al destinatario por su nombre.
3. **Introducción:** Preséntate brevemente, presenta la startup y basado en el perfil que recibiste, encuentra elementos que enganchen tecnica y emocionalmente al destinatario.
4. **Propuesta de valor:** Explica cómo nuestra startup puede beneficiar a la empresa del destinatario, adaptada a su perfil.
5. **Llamada a la acción:** Invita al destinatario a realizar una acción específica (por ejemplo, programar una demostración, visitar nuestro sitio web, agendar una reunión).
6. **Cierre:** Agradece al destinatario y proporciona tu información de contacto (www.ainstein.cl; Teléfono: +56963058027).

# REGLAS GENERALES

- Utiliza un lenguaje natural y evita un lenguaje demasiado comercial o agresivo.
- Demuestra conocimiento de la industria o los intereses del destinatario.
- Resalta los puntos de venta únicos de nuestra startup que sean más relevantes para el destinatario.
- NO UTILIZAR caracteres o palabras que no sean en el idioma LATIN.
- NO UTILIZAR palabras exageradas como: impresionado, destacado, extraordinario, etc.
- NO UTILIZAR vocabulario ambiguo y generico, como: eficiencia, eficacia, maximizar, optimizar, etc.
- Utiliza "TU" y no "USTED".
- De acuerdo a la edad del destinatario, ajusta el lenguaje y utiliza emojis, en caso de que sea un publico más juvenil.

Escribe tu correo electrónico promocional personalizado dentro de las etiquetas `<email>`. No incluyas ningún texto de marcador de posición ni variables en tu resultado final.
    """
