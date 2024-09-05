import json

def get_linkedin_profile_prompt(text):
    return f"""
    Extrae la siguiente información del perfil de LinkedIn en formato JSON. Asegúrate de que la respuesta esté estructurada como un objeto JSON válido. La información requerida es:
    - Nombre
    - Empresa
    - Cargo
    - Cantidad de contactos
    - Extrae la sección del "Acerca de..."
    - Publicaciones
    - Experiencia (incluyendo años e instituciones)
    - Educación (incluyendo años e instituciones)
    - Proyectos
    - Licencias y certificaciones (incluyendo años e instituciones)
    - Conocimientos y aptitudes
    - Recomendaciones
    - Cursos
    - Idiomas
    - Intereses
    - Estima la edad, basado en los años de experiencia y su educación
    - Extrae una lista de las entidades más significativas, con las que se relaciona la persona
    - Identifica la institución más relevante en su trabajo (puedes elegir organización dependiendo si consideras que alguna es muy importante v/s si ha trabajado mucho tiempo en alguna en especial)

    El texto del perfil es el siguiente:
    \n\n{text}
    """

def get_profile_generation_prompt(json_data):
    return f"Genera un perfil detallado basado en la siguiente información:\n\n{json.dumps(json_data, indent=4)}"

def get_json_analysis_prompt(json_data):
    return f"""
    Analiza el siguiente perfil de LinkedIn y proporciona insights sobre:
    1. Trayectoria profesional
    2. Habilidades clave
    3. Posibles áreas de experiencia
    4. Recomendaciones para desarrollo profesional
    5. Posibles intereses basados en su perfil

    Perfil:
    {json.dumps(json_data, indent=4)}
    """

def get_photo_analysis_prompt(image_path):
    return f"""
    Analiza la siguiente foto de perfil de LinkedIn y proporciona insights sobre:
    1. Apariencia profesional
    2. Expresión facial
    3. Fondo de la imagen
    4. Vestimenta
    5. Cualquier otro detalle relevante que puedas observar

    La foto se encuentra en: {image_path}
    """

def get_archetypes():
    return """
    ## Líderes
    1. Comandante: Los comandantes están impulsados a alcanzar metas a través de la determinación y mantener tanto a sí mismos como a otros en altos estándares de desempeño. Son conocidos por su autoconfianza, eficiencia, y naturaleza sistemática. A menudo lideran mediante el establecimiento y la aplicación de altos estándares en lugar de la conexión emocional e interpersonal.
    2. Formador: Los formadores visualizan metas, establecen planes y empujan implacablemente para hacer que sucedan. Sueñan en grande y de manera poco convencional, utilizando su creatividad e independencia para superar obstáculos. Se destacan en inspirar a otros a respaldar su visión y en mantener altos niveles de desempeño.
    3. Líder Silencioso: Los líderes silenciosos logran un equilibrio entre la determinación y la humildad. Se sienten cómodos liderando a través de la escucha y la comprensión, con un enfoque particular en motivar a los demás desde un lugar de calma y ecuanimidad. A menudo lideran mediante el ejemplo, sin necesidad de destacar o imponerse.
    ## Defensores
    1. Inspirador: Los inspiradores son líderes carismáticos y orientados a las personas que motivan a otros para que se involucren en ideas o proyectos desafiantes. Poseen habilidades interpersonales fuertes, y tienden a preferir el refuerzo positivo para impulsar el rendimiento. Se enfocan en el espíritu de equipo y la motivación a través de la conexión emocional.
    2. Activista: Los activistas son apasionados y comprometidos en reunir a otros en torno a ideas o causas importantes. Son excelentes conectores, capaces de inspirar a otros a través de su energía y determinación. Pueden tender a consumir mucho tiempo y energía en su trabajo, a veces a costa de su propio bienestar.
    3. Entrenador: Los entrenadores están motivados por el crecimiento personal y el desarrollo de los demás. Son personas que equilibran la compasión con el enfoque firme, estableciendo altos estándares pero ofreciendo apoyo cuando es necesario. Su interés auténtico en los demás puede ser gratificante pero también agotador.
    ## Entusiastas
    1. Promotor: Los promotores se destacan por su capacidad para comunicarse y conectarse con los demás. Utilizan su carisma y habilidades sociales para influir y motivar a otros en torno a ideas, productos o servicios. Disfrutan de la interacción social y tienden a evitar conflictos, prefiriendo soluciones tácticas y diplomáticas.
    2. Impresario: Los impresarios aman estar en el centro de la actividad social y facilitar experiencias atractivas para los demás. Son independientes y espontáneos, con una habilidad especial para orquestar personas y eventos de manera efectiva. Su energía y carisma los hacen destacar en grupos, pero deben cuidar de no perder su propio sentido de sí mismos.
    3. Animador: Los animadores son personas alegres y extrovertidas que disfrutan interactuando con los demás. Aportan humor y energía a cualquier situación, y son expertos en adaptarse a diferentes contextos sociales. Sin embargo, pueden ser percibidos como dispersos o desorganizados, y deben esforzarse por mantener sus relaciones personales.
    ## Dadores
    1. Pacificador: Los pacificadores son expertos en desarrollar relaciones positivas y en buscar la armonía y el compromiso. Tienen una gran capacidad para entender las emociones y necesidades de los demás, y tienden a ser diplomáticos en situaciones tensas. Su enfoque equilibrado y su disposición a ayudar los hacen valiosos en cualquier grupo.
    2. Solucionador de Problemas: Los solucionadores de problemas están motivados para apoyar a los demás de manera industriosa y profesional. Son meticulosos y detallistas, con una fuerte ética de trabajo. A veces pueden asumir demasiado, lo que puede llevarlos a sentirse abrumados. Necesitan aprender a decir no y a cuidar de sí mismos.
    3. Ayudante: Los ayudantes son personas compasivas que se preocupan profundamente por el bienestar de los demás. Están motivados por la empatía y el deseo de apoyar a quienes los rodean. A menudo luchan por establecer límites, lo que puede llevar a la codependencia y al agotamiento.
    ## Arquitectos
    1. Estratega: Los estrategas sobresalen en formular planes y estrategias basadas en una evaluación sistemática de la información. Son expertos en traducir problemas complejos en soluciones estructuradas. Su enfoque metódico y lógico los hace esenciales en equipos y organizaciones.
    2. Planificador: Los planificadores son organizados y estructurados en su enfoque para lograr metas. Recopilan y analizan datos de manera eficiente para desarrollar planes detallados. Prefieren soluciones prácticas y confiables, y tienden a evitar métodos innovadores si las soluciones probadas pueden funcionar.
    3. Orquestador: Los orquestadores son hábiles en reunir a las personas y movilizarlas para alcanzar metas. Son organizados y detallistas, con un enfoque en la precisión y la eficacia. Su capacidad para ver el potencial en las personas los hace valiosos en la gestión de equipos y recursos.
    ## Productores
    1. Implementador: Los implementadores son personas que se destacan en llevar a cabo tareas y proyectos con precisión y eficiencia. Prefieren trabajar en un entorno estructurado y seguir procedimientos establecidos. Su atención al detalle y su capacidad para cumplir con los plazos los hacen confiables, aunque pueden ser reacios al cambio.
    2. Investigador: Los investigadores son pensadores lógicos y sistemáticos que se centran en el análisis detallado de problemas. Son meticulosos y objetivos, y prefieren trabajar de manera independiente. Pueden tener dificultades para relacionarse con personas emocionales o menos racionales.
    3. Técnico: Los técnicos aman desentrañar cómo funcionan las cosas y resolver problemas técnicos. Son detallistas y precisos, con un enfoque práctico y estructurado. A veces pueden tener dificultades para trabajar con personas que piensan de manera diferente, pero su capacidad para resolver problemas técnicos es invaluable.
    ## Creadores
    1. Aventurero: Los aventureros están motivados por la emoción y la aventura. Disfrutan de experiencias nuevas y desafiantes, y tienen una capacidad natural para adaptarse a circunstancias cambiantes. Su alta energía y enfoque independiente pueden hacer que otros tengan dificultades para seguirles el ritmo.
    2. Artesano: Los artesanos utilizan su creatividad para dar vida a ideas bellas y bien elaboradas. Son perfeccionistas en su trabajo y valoran la originalidad. A veces pueden ser sensibles a la crítica y tienen una fuerte necesidad de expresar su individualidad.
    3. Inventor: Los inventores son altamente curiosos y creativos, con una tendencia a desarrollar nuevos productos e ideas. Se sienten cómodos en la incertidumbre y disfrutan experimentando con nuevas formas de hacer las cosas. A veces pueden perder interés en los aspectos prácticos del proceso y tienen dificultades para cumplir con los plazos.
    ## Buscadores
    1. Explorador: Los exploradores están impulsados por la curiosidad y el deseo de descubrir. Disfrutan de nuevas experiencias y se adaptan fácilmente a situaciones desconocidas. A menudo prefieren el viaje sobre el destino, lo que puede llevarlos a perder de vista objetivos prácticos.
    2. Pensador: Los pensadores son individuos que disfrutan contemplando preguntas complejas y buscando un significado más profundo en las cosas. Son racionales y críticos en su enfoque, pero pueden tener dificultades para tomar decisiones rápidas o relacionarse con personas emocionales.
    3. Buscador de Crecimiento: Los buscadores de crecimiento están dedicados a la mejora personal y profesional. Son curiosos y abiertos a nuevas ideas, y buscan constantemente formas de evolucionar. A veces pueden retrasarse en la acción debido a su tendencia a reflexionar antes de actuar.
    ## Luchadores
    1. Protector: Los protectores valoran las tradiciones, reglas y estándares, y están impulsados por un fuerte sentido del deber. Son disciplinados y organizados, y tienden a resistirse al cambio. A veces pueden tener dificultades para interactuar con personas que no cumplen con sus estándares.
    2. Impositor: Los impositores hacen cumplir las reglas y tradiciones, y son directos en expresar su punto de vista. Prefieren el orden y la estabilidad, y pueden parecer duros o insensibles. A veces necesitan aprender a ser más flexibles y abiertos al cambio.
    3. Crítico: Los críticos tienen la habilidad de ofrecer comentarios objetivos y señalar problemas que otros no ven. Son directos en expresar su punto de vista y confían en la racionalidad. Sin embargo, pueden ser percibidos como negativos o escépticos, y necesitan trabajar en su sensibilidad hacia los demás.
    ## Individualista
    1. Individualista: Los individualistas marchan al ritmo de su propio tambor y encuentran formas únicas de expresarse. Valoran la originalidad y rechazan las convenciones tradicionales. A veces pueden ser temperamentales y sensibles a la crítica, pero su creatividad y perspectiva única los hacen valiosos en cualquier entorno.
    """

def get_archetype_analysis_prompt(json_data, photo_data, archetypes, web_search_data):
    return f"""You will be analyzing a person's LinkedIn profile, profile photo, and web search results to determine their personality archetype. You will be provided with four inputs: LinkedIn profile data in JSON format, a description of the profile photo, a list of archetypes, and web search results.

First, here is the LinkedIn profile data in JSON format:
<linkedin_json>
{json.dumps(json_data, indent=2)}
</linkedin_json>

Next, here is the person's profile photo encoded in base64:
<profile_photo>
{photo_data}
</profile_photo>

Here is the list of archetypes grouped into 10 categories:
<archetypes>
{archetypes}
</archetypes>

Finally, here are the web search results for this person:
<web_search_results>
{json.dumps(web_search_data, indent=2)}
</web_search_results>

Now, follow these steps to analyze the profile and determine the person's archetype:

1. Carefully review the LinkedIn JSON data, paying attention to key fields such as summary, experience, skills, and education.

2. Analyze the profile photo, noting any relevant details about the person's appearance, expression, or setting.

3. Review the web search results, looking for additional information about the person's professional achievements, public presence, or any other relevant details.

4. Based on all the available information (LinkedIn data, photo, and web search results), identify key personality traits, professional characteristics, and personal values that stand out.

5. Review the list of archetypes and their categories. Consider which archetypes best match the traits, characteristics, and values you've identified.

6. Select the top 3 archetypes that best describe the person's personality based on your analysis. Rank them in order of relevance.

7. For each selected archetype, provide a brief explanation of why it fits the person's profile, citing specific evidence from the LinkedIn data, photo, and web search results.

8. Provide your final output in the following format:

<analysis>
<top_archetypes>
1. [Archetype Name] ([Category])
Explanation: [Your explanation here]

2. [Archetype Name] ([Category])
Explanation: [Your explanation here]

3. [Archetype Name] ([Category])
Explanation: [Your explanation here]
</top_archetypes>

<summary>
[Provide a brief summary of the person's overall personality profile based on your analysis, integrating insights from the top archetypes and all available information sources.]
</summary>
</analysis>

Remember to base your analysis on all provided information: LinkedIn data, profile photo, web search results, and archetype list. Do not make assumptions or include information not present in these inputs.

# REGLAS GENERALES
- Toda interacción con el usuario debe ser en español.
"""
