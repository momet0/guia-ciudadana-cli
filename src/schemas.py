from typing import Optional
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    """
    Esquema de datos Pydantic para el perfil del ciudadano.
    Define los atributos que el LLM debe intentar extraer de las conversaciones.
    """
    nombre: Optional[str] = Field(
        default=None,
        description="el nombre o como prefiere ser llamada el ciudadano"
    )
    edad: Optional[int] = Field(
        default=None,
        description="la edad del ciudadano en años"
    )
    estudia: Optional[bool] = Field(
        default=None,
        description="True si el ciudadano actualmente cursa estudios, False si indica que no estudia"
    )
    trabaja: Optional[bool] = Field(
        default=None,
        description="True si el ciudadano actualmente trabaja, False si indica que no trabaja"
    )
    ubicacion: Optional[str] = Field(
        default=None,
        description="ciudad, barrio o provincia donde reside el ciudadano"
    )


class GuideInfo(BaseModel):
    """
    Esquema de datos Pydantic para la informacion de identidad del negocio.
    """
    name: str = Field(
        default="guia ciudadana",
        description="el nombre o como prefiere ser llamada el negocio"
    )
    organization: str = Field(
        default="Organismo publico",
        description="la organizacion que representa el negocio"
    )
    domain: str = Field(
        default="tramites y servicios ciudadanos",
        description="el dominio de la organizacion"
    )
    language: str = Field(
        default="es",
        description="el idioma de la conversacion"
    )
    tone: str = Field(
        default="amable,calido,cordial y servicial",
        description="el tono de la forma de contestar del chatbot"
    )
    

class KnowledgeConfig(BaseModel):
    """
    Esquema de datos Pydantic para la configuracion del conocimiento
    """
    sources_dir: str = Field(
        default="data/docs",
        description="la ruta del directorio que contiene los documentos"
    )
    allowed_extensions: list[str]= Field(
        default=[".pdf",".txt",".md"],
        description="la lista de extensiones de archivo permitidas"
    )
    chunk_size: int = Field(
        default=600,
        gt=0,
        description="el tamaño de fragmentos en caracteres"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        description="el solapamiento entre los trozos"
    )
    top_k: int = Field(
        default=3,
        gt=0,
        description="el numero de trozos a recuperar"
    )
    
class StorageConfig(BaseModel):
    """
    Esquema de datos Pydantic para la configuracion del almacenamiento
    """
    type: str = Field(
        default="mongodb",
        description="que base de datos see usara para guardar y recuperar la informacion de los documentos"
    )
    database_url: str = Field(
        default="mongodb://localhost:27017",
        description="la url de la base de datos"
    )

class AppConfig(BaseModel):
    """
    Esquema de datos Pydantic para la configuracion de la aplicacion
    """
    guide: GuideInfo = Field(
        default=GuideInfo(),
        description="la informacion de identidad del negocio"
    )
    knowledge: KnowledgeConfig= Field(
        default=KnowledgeConfig(),
        description="la configuracion del conocimiento"
    )
    storage: StorageConfig = Field(
        default=StorageConfig(),
        description="la configuracion del almacenamiento"
    )
