# Guía Ciudadana CLI

Asistente interactivo por consola para la orientación de trámites locales, derechos ciudadanos y becas, impulsado por LangChain, MongoDB y LLMs.

## Características

- **Atención contextual:** Recuerda la información del usuario entre sesiones gracias al historial persistido en MongoDB.
- **Orientación clara:** Simplifica el lenguaje burocrático a pasos accionables con respuestas estructuradas.
- **Transparencia:** Diseñado para brindar respuestas precisas y estructuradas, sin inventar requisitos ni fechas.
- **Múltiples proveedores:** Soporta **Groq** y **OpenAI**, seleccionables mediante configuración.
- **Perfilamiento progresivo:** Pide los datos del usuario (edad, ocupación, ciudad) de a uno por vez cuando hacen falta para validar un trámite.

## Stack Tecnológico

| Tecnología | Uso |
| --- | --- |
| [LangChain](https://www.langchain.com/) | Orquestación de la cadena de IA (LCEL) y gestión de memoria |
| MongoDB | Persistencia del historial de conversaciones por sesión |
| Groq / OpenAI / Ollama | Proveedores de modelos de lenguaje |
| Python 3 | Lenguaje de implementación |

## Estructura del Proyecto

```
chatbot-project/
├── main.py            # Punto de entrada de la aplicación
├── requirements.txt   # Dependencias del proyecto
├── .env.example       # Plantilla de variables de entorno
└── src/
    ├── cli.py         # Interfaz de consola (bucle de conversación)
    ├── chain.py       # Ensambla la cadena de IA con memoria
    ├── llm.py         # Factory del proveedor de LLM (Groq/OpenAI)
    ├── config.py      # Configuración centralizada desde variables de entorno
    ├── database.py    # Factory del historial de sesión en MongoDB
    └── prompts.py     # Prompt de sistema de GuíaCiudadana
```

## Requisitos

- Python 3.10+
- MongoDB local o remoto (URI de conexión)
- Clave de API del proveedor seleccionado (Groq u OpenAI)

## Instalación

1. Clona el repositorio y crea un entorno virtual:

   ```bash
   git clone <url-del-repositorio>
   cd chatbot-project
   python -m venv .venv
   ```

2. Activa el entorno virtual:

   - **Windows:** `.venv\Scripts\activate`
   - **Linux/macOS:** `source .venv/bin/activate`

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:

   ```bash
   cp .env.example .env
   ```

   Edita el archivo `.env` con tus credenciales.

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `LLM_PROVIDER` | Proveedor de IA: `groq` u `openai` | `groq` |
| `GROQ_API_KEY` | Clave de API de Groq (requerida si `LLM_PROVIDER=groq`) | — |
| `OPENAI_API_KEY` | Clave de API de OpenAI (requerida si `LLM_PROVIDER=openai`) | — |
| `MODEL_NAME` | Nombre del modelo a utilizar | — |
| `TEMPERATURE` | Temperatura de generación del modelo | `0.2` |
| `MONGODB_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017/` |
| `DB_NAME` | Nombre de la base de datos | `guia_ciudadana_db` |
| `COLLECTION_NAME` | Colección donde se guardan las conversaciones | `conversations` |

## Uso

```bash
python main.py
```

Al iniciar:

1. Ingresa tu **ID de usuario o DNI** para recuperar tu historial (si no ingresas nada, se usa la sesión `ciudadano_anonimo`).
2. Escribe tu consulta sobre trámites, becas o derechos.
3. Para finalizar, escribe `salir`, `exit`, `quit` o `chau`.

La conversación queda guardada automáticamente en MongoDB, por lo que puedes retomarla en cualquier momento con tu mismo ID de sesión.

## Arquitectura de la Cadena

1. `src/llm.py` obtiene la instancia del LLM según el proveedor configurado (patrón Factory).
2. `src/prompts.py` define el prompt de sistema de GuíaCiudadana.
3. `src/chain.py` une el prompt con el LLM usando la sintaxis de tubería de LCEL y lo envuelve en `RunnableWithMessageHistory`.
4. `src/database.py` inyecta y guarda automáticamente el historial de la conversación en MongoDB.
