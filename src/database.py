from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from src.config import config

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