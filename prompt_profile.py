import json

def get_linkedin_profile_prompt(text):
    return f"""
    Extrae la siguiente información del perfil de LinkedIn proporcionado y devuélvela en formato JSON sin comentarios ni texto adicional:
    
    [Información del perfil]
    
    Debe contener los siguientes campos:

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
    - Extrae una lista de las entidades más significativas con las que se relaciona la persona
    - Identifica la institución más relevante en su trabajo (puedes elegir organización dependiendo si consideras que alguna es muy importante v/s si ha trabajado mucho tiempo en alguna en especial)

    Si algún campo no está disponible, indícalo como un string vacío o una lista vacía según corresponda.

    Recuerda, **solo devuelve el JSON sin notas ni comentarios adicionales**.

    El texto del perfil es el siguiente:
    \n\n{text}
    """

def get_photo_analysis_prompt():
    return f"""
Eres un psicólogo experto en análisis de imágenes de LinkedIn. Se te proporcionará una descripción detallada de una foto de perfil de LinkedIn. Tu tarea es realizar un análisis psicológico **objetivo** de la persona en la foto, identificando tanto aspectos positivos como negativos. Presta atención a la expresión facial, lenguaje corporal, vestimenta, apariencia general y cualquier otro detalle relevante que puedas observar.

Por favor, proporciona un informe detallado que incluya:

1. **Análisis de la expresión facial**: Describe las emociones que la persona podría estar expresando y cómo estas pueden reflejar su estado emocional o personalidad.

2. **Análisis del lenguaje corporal**: Comenta sobre la postura, gestos y cualquier otro aspecto del lenguaje corporal que pueda indicar rasgos de personalidad o actitudes.

3. **Análisis de la vestimenta y apariencia**: Evalúa cómo la elección de ropa y aspecto general pueden influir en la percepción de la persona, incluyendo profesionalismo, atención al detalle, etc.

4. **Análisis del entorno o fondo**: Describe cómo el entorno de la foto contribuye a la impresión general de la persona.

5. **Conclusiones**: Proporciona una evaluación general que incluya tanto fortalezas como posibles áreas de mejora desde una perspectiva psicológica.

Recuerda ser objetivo y equilibrado en tu análisis, evitando sesgos y proporcionando observaciones basadas en la descripción de la imagen.

Aquí está la descripción de la foto:
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

def get_archetype_analysis_prompt(json_data, photo_analysis, archetypes, person_search_data, company_search_data, person_search_file, company_search_file):
    return f"""You will be analyzing a person's LinkedIn profile, profile photo, and web search results to determine their personality archetype and provide personalized negotiation recommendations. You will be provided with six inputs: LinkedIn profile data in JSON format, a description of the profile photo, a list of archetypes, web search results for the person, and web search results for their company.

First, here is the LinkedIn profile data in JSON format:
<linkedin_json>
{json.dumps(json_data, indent=2)}
</linkedin_json>

Next, here is the **profile photo description**:
<profile_photo_analysis>
{photo_analysis}
</profile_photo_analysis>

Here is the list of archetypes grouped into 10 categories:
<archetypes>
{archetypes}
</archetypes>

Here are the web search results for this person from the file {person_search_file}:
<person_web_search_results>
{person_search_data}
</person_web_search_results>

Here are the web search results for the person's company from the file {company_search_file}:
<company_web_search_results>
{company_search_data}
</company_web_search_results>

Tu tarea es realizar un análisis psicológico detallado, crítico y matizado de la persona, integrando la información de todas las fuentes proporcionadas. Deberás descubrir patrones únicos, aspectos ocultos y rasgos no evidentes, basando tus conclusiones estrictamente en la evidencia disponible. Evita generalizaciones, redundancias y suposiciones sin fundamento.

Por favor, genera los siguientes outputs en formato markdown bellamente formateado:

1. **Currículum vitae**: Resume la trayectoria profesional de la persona utilizando los datos proporcionados en `<linkedin_json>`. Enfócate en roles clave, logros, habilidades, educación y cualquier experiencia profesional notable. Asegura que el resumen sea completo y adaptado al perfil particular de la persona.

2. **Información en la web de la persona**: Proporciona un resumen completo y objetivo de la información encontrada sobre la persona en los resultados de búsqueda web (`<person_web_search_results>`). Extrae información clave, detalles relevantes y cualquier insight importante de los resultados de búsqueda. No te limites a listar los enlaces; en su lugar, sintetiza el contenido encontrado, destacando hallazgos significativos.

3. **Información en la web sobre la empresa**: Proporciona un resumen completo y objetivo de la información encontrada sobre la empresa en los resultados de búsqueda web (`<company_web_search_results>`). Extrae información clave, detalles relevantes y cualquier insight importante de los resultados de búsqueda. No te limites a listar los enlaces; en su lugar, sintetiza el contenido encontrado, enfocándote en aspectos que puedan influir en el contexto profesional de la persona.

4. **Análisis de la Foto de la Persona**: Proporciona un análisis psicológico objetivo de la foto de la persona, identificando tanto aspectos positivos como negativos. Incluye los siguientes puntos:

   - **Análisis de la expresión facial**
   - **Análisis del lenguaje corporal**
   - **Análisis de la vestimenta y apariencia**
   - **Análisis del entorno o fondo**
   - **Conclusiones**

5. **Perfil de la persona**: Desarrolla un perfil psicológico de la persona, actuando como un detective-psicólogo. Asume que las personas en LinkedIn presentan solo lo mejor de sí mismas; por lo tanto, analiza críticamente la información para identificar posibles contradicciones o aspectos ocultos que puedan inferirse de los datos. Utiliza el análisis de la foto y los resultados de búsqueda web para descubrir insights que pueden no ser inmediatamente aparentes. Proporciona un perfil matizado y basado en evidencia.

6. **Definición del arquetipo de la persona**: Sigue estos pasos:

   a. Revisa detenidamente los datos JSON de LinkedIn, el análisis de la foto y los resultados de búsqueda web, prestando atención a campos clave como resumen, experiencia, habilidades, educación, número de contactos, edad, instituciones relevantes y cualquier otra información pertinente.

   b. Identifica rasgos de personalidad, comportamientos, patrones y valores que se destaquen, enfocándote en evidencia específica de este individuo.

   c. Considera el perfil descrito arriba en el punto **5**.

   d. Revisa la lista de arquetipos y sus categorías. Considera cuáles arquetipos coinciden mejor con los rasgos, comportamientos y valores identificados.

   e. Selecciona los **3 arquetipos más relevantes** y su grupo que mejor describen la personalidad de la persona según la información que tienes disponible. Asegura que tu selección esté justificada por evidencia específica.

   f. Para cada arquetipo seleccionado, proporciona una explicación detallada y crítica de por qué se ajusta al perfil de la persona, citando evidencia específica de los datos de LinkedIn, el análisis de la foto y los resultados de búsqueda web.

   Presenta tu salida final en el siguiente formato:

     <analysis>
     <top_archetypes>
     1. **[Nombre del arquetipo]** (*[Categoría]*)
        - **Explicación**: [Tu explicación detallada y crítica aquí]

     2. **[Nombre del arquetipo]** (*[Categoría]*)
        - **Explicación**: [Tu explicación detallada y crítica aquí]

     3. **[Nombre del arquetipo]** (*[Categoría]*)
        - **Explicación**: [Tu explicación detallada y crítica aquí]
     </top_archetypes>

     <summary>
     [Proporciona un resumen crítico del perfil de personalidad de la persona basado en tu análisis, integrando ideas de los arquetipos principales y considerando tanto fortalezas como posibles áreas de mejora.]
     </summary>
     </analysis>

7. **Fortalezas**: Basado en toda la información proporcionada, describe detalladamente las fortalezas de la persona, apoyándote en evidencia específica. Enfócate en cualidades y capacidades que sean evidentes a partir de los datos.

8. **Debilidades**: Basado en toda la información proporcionada, describe detalladamente las debilidades o áreas de mejora de la persona. Sé objetivo y crítico, apoyándote en evidencia específica. Apunta a descubrir debilidades ocultas o no evidentes que estén respaldadas por los datos.

9. **Consideraciones clave al negociar con esta persona**: Proporciona una lista de **6 consideraciones clave al negociar con esta persona**, explicando paso a paso el razonamiento detrás de cada una. Asegúrate de que cada recomendación esté basada en detalles específicos de la personalidad y comportamiento de la persona, y explica cómo estos rasgos pueden influir en el proceso de negociación. Evita generalidades y enfócate en estrategias personalizadas.

**Recuerda** basar tu análisis únicamente en los datos proporcionados de LinkedIn, los resultados de búsqueda web, el análisis de la foto de perfil y la lista de arquetipos. Evita suposiciones infundadas y sé objetivo en tus evaluaciones.

**REGLAS:**

a. Actúa como un evaluador crítico y exigente.

b. Al desarrollar tus descripciones, infiere información que la persona podría intentar ocultar, pero apóyate siempre en la evidencia disponible.

c. Recuerda que las personas intentan mostrar lo mejor de sí mismas; tu tarea es descubrir la realidad, incluyendo posibles inconsistencias o áreas ocultas.

d. Evita la redundancia en tus explicaciones y sé específico.

e. Responde siempre en **español**.

f. Asegúrate de ver más allá de lo evidente; las personas presentan la mejor versión de sí mismas, y tú debes encontrar todo aquello de lo que no hablan.

g. Enfócate en descubrir los rasgos y características particulares de este individuo, basándote en evidencia específica.

h. Evita la redundancia en tus explicaciones; sé preciso y basa tus análisis en la evidencia disponible.

i. **Especificidad sobre generalidad**: Basa tus conclusiones y recomendaciones en detalles específicos de los datos proporcionados, evitando declaraciones vagas o generales.
"""
