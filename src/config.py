import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    """
    Clase de configuracion centralizada e inmutable
    lee las variables de entorno y proporciona valores por defecto seguros
    """
    #PROVEEDOR DE LLM SELECCIONADO
    LLM_PROVIDER:str = os.getenv("LLM_PROVIDER","groq").lower()

    #CREDENCIALES DE APIS
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY","")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY","")

    #CONFIGURACION DEL MODELO
    MODEL_NAME: str = os.getenv("MODEL_NAME","")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE","0.2"))

    #CONFIGURACION DE MONGODB
    MONGODB_URI: str = os.getenv("MONGODB_URI","mongodb://localhost:27017/")
    DB_NAME: str = os.getenv("DB_NAME","guia_ciudadana_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME","conversations")

    def validate(self) -> None:
        """
        Aplica el patrón 'Fail-Fast': valida que las llaves necesarias existan
        antes de que el programa intente ejecutar llamadas a la API.
        """
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("Error : falta 'OPENAI_API_KEY' en el archivo .env")
        elif self.LLM_PROVIDER == "groq" and not self.GROQ_API_KEY:
            raise ValueError("Error : falta 'GROQ_API_KEY' en el archivo .env")

config = Config()
