# Text-to-SQL AI Database Solutions (Safe SQL Agent)

Este proyecto es un entorno reproducible ("Laboratorio") para probar arquitecturas Text-to-SQL seguras. Se centra en la implementación de un agente de IA que interactúa con bases de datos SQL (inspirado en `smolagents` de Hugging Face), incorporando una capa robusta de validación para evitar inyecciones y operaciones destructivas.

## Arquitectura

- **Base de Datos**: SQLite (en memoria o archivo local).
- **Backend / Orquestación**: Python nativo.
- **Framework de Agentes**: `smolagents` de Hugging Face (CodeAgent compatible).
- **Seguridad (SQL Guard)**: Interceptor de consultas (`validator.py`) para garantizar operaciones seguras.
- **Inicialización**: Scripts Python (`db.py`) sobre archivos `.sql` puros para definir esquemas y cargar datos semilla.

## Características Principales (Fase Actual)

- **Agente Basado en Código**: En lugar de depender de un simple prompt estático, el flujo permite que el orquestador razone sobre la base de datos (Pensar -> Actuar -> Observar -> Responder), dándole la capacidad de autocorregirse ante errores de sintaxis SQL.
- **Seguridad Interceptiva**: La aplicación (`app.py`) ilustra de manera directa la diferencia entre una consulta SQL válida (aprobada por el validador) y una destructiva (interceptada y bloqueada).
- **Transparencia**: Todo el flujo (pregunta del usuario, SQL generado y resultado de validación) se muestra en consola.

## Seguridad (SQL Guard)

El sistema incorpora un mecanismo de seguridad estricto (`validator.py`) que:
- Bloquea explícitamente consultas de modificación (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`).
- Asegura que todas las sentencias sean de tipo solo lectura (`SELECT`).
- Previene inyección múltiple bloqueando sentencias encadenadas por punto y coma (`;`).

## Instalación y Ejecución

1. Asegúrate de estar en el directorio correcto y con tu entorno virtual activo si aplica.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicializa la base de datos y sus datos de prueba:
   ```bash
   python db.py
   ```
4. Ejecuta la demostración interactiva:
   ```bash
   python app.py
   ```

## Próximos Pasos (Futuro)

- **Historial y Observabilidad**: Creación de una tabla `query_logs` para registrar métricas de latencia, cantidad de filas devueltas, éxito/falla y consultas en crudo.
- **Soporte Multi-Proveedor**: Integración profunda con modelos OpenAI, DeepSeek y Gemini.
- **Interfaz Web (Chat UI)**: Incorporar un frontend ligero para conversar directamente con el agente sin usar la terminal.
- **Limitación de Filas Inteligente**: Inyección automática de `LIMIT 20` (o similar) en las consultas aprobadas.
