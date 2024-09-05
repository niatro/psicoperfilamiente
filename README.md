# AInstein LinkedIn Analyzer y Generador de Emails

AInstein LinkedIn Analyzer es una herramienta potente que automatiza el proceso de extracción, análisis y generación de emails personalizados a partir de perfiles de LinkedIn. Este proyecto aprovecha los últimos avances en web scraping, procesamiento de lenguaje natural e inteligencia artificial para proporcionar una solución integral para empresas que buscan mejorar sus esfuerzos de alcance en LinkedIn.

```mermaid
graph TD
subgraph Input["Input"]
A[("📊 Perfil LinkedIn")]
P[("⚙️ Usuario y Contraseña")]
end

subgraph Screenshot["Screenshot"]
C["📸 Capturador Web"]
F[("📁 Screnshot linkedin")]
G[("📁 Screnshot sección 1")]
end

subgraph Curriculum["Currículum"]
E["🧠 Analizador de Perfiles"]
I[("📁 Análisis perfil")]
end

subgraph Rostro["Rostro"]
D["🖼️ Extractor de Imágenes"]
H[("📁 Análisis foto")]
end

subgraph Psicoperfilamiento["Psicoperfilamiento"]
J["🧠 Generador de Perfiles IA"]
K{"🤖 Elección de IA"}
L["🤖 GPT-4"]
M["🤖 Claude"]
N["📄 Generador de Perfiles"]
O[("📁 Perfil Completo")]
end

subgraph Email["Email"]
T["✉️ Generador de Emails IA"]
U{"🤖 Elección de IA"}
V["🤖 GPT-4"]
W["🤖 Claude"]
X[("📁 mails")]
end

Q["🌐 Búsqueda en web"]
R["📝 Archetypes"]
S["📝 Prompts de Email"]

A -->|URLs de LinkedIn| C
P -.->|Configuración| C
C -->|Capturas completas| F
C -->|Capturas parciales| G
F -->|Análisis de captura| E
G -->|Extracción de secciones| D
E -->|Datos estructurados| I
D -->|Fotos procesadas| H
I -->|Análisis de perfil| J
H -->|Análisis de foto| J
J -->|Selección de modelo| K
K -->|OpenAI| L --> N
K -->|Anthropic| M --> N
N -->|Emails y perfiles| O
O -->|Perfiles completos| T
T -->|Selección de modelo| U
U -->|OpenAI| V --> X
U -->|Anthropic| W --> X
Q -.->|Análisis Web| J
R -.->|Prompts| J
S -.->|Prompts| T

%% Definición de estilos
classDef inputFile fill:#FF5733,stroke:#333,stroke-width:2px,color:white
classDef mainScript fill:#3498DB,stroke:#333,stroke-width:2px,color:white
classDef jsScript fill:#F1C40F,stroke:#333,stroke-width:2px,color:black
classDef pythonScript fill:#2ECC71,stroke:#333,stroke-width:2px,color:white
classDef outputFolder fill:#E67E22,stroke:#333,stroke-width:2px,color:white
classDef aiScript fill:#9B59B6,stroke:#333,stroke-width:2px,color:white
classDef decision fill:#FF69B4,stroke:#333,stroke-width:2px,color:black
classDef aiModel fill:#27AE60,stroke:#333,stroke-width:2px,color:white
classDef outputScript fill:#16A085,stroke:#333,stroke-width:2px,color:white
classDef configFile fill:#8E44AD,stroke:#333,stroke-width:2px,color:white
classDef promptFile fill:#2980B9,stroke:#333,stroke-width:2px,color:white
classDef webSearch fill:#4CAF50,stroke:#333,stroke-width:2px,color:white

%% Asignación de clases a nodos
class A,P inputFile
class C jsScript
class D,E pythonScript
class F,G,H,I,O,X outputFolder
class J,T aiScript
class K,U decision
class L,M,V,W aiModel
class N outputScript
class Q webSearch
class R,S promptFile

%% Estilos de subgrafos con colores más oscuros
style Input fill:#8B4513,stroke:#FF9800,stroke-width:2px,color:white
style Screenshot fill:#1A237E,stroke:#2196F3,stroke-width:2px,color:white
style Curriculum fill:#1B5E20,stroke:#4CAF50,stroke-width:2px,color:white
style Rostro fill:#880E4F,stroke:#E91E63,stroke-width:2px,color:white
style Psicoperfilamiento fill:#311B92,stroke:#673AB7,stroke-width:2px,color:white
style Email fill:#B71C1C,stroke:#F44336,stroke-width:2px,color:white

%% Estilo de las flechas
linkStyle default stroke:#FFFFFF,stroke-width:2px,fill:none
```

## Características

- **Scraping de Perfiles de LinkedIn**: Extrae automáticamente datos de perfiles de LinkedIn, incluyendo texto, imágenes y otra información relevante.
- **Análisis de Perfiles**: Analiza los datos extraídos del perfil para generar insights detallados sobre cada individuo.
- **Generación de Emails con IA**: Utiliza modelos de lenguaje avanzados (OpenAI y Anthropic) para generar emails personalizados y persuasivos basados en el análisis del perfil.
- **Flujo de Trabajo Automatizado**: Optimiza todo el proceso, desde la extracción del perfil hasta la generación del email, para ahorrar tiempo y mejorar la eficiencia.

## Arquitectura del Sistema

AInstein LinkedIn Analyzer se compone de los siguientes componentes principales:

1. **LinkedIn Scraper**: Responsable de extraer datos de perfiles de LinkedIn, incluyendo la captura de screenshots y extracción de texto.
2. **Extractor de Imágenes de Perfil**: Procesa las imágenes de perfil extraídas y las prepara para un análisis posterior.
3. **Analizador de Perfiles**: Analiza los datos extraídos del perfil y genera información estructurada sobre cada individuo.
4. **Generador de Perfiles con IA**: Aprovecha los datos del perfil y las imágenes para generar un análisis detallado utilizando modelos de IA.
5. **Generador de Emails con IA**: Genera emails personalizados basados en el análisis del perfil impulsado por IA.

## Comenzando

Para comenzar con AInstein LinkedIn Analyzer, sigue estos pasos:

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/ainstein-linkedin-analyzer.git
   ```
2. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno en un archivo `.env`:
   ```
   OPENAI_API_KEY=tu_clave_api_de_openai
   ANTHROPIC_API_KEY=tu_clave_api_de_anthropic
   ```
4. Prepara tus datos de entrada (URLs de perfiles de LinkedIn) en un archivo Excel llamado `prueba_url.xlsx`.
5. Ejecuta el script principal:
   ```
   python linkedin_scraper.py
   ```
6. Procesa los perfiles extraídos:
   ```
   python linkedin_profile_analyzer.py
   ```
7. Genera perfiles completos con IA:
   ```
   python ai_profile_generator.py
   ```
8. Genera emails personalizados:
   ```
   python mails.py
   ```
9. Los emails generados se guardarán en la carpeta `mails`.

## Configuración

La configuración del proyecto se gestiona a través de los siguientes archivos:

- `config.py`: Define las rutas, tiempos de espera y otras configuraciones.
- `models.py`: Especifica los modelos de IA disponibles para el análisis de perfiles y la generación de emails.
- `prompt_profile.py`: Establece los prompts utilizados para el análisis de perfiles.
- `prompt_email.py`: Define los prompts utilizados para la generación de emails.

## Estructura del Proyecto

```
ainstein-linkedin-analyzer/
│
├── linkedin_scraper.py
├── linkedin_profile_analyzer.py
├── linkedin_profile_image_extractor.py
├── ai_profile_generator.py
├── mails.py
├── config.py
├── models.py
├── prompt_profile.py
├── prompt_email.py
├── requirements.txt
├── README.md
│
├── capturas_linkedin/
├── captura_1/
├── profile_photos/
├── json_profiles/
├── perfiles_completos/
└── mails/
```

## Contribuciones

Agradecemos las contribuciones al proyecto AInstein LinkedIn Analyzer. Si encuentras algún problema o tienes sugerencias para mejoras, no dudes en enviar un pull request o abrir un issue en el repositorio de GitHub.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Advertencia

El uso de este software para scraping y análisis de perfiles de LinkedIn debe cumplir con los términos de servicio de LinkedIn y las leyes de privacidad aplicables. Asegúrate de tener los permisos necesarios antes de utilizar esta herramienta.
