import sys
from src.chain import get_citizen_chain

def run_cli():
    print("\n==================================================")
    print("🏛️  BIENVENIDO A GUÍA CIUDADANA - ASISTENTE VIRTUAL")
    print("==================================================")
    print("Orientación en trámites, becas y derechos locales.")
    print("--------------------------------------------------\n")

    #solicitar el id de sesion para recuperar el historial de mongoDB
    session_id = input("👤 Ingresa tu ID de usuario o DNI para la sesión: ").strip()
    if not session_id:
        session_id = "ciudadano_anonimo"
        print("ℹ️  No ingresaste un ID. Usando sesión por defecto: 'ciudadano_anonimo'")

    print(f"\n✅ Sesión activa: [{session_id}]")
    print("💡 Escribe 'salir', 'exit' o 'chao' para finalizar la conversación.\n")

    #inicializar la cadena de ia
    try:
        chain = get_citizen_chain()
    except Exception as e:
        print(f"❌ Error al inicializar la aplicación: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input(f"👤 [{session_id}]: ").strip()

            #comandos de salida
            if user_input.lower() in ["salir","exit","quit","chau"]:
                print("\n👋 ¡Hasta pronto! Tu historial ha quedado guardado en MongoDB.\n")
                break

            #ignorar enter/lineas vacias
            if not user_input:
                continue
            
            print("🤖 GuíaCiudadana pensando...", end="\r")

            #invocar cadena pasando la entrada y session_id
            response = chain.invoke(
                {"input":user_input},
                config={"configurable":{"session_id":session_id}}
            )

            #limpiar el indicador de pensando y mostrar respuesta
            print(" " * 40, end="\r")
            print(f"🤖 GuíaCiudadana:\n{response.content}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n\n👋 Sesión interrumpida por el usuario. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}\n")