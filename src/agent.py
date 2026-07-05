import os
import time
from sqlalchemy import create_engine, inspect, text
from smolagents import CodeAgent, InferenceClientModel, LiteLLMModel, tool
from .validator import is_safe_sql

DB_NAME = "safe_sql_demo.db"
engine = create_engine(f"sqlite:///{DB_NAME}")

# Estado global para interceptar la última consulta SQL y sus datos
last_query_state = {"sql": "", "data": []}

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
    global last_query_state
    last_query_state["sql"] = query
    last_query_state["data"] = []
    
    if not is_safe_sql(query):
        return "ERROR DE SEGURIDAD: Consulta bloqueada por el validador (SQL Guard). Solo se permite SELECT."
    
    output = ""
    results = []
    try:
        with engine.connect() as con:
            rows = con.execute(text(query))
            for row in rows:
                # Extraemos a un diccionario para poder serializarlo a JSON en el Frontend
                results.append(dict(row._mapping))
                output += "\n" + str(row)
                
        last_query_state["data"] = results
        
        if not output:
            return "La consulta se ejecutó con éxito pero no devolvió resultados."
        return output
    except Exception as e:
        return f"Error ejecutando SQL: {e}"

sql_engine.description += f"\n\n{get_schema_description()}"

def run_agent(question: str, provider: str = "mock"):
    global last_query_state
    last_query_state = {"sql": "", "data": []} # Reiniciar estado
    
    if provider == "mock":
        # Simulamos una llamada falsa
        time.sleep(2)
        last_query_state["sql"] = "SELECT * FROM mock_table LIMIT 1;"
        last_query_state["data"] = [{"id": 1, "mock_status": "Funciona Perfectamente!"}]
        return "Esta es una respuesta simulada por el modo Mock. ¡Todo funciona bien!", last_query_state["sql"], last_query_state["data"]

    # Determinar el modelo según el proveedor
    try:
        if provider == "huggingface":
            if not os.getenv("HF_TOKEN"):
                raise ValueError("HF_TOKEN no está configurado en .env")
            model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
            
        elif provider == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY no está configurado en .env")
            model = LiteLLMModel(model_id="gpt-4o-mini")
            
        elif provider == "deepseek":
            if not os.getenv("DEEPSEEK_API_KEY"):
                raise ValueError("DEEPSEEK_API_KEY no está configurado en .env")
            model = LiteLLMModel(model_id="deepseek/deepseek-chat")
            
        else:
            raise ValueError(f"Proveedor desconocido: {provider}")

        agent = CodeAgent(
            tools=[sql_engine],
            model=model,
            additional_authorized_imports=["sqlalchemy"]
        )
        
        respuesta = agent.run(question)
        return str(respuesta), last_query_state["sql"], last_query_state["data"]
        
    except Exception as e:
        raise Exception(f"Error en el agente ({provider}): {e}")
