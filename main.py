import os
import sys
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

# Importación del proveedor de LLM (OpenAI por defecto)
from langchain_openai import ChatOpenAI

# Cargar variables de entorno
load_dotenv()

# Validar que tengamos las credenciales necesarias
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: Por favor, configura tu OPENAI_API_KEY en el archivo .env")
    sys.exit(1)

# 1. Configuración del Modelo de Lenguaje (LLM)
# Usamos gpt-4o-mini por ser rápido y muy económico.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# 💡 Alternativa Gratuita con Groq:
# from langchain_groq import ChatGroq
# llm = ChatGroq(model="llama-3.3-70b-versatile")

# 💡 Alternativa 100% Local y Gratuita con Ollama:
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3")


# 2. Definición del Prompt (Plantilla de conversación)
# Usamos MessagesPlaceholder para indicarle a LangChain dónde inyectar el historial de chat.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente de IA empático, amigable, ingenioso y muy capaz."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Creamos la cadena básica asociando el prompt con el LLM
chain = prompt | llm


# 3. Función para recuperar/crear el historial en MongoDB
# Esta función es requerida por RunnableWithMessageHistory
def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
    return MongoDBChatMessageHistory(
        connection_string=os.getenv("MONGODB_URI", "mongodb://localhost:27017/"),
        database_name="chat_db",
        collection_name="conversations",
        session_id=session_id
    )


# 4. Envolver la cadena con manejo automático de memoria
wrapped_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


# 5. El bucle de consola interactivo (CLI)
def main():
    print("=========================================")
    print("🤖 ¡Bienvenido al Chatbot con Memoria MongoDB!")
    print("=========================================\n")
    
    # Solicitamos un ID de sesión (puede ser el nombre del usuario o cualquier ID)
    session_id = input("👤 Ingresa tu ID de usuario o sesión para comenzar: ").strip()
    if not session_id:
        session_id = "default_user"
    
    print(f"\nConectado con la sesión: '{session_id}'")
    print("Escribe 'salir' o 'exit' para terminar la conversación.\n")
    
    while True:
        try:
            user_input = input("✨ Tú: ").strip()
            
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\n👋 ¡Hasta luego! Tu historial ha quedado guardado en MongoDB.")
                break
                
            if not user_input:
                continue
                
            # Ejecutamos la cadena pasando el input y la configuración del session_id
            response = wrapped_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )
            
            # Mostramos la respuesta del asistente
            print(f"🤖 Asistente: {response.content}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Chat finalizado de forma abrupta.")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}\n")

if __name__ == "__main__":
    main()