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
