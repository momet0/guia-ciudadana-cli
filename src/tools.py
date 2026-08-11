from langchain_core.tools import tool
import os

@tool
def calcular_monto_estimado_beca(edad:int , es_estudiante:bool,
                                  es_carrera_prioritaria:bool, ingresos_familiares:float) -> str:
    """
    A partir de los argumentos se verifica y calcula cuanto sera el monto adecuado que le corresponde al ciudadano.
    """
    if not es_estudiante:
        return "la beca solo le corresponde a ciudadanos que son estudiantes"
    elif ingresos_familiares > 800000:
        return "los ingresos familiares superan los requisitos de la beca por lo tanto no le corresponde la beca"

    if es_carrera_prioritaria:
        return "como su carrera es proritara le corresponde un aumento a su beca de un monto de $50000"
    else:
        return "el monto de su beca es de $35000"

@tool
def exportar_resumen_ciudadano(session_id: str, resumen_text: str) -> str:
    """
    crea un txt donde se guarda una constancia de cada consulta del ciudadano, en el directorio data/reports 
    """
    ruta = 'data/reports'

    if not os.path.exists(ruta):
        os.makedirs(ruta,exist_ok=True)

    file_path = os.path.join(ruta, f"constancia_{session_id}.txt")
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(resumen_text)

    return f"el archivo fue creado y se guardo con exito en la ruta: {file_path}"