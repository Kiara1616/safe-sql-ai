# Text-to-SQL AI Database Solutions (Safe SQL Agent - Enterprise)

Este proyecto es un entorno reproducible ("Laboratorio") para probar arquitecturas Text-to-SQL seguras. En su iteración actual (Fase 2.5), se ha evolucionado de un simple script de consola a una **Aplicación Web Full-Stack Multi-IA**.

El núcleo del proyecto es un agente de IA que interactúa con bases de datos SQL, protegido por un **SQL Guard** determinista que intercepta y bloquea consultas destructivas antes de que toquen la base de datos.

## 🚀 Novedades (Fase 2.5)
- **Interfaz Web (Studio):** Una UI moderna (HTML/CSS/JS puros) con diseño "Glassmorphism" que muestra el mensaje natural de la IA, el código SQL exacto que generó, y una tabla HTML con los datos crudos resultantes.
- **Multi-Proveedor de IA:** Soporte dinámico para Hugging Face (`Qwen2.5-Coder`), OpenAI (`GPT-4o-Mini`) y DeepSeek (`DeepSeek-Chat`) a través de `litellm`.
- **Modo Mock (Demo sin costo):** Capacidad de probar el flujo de la aplicación de manera local, recibiendo respuestas simuladas, sin consumir tokens ni internet.
- **Backend Robusto:** API impulsada por `FastAPI` y estructuración modular del código (`src`, `config`, `migrations`).

## ⚙️ Arquitectura
1. **Frontend:** HTML/CSS/JS (Vanilla).
2. **Backend:** Python (FastAPI, Uvicorn, smolagents, litellm).
3. **Seguridad (SQL Guard):** Script determinista que obliga a usar solo sentencias `SELECT` no encadenadas.
4. **Base de Datos:** SQLite (`safe_sql_demo.db`).

## 🛠️ Instalación y Configuración

Para utilizar este proyecto en tu máquina local, sigue estos pasos:

### 1. Clonar el repositorio y dependencias
```bash
# Clona este repositorio
git clone https://github.com/KiaaraZM/safe-sql-ai.git
cd safe-sql-ai

# Instala las dependencias
pip install -r requirements.txt
```

### 2. Configurar los Tokens de IA (Importante)
Por seguridad, la interfaz web no te pedirá los tokens. Debes crear un archivo llamado `.env` en la raíz del proyecto y agregar las claves de los proveedores que desees utilizar:

```env
# Agrega el token de Hugging Face si vas a usar Qwen2.5
HF_TOKEN=tu_token_aqui

# Agrega si vas a usar OpenAI
OPENAI_API_KEY=tu_token_aqui

# Agrega si vas a usar DeepSeek
DEEPSEEK_API_KEY=tu_token_aqui
```
*(Nota: Si solo vas a usar el "Modo Mock", no necesitas configurar ningún token).*

### 3. Inicializar la Base de Datos
Ejecuta las migraciones para crear las tablas `customers` y `sales`, y poblar la base de datos de ejemplo:
```bash
python scripts/run_migrations.py
```

### 4. Ejecutar el Servidor Web
Levanta el backend de FastAPI:
```bash
uvicorn src.main:app --port 8080
```
Finalmente, abre **http://localhost:8080** en tu navegador para empezar a chatear con la base de datos.

## 🔒 Seguridad (SQL Guard)
El archivo `src/validator.py` bloquea cualquier instrucción como `DROP`, `DELETE`, `UPDATE`, `INSERT` o `ALTER`. Ante un intento de modificación (incluso inyecciones en subconsultas o sentencias separadas por `;`), el validador abortará la operación antes de que llegue al motor SQLite.
