import os
from db import get_connection
from validator import is_safe_sql

def ask_database(question: str, generated_sql: str) -> str:
    print(f"Pregunta del usuario: {question}")
    print(f"SQL Generado por IA:\n{generated_sql}\n")
    
    if not is_safe_sql(generated_sql):
        return "Consulta bloqueada por el validador: operación no permitida."

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(generated_sql)
            rows = cursor.fetchall()
            return f"Resultado de la consulta: {rows}"
    except Exception as e:
        return f"Error ejecutando SQL: {e}"

def main():
    print("--- Asistente SQL Seguro con IA ---")
    
    pregunta = "¿Cuál es el total de ventas por mes?"
    
    # Simulación de un LLM generando SQL válido
    sql_valido = "SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS total FROM sales GROUP BY month ORDER BY month;"
    
    print("\n[Escenario 1: Consulta Válida]")
    resultado = ask_database(pregunta, sql_valido)
    print(resultado)
    
    print("\n[Escenario 2: Intento de Inyección o Modificación]")
    sql_invalido = "DELETE FROM sales WHERE total_amount > 100;"
    resultado_invalido = ask_database("Borra las ventas mayores a 100", sql_invalido)
    print(resultado_invalido)

if __name__ == "__main__":
    if not os.path.exists("safe_sql_demo.db"):
        import db
        db.setup_db()
    main()
