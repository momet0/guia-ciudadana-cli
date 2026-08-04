from langchain_core.runnables.history import RunnableWithMessageHistory
from src.llm import get_llm
from src.prompts import CITIZEN_CHAT_PROMPT
from src.database import get_session_history

def get_citizen_chain():
    """
    Ensambla la cadena completa de Inteligencia Artificial:
    1. Obtiene la instancia del LLM desde el Factory (src/llm.py).
    2. Une el Prompt con el LLM usando la sintaxis de tubería '|' (LCEL).
    3. Envuelve la cadena con RunnableWithMessageHistory para inyectar 
       y guardar automáticamente el historial en MongoDB.
    """
    #inicializar el proveedor de ia elegido
    llm = get_llm()

    #crear la cadena base
    base_chain = CITIZEN_CHAT_PROMPT | llm

    #envolver la cadena con gestion automatica de memoria
    conversation_chain = RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    return conversation_chain
