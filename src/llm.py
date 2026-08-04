from langchain_core.language_models.chat_models import BaseChatModel
from src.config import config

def get_llm()->BaseChatModel:
    """
    Patrón Factory: construye y retorna la instancia del modelo de lenguaje
    según el proveedor definido en la configuración.
    
    Retorna un objeto que implementa 'BaseChatModel', lo que garantiza
    que responderá a los mismos métodos (.invoke(), .stream(), etc.)
    sin importar qué proveedor esté por debajo.
    """
    provider = config.LLM_PROVIDER
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        config.validate()
        return ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            api_key=config.OPENAI_API_KEY
        )
    elif provider == "groq":
        from langchain_groq import ChatGroq
        config.validate()
        return ChatGroq(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            api_key=config.GROQ_API_KEY
        )
    else:
        raise ValueError(
            f"❌ Proveedor de LLM no soportado: '{provider}'. "
            "Usa 'openai' o 'groq' en tu archivo .env"
        )