import os
from sqlalchemy import create_engine, inspect, text
from smolagents import CodeAgent, HfApiModel, tool
from .validator import is_safe_sql

DB_NAME = "safe_sql_demo.db"

# Usamos SQLAlchemy para conectarnos a la base local
engine = create_engine(f"sqlite:///{DB_NAME}")

def get_schema_description():
    try:
        inspector = inspect(engine)
        desc = "Esquema de la base de datos:\n"
        for table_name in inspector.get_table_names():
            desc += f"\nTabla '{table_name}':\nColumns:\n"
            for col in inspector.get_columns(table_name):
                desc += f"  - {col['name']}: {col['type']}\n"
        return desc
    except Exception as e:
        return "No se pudo obtener el esquema."

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
    if not is_safe_sql(query):
        return "ERROR DE SEGURIDAD: Consulta bloqueada por el validador (SQL Guard). Solo se permite SELECT."
    
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

# Inyectar el esquema en la herramienta
sql_engine.description += f"\n\n{get_schema_description()}"

def run_agent(question: str) -> str:
    # Usamos un modelo ligero ideal para código
    agent = CodeAgent(
        tools=[sql_engine],
        model=HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct"),
        additional_authorized_imports=["sqlalchemy"]
    )
    try:
        # Aquí capturamos la salida final del agente
        respuesta = agent.run(question)
        return str(respuesta)
    except Exception as e:
        return f"Error en el agente: {e}"
