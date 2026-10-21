# AI Knowledge Assistant

API asíncrona para el curso ADSO sena - Módulo I (integración LLM con OpenRouter).

Este proyecto es el primer incremento funcional del AI Knowledge Assistant: una API REST asíncrona con FastAPI, preparada para evolucionar hacia un sistema de IA real en módulos posteriores.

## 🚀 Tecnologías

- **Python 3.12+**: Lenguaje principal
- **FastAPI**: Framework moderno para APIs REST
- **Pydantic**: Validación de datos con type hints
- **AsyncIO**: Programación asíncrona en Python
- **HTTPX**: Cliente HTTP asíncrono
- **pytest**: Framework de pruebas automatizadas
- **Git/GitHub**: Control de versiones

## 📋 Requisitos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/esteban64-64/MINI-PROYECTO.git
cd MINI-PROYECTO
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

**En Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -e ".[dev]"
```

### 4. Configurar OpenRouter

Copia `.env.example` a `.env` y coloca tu clave (`OPENROUTER_API_KEY`). `.env` está en `.gitignore`.
Para los experimentos fija un modelo concreto en `OPENROUTER_MODEL` (`openrouter/free` puede enrutar a distintos modelos).

## 🏃 Ejecución

### Iniciar el servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

### Acceder a la documentación Swagger

Abre tu navegador en: **http://localhost:8000/docs**

Allí podrás ver todos los endpoints, probarlos y ver los esquemas de datos.

## 🧪 Pruebas

### Ejecutar todas las pruebas

```bash
python -m pytest -q
```

### Ejecutar pruebas con detalles

```bash
python -m pytest -v
```

### Ejecutar pruebas específicas

```bash
# Solo pruebas unitarias
python -m pytest tests/unit/

# Solo pruebas de integración
python -m pytest tests/integration/
```

## 📡 Endpoints

### GET /health
Health check de la API.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /api/v1/chat
Envía la pregunta al LLM a través de OpenRouter.

**Request:**
```json
{
  "question": "¿Qué es un LLM?",
  "temperature": 0.3,
  "top_p": 1.0,
  "max_tokens": 300
}
```

**Validación (422 si falla, sin llamar al LLM):**
- `question`: 3 a 2000 caracteres
- `temperature`: 0 a 1.5 (por defecto 0.3)
- `top_p`: mayor que 0 y hasta 1 (por defecto 1.0)
- `max_tokens`: 1 a 2000 (por defecto 300)

**Response 200:**
```json
{
  "answer": "Un LLM es...",
  "model": "<modelo efectivamente servido>"
}
```

**Response 502:** error controlado del proveedor (timeout, HTTP 429/5xx, respuesta sin `choices`, falta de API key).

### GET /api/v1/info
Información básica del proyecto.

**Response:**
```json
{
  "name": "AI Knowledge Assistant",
  "version": "0.2.0",
  "environment": "development",
  "llm_enabled": true,
  "model": "openrouter/free"
}
```

## 📁 Estructura del Proyecto

```
app/
├── main.py                       # Aplicación FastAPI
├── api/
│   ├── chat.py                   # Router POST /api/v1/chat (Depends + 502)
│   └── routes/
│       ├── health.py             # GET /health
│       └── info.py               # GET /api/v1/info
├── core/config.py                # Lectura de .env (API key, modelo, timeout)
├── schemas/chat.py               # Pydantic: question, temperature, top_p, max_tokens
├── services/assistant_service.py # System prompt + orquestación
└── providers/
    ├── base.py                   # Contrato LLMProvider, LLMResult, LLMProviderError
    └── openrouter.py             # Adaptador HTTPX hacia OpenRouter
tests/
├── fakes.py                      # FakeLLMProvider
├── unit/                         # Servicio y adaptador (MockTransport: timeout, 429, sin choices)
└── integration/test_api.py       # 200, 422 y 502 sin consumo externo
scripts/
├── asyncio_demo.py
└── httpx_demo.py
```

## 🔄 Flujo de una solicitud

Cliente/Swagger → Router (`app/api/chat.py`) → Pydantic (`app/schemas/chat.py`, 422) →
Service (`app/services/assistant_service.py`) → Contrato (`app/providers/base.py`) →
Adaptador HTTPX (`app/providers/openrouter.py`) → OpenRouter/LLM → respuesta por las mismas capas
(error del proveedor → `LLMProviderError` → 502).

## 🔑 Conceptos Clave

### FastAPI
Framework moderno para crear APIs REST con:
- Validación automática de datos
- Documentación Swagger/OpenAPI integrada
- Soporte nativo para async/await

### Pydantic
Librería de validación de datos basada en type hints de Python:
- Valida entradas automáticamente
- Retorna error HTTP 422 si la validación falla
- Genera documentación automática

### AsyncIO
Biblioteca estándar de Python para programación asíncrona:
- `async def`: Define funciones asíncronas
- `await`: Espera operaciones I/O sin bloquear
- Permite manejar múltiples solicitudes concurrentemente

### HTTPX
Cliente HTTP moderno con soporte síncrono y asíncrono:
- Usado en pruebas de integración
- Compatible con aplicaciones ASGI como FastAPI

### Git vs GitHub
- **Git**: Sistema de control de versiones local
- **GitHub**: Servicio de hosting de repositorios Git en la nube

## 🎯 Próximos Pasos

- ✔ LLM real vía OpenRouter (Módulo I)
- ✗ RAG (Retrieval-Augmented Generation)
- ✗ Bases vectoriales
- ✗ Agentes
- ✗ Observabilidad (tokens y costo)

## 📝 Notas Importantes

- La API key se lee de `.env`; nunca se sube al repositorio ni aparece en respuestas de error.
- Las pruebas usan `FakeLLMProvider` y `httpx.MockTransport`: no consumen OpenRouter.

## 🤝 Contribución

Este es un proyecto educativo para el curso ADSO sena.

## 📄 Licencia

Proyecto educativo - SENA
