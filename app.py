import os
from sqlalchemy import create_engine, inspect, text
from smolagents import CodeAgent, HfApiModel, tool
from validator import is_safe_sql
import db
from dotenv import load_dotenv

# Cargar variables de entorno (como HF_TOKEN)
load_dotenv()

# Inicializa la DB si no existe
if not os.path.exists(db.DB_NAME):
    db.setup_db()

# Usamos SQLAlchemy para conectarnos a la base local
engine = create_engine(f"sqlite:///{db.DB_NAME}")

# Generar la descripción del esquema dinámicamente
inspector = inspect(engine)
table_description = "Esquema de la base de datos:\n"
for table_name in inspector.get_table_names():
    table_description += f"\nTabla '{table_name}':\nColumns:\n"
    for col in inspector.get_columns(table_name):
        table_description += f"  - {col['name']}: {col['type']}\n"

@tool
def sql_engine(query: str) -> str:
    """
    Permite realizar consultas SQL sobre la base de datos de ventas.
    Devuelve una representación en texto del resultado.
    
    Asegúrate de generar SQL válido (ej. SQLite).
    ATENCIÓN: Solo se permiten consultas SELECT (solo lectura).
    
    Args:
        query: La consulta SQL a ejecutar.
    """
    print(f"\n[Ejecutando SQL]: {query}")
    
    if not is_safe_sql(query):
        error_msg = "ERROR DE SEGURIDAD: Consulta bloqueada por el validador (SQL Guard). Solo se permite SELECT."
        print(f"[SQL Guard]: {error_msg}")
        return error_msg
    
    output = ""
    try:
        with engine.connect() as con:
            rows = con.execute(text(query))
            for row in rows:
                output += "\n" + str(row)
        if not output:
            return "La consulta se ejecutó con éxito pero no devolvió resultados."
        return output
    except Exception as e:
        return f"Error ejecutando SQL: {e}"

# Inyectamos el esquema en la descripción de la herramienta para que el agente lo vea
sql_engine.description += f"\n\n{table_description}"

def main():
    print("--- Asistente SQL Seguro con smolagents ---")
    
    # Verificación del token
    if not os.getenv("HF_TOKEN"):
        print("ADVERTENCIA: No se encontró HF_TOKEN en el entorno. Si el modelo falla, crea un archivo .env con tu token de Hugging Face.")
    
    print("Inicializando agente de IA...")
    
    # Configuración del CodeAgent
    # Utilizamos Qwen u otro modelo eficiente para razonamiento en código
    agent = CodeAgent(
        tools=[sql_engine],
        model=HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct"), 
        additional_authorized_imports=["sqlalchemy"]
    )
    
    # Pregunta de prueba que requiere un JOIN
    pregunta = "¿Cuál es el cliente (name) que realizó la compra con el monto más alto (total_amount)?"
    
    print(f"\nPregunta del usuario: {pregunta}\n")
    print("El agente está pensando...")
    
    # El agente procesará la pregunta, escribirá Python, llamará a sql_engine y analizará el resultado
    respuesta = agent.run(pregunta)
    
    print("\n[Respuesta Final del Agente]")
    print(respuesta)

if __name__ == "__main__":
    main()
