from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from src.llm import get_llm
from src.prompts import CITIZEN_CHAT_PROMPT
from src.database import get_session_history, get_user_profile, update_user_profile
from src.extractor import extract_user_profile
from typing import Dict, Any


def format_profile_for_prompt(profile_dict: Dict[str, Any]) -> str:
    """
    Toma el diccionario nativo recuperado de MongoDB y lo transforma 
    en un bloque de texto legible para el System Prompt.
    """
    if not profile_dict:
        return "no se registraron todavia datos del ciudadano"

    formatted_lines = []
    for key, value in profile_dict.items():
        if value is not None:
            formatted_lines.append(f"- {key.capitalize()}: {value}")

    return "\n".join(formatted_lines) if formatted_lines else "todavia no se registran datos del ciudadano"

def process_citizen_interaction(session_id: str, user_input: str) -> str:
    """
    Orquestador principal del flujo conversacional con perfilamiento:
    1. Ejecuta la extracción de entidades en segundo plano y actualiza MongoDB.
    2. Recupera el perfil consolidado de MongoDB.
    3. Construye la cadena conversacional pasándole el perfil formateado.
    4. Invoca la respuesta del LLM y persiste la conversación en el historial.
    """

    try:
        extracted_profile = extract_user_profile(user_input)
        update_user_profile(user_id=session_id, profile_data=extracted_profile)
    except Exception as e:
        print(f"ERROR No se pudo extraer perfil del mensaje: {e}")

    current_profile_dict = get_user_profile(user_id=session_id)
    formatted_profile_str = format_profile_for_prompt(current_profile_dict)

    history = get_session_history(session_id=session_id)
    
    llm = get_llm()
    base_chain = CITIZEN_CHAT_PROMPT | llm

    response = base_chain.invoke(
        {
            "input": user_input,
            "user_profile": formatted_profile_str,
            "history": history.messages 
        },
        config={"configurable":{"session_id": session_id}}
    )

    history.add_user_message(user_input)
    history.add_ai_message(response.content)

    return response.content

