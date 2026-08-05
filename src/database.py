from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.config import config
from pymongo import MongoClient
from typing import Dict, Any, Optional
from src.schemas import UserProfile

#cliente unico reutilizable para operaciones directas en pymongo
_mongo_client: Optional[MongoClient] = None

def get_mongo_client() -> MongoClient:
    """Retorna una instancia Singleton del cliente nativo de PyMongo."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(config.MONGODB_URI)
    return _mongo_client


def get_session_history(session_id : str) -> MongoDBChatMessageHistory:
    """
    Función fábrica (Session Factory) para LangChain.
    
    Recibe un 'session_id' (ej: ID del ciudadano o número de sesión) y 
    retorna un objeto de historial de mensajes que lee y escribe directamente 
    en la colección configurada de MongoDB.
    """
    return MongoDBChatMessageHistory(
        connection_string=config.MONGODB_URI,
        database_name=config.DB_NAME,
        collection_name=config.COLLECTION_NAME,
        session_id=session_id
    )

def get_user_profile(user_id:str) -> Dict[str, Any]:
    """
    Recupera el documento del perfil de usuario desde la colección 'users'.
    Retorna un diccionario vacío {} si el usuario no existe.
    """
    client = get_mongo_client()
    db = client[config.DB_NAME]
    collection = db["users"]

    #buscar documento por la clave_id
    user_doc = collection.find_one({"_id":user_id})
    if user_doc:
        user_doc.pop("_id", None)
        return user_doc
    return {}

def update_user_profile(user_id: str, profile_data: UserProfile) -> None:
    """
    Actualiza el perfil del usuario en MongoDB aplicando un 'merge' parcial.
    Solo sobrescribe los campos que no sean None en 'profile_data'.
    """

    #convertir pydantic a diccionario filtrando valores None
    update_data = profile_data.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        return #no datos nuevos a actualizar

    client = get_mongo_client()
    db = client[config.DB_NAME]
    collection = db["users"]

    #ejecutar actualizacion atomica en MongoDB
    collection.update_one(
        {"_id": user_id},
        {"$set": update_data},
        upsert=True
    )