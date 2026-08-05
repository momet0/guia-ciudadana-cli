from langchain_core.prompts import ChatPromptTemplate
from src.llm import get_llm
from src.schemas import UserProfile

EXTRACTION_PROMPT = ChatPromptTemplate([
    ("system", """
    Eres un extractor de datos especializado. Tu objetivo es analizar el mensaje de un usuario
    y extraer datos personales si los menciona explícitamente.
    
    REGLAS:
    1. Extrae SOLAMENTE información expresada de forma clara por el usuario.
    2. Si el usuario no menciona ningún dato personal relevante para el esquema, retorna los campos como None.
    3. NO asumas ni inventes ningún dato.
    """),
    ("human", "{input}")
])

def extract_user_profile(user_input: str) -> UserProfile:
    """
    Toma el texto de entrada del usuario y utiliza la capacidad 'Structured Output'
    del LLM para retornar una instancia validada de UserProfile.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(UserProfile)

    extraction_chain = EXTRACTION_PROMPT | structured_llm

    result: UserProfile = extraction_chain.invoke({"input": user_input})
    return result