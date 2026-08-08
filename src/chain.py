from typing import Dict, Any, List
from langchain_core.documents import Document
from src.llm import get_llm
from src.prompts import CITIZEN_CHAT_PROMPT
from src.database import get_session_history, get_user_profile, update_user_profile
from src.extractor import extract_user_profile
from src.rag import get_retriever

def format_docs(docs: List[Document]) -> str:
    """
    Transforma la lista de objetos Document devueltos por FAISS 
    en un bloque de texto legible en Markdown con sus fuentes.
    """
    if not docs:
        return "No se encontró documentación oficial específica relevante para esta consulta."
    
    formatted = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Documento Oficial")
        formatted.append(f"[Fuente {i}: {source}]\n{doc.page_content.strip()}")
    
    return "\n\n".join(formatted)

def format_profile_for_prompt(profile_dict: Dict[str, Any]) -> str:
    """
    Transforma el diccionario del perfil de MongoDB en un formato 
    de texto legible (Markdown) para el System Prompt.
    """
    if not profile_dict:
        return "Aún no se han registrado datos personales de este ciudadano."
    
    formatted_lines = []
    for key, value in profile_dict.items():
        if value is not None:
            formatted_lines.append(f"- {key.capitalize()}: {value}")
    
    return "\n".join(formatted_lines) if formatted_lines else "Aún no se han registrado datos personales de este ciudadano."

def process_citizen_interaction(session_id: str, user_input: str) -> str:
    """
    Orquestador principal con integración completa (RAG + Perfil + Historial):
    1. Extracción de entidades (Fase 2) -> MongoDB (users)
    2. Búsqueda Vectorial RAG (Fase 3) -> FAISS Retriever
    3. Carga de Perfil e Historial de MongoDB
    4. Invocación de la cadena LCEL con todas las variables
    5. Persistencia del mensaje en el historial -> MongoDB (conversations)
    """
    # 1. Extracción de entidades y actualización de perfil en MongoDB
    try:
        extracted_profile = extract_user_profile(user_input)
        update_user_profile(user_id=session_id, profile_data=extracted_profile)
    except Exception as e:
        print(f"⚠️ [Warning] No se pudo extraer perfil del mensaje: {e}")

    # 2. Búsqueda semántica de fragmentos oficiales en FAISS (RAG)
    try:
        retriever = get_retriever(k=3)
        retrieved_docs = retriever.invoke(user_input)
        formatted_context_str = format_docs(retrieved_docs)
    except Exception as e:
        print(f"⚠️ [Warning] Error al recuperar documentos de FAISS: {e}")
        formatted_context_str = "No fue posible consultar la base vectorial de documentos oficiales."

    # 3. Cargar perfil actualizado desde la colección 'users' de MongoDB
    current_profile_dict = get_user_profile(user_id=session_id)
    formatted_profile_str = format_profile_for_prompt(current_profile_dict)

    # 4. Cargar el historial de mensajes directamente desde MongoDB
    history = get_session_history(session_id=session_id)

    # 5. Inicializar el LLM y construir la cadena LCEL
    llm = get_llm()
    chain = CITIZEN_CHAT_PROMPT | llm

    # 6. Invocación pasando TODAS las variables declaradas en el System Prompt
    response = chain.invoke({
        "input": user_input,
        "context": formatted_context_str,      # Inyección por RAG (FAISS)
        "user_profile": formatted_profile_str,  # Inyección por Perfilamiento (MongoDB)
        "history": history.messages             # Inyección por Historial (MongoDB)
    })

    # 7. Guardar la nueva interacción en MongoDB
    history.add_user_message(user_input)
    history.add_ai_message(response.content)

    return response.content