# AI Knowledge Assistant

API asíncrona para el curso de Ingeniería de Sistemas de IA - Módulo 0.

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
Endpoint para enviar preguntas al asistente.

**Request:**
```json
{
  "question": "¿Qué es FastAPI?"
}
```

**Validación:**
- `question`: Mínimo 3 caracteres, máximo 2000 caracteres

**Response:**
```json
{
  "answer": "FastAPI es un framework de Python para construir APIs basado en type hints y ASGI.",
  "provider": "bootstrap-local"
}
```

### GET /api/v1/info
Información básica del proyecto.

**Response:**
```json
{
  "name": "AI Knowledge Assistant",
  "version": "0.1.0",
  "environment": "development",
  "llm_enabled": false
}
```

## 📁 Estructura del Proyecto

```
ai-knowledge-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # Endpoint /health
│   │       ├── chat.py         # Endpoint /api/v1/chat
│   │       └── info.py         # Endpoint /api/v1/info
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── health.py           # Modelos Pydantic para health
│   │   └── chat.py             # Modelos Pydantic para chat
│   └── services/
│       ├── __init__.py
│       └── assistance_service.py  # Lógica de negocio del asistente
├── scripts/
│   └── asyncio_demo.py         # Demostración de AsyncIO
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_assistant_service.py  # Pruebas unitarias
│   └── integration/
│       ├── __init__.py
│       └── test_api.py         # Pruebas de integración
├── .gitignore
├── pyproject.toml              # Configuración del proyecto y dependencias
└── README.md
```

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

## 🎯 Próximos Pasos (Módulos Futuros)

Este proyecto es la base técnica. En módulos posteriores se integrará:
- ✗ LLM real (OpenAI, Anthropic, etc.)
- ✗ RAG (Retrieval-Augmented Generation)
- ✗ Bases vectoriales
- ✗ Agentes
- ✗ Observabilidad

## 📝 Notas Importantes

- Este proyecto **NO** integra LLMs reales todavía
- La lógica del asistente usa respuestas predefinidas (bootstrap)
- Todas las pruebas deben pasar antes de entregar
- El repositorio no contiene secretos ni credenciales

## 🤝 Contribución

Este es un proyecto educativo para el curso de Ingeniería de Sistemas de IA.

## 📄 Licencia

Proyecto educativo - SENA
