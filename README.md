# NutriPets IA

Aplicación para recomendar alimentos, responder preguntas sobre nutrición de mascotas y detectar situaciones de riesgo mediante IA.

## Funcionalidades
- API REST con FastAPI
- búsqueda semántica sobre recetas, FAQ y consejos
- detección de ingredientes tóxicos
- interfaz web simple para probar el sistema

## Requisitos
- Python 3.11+
- MySQL configurado
- Ollama disponible si se quiere usar el generador de respuestas

## Ejecución del backend
1. Entrar a la carpeta del backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # o venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
2. Iniciar la API:
   ```bash
   uvicorn app.main:app --reload
   ```
3. La API quedará disponible en:
   - http://127.0.0.1:8000/docs
   - http://127.0.0.1:8000

## Carga inicial de datos
Puedes usar los endpoints:
- `POST /loader/all` para cargar catalogos y datos base
- `POST /ai/index` para construir el índice vectorial

## Interfaz web
Abre [frontend/index.html](frontend/index.html) en un navegador o sirve la carpeta con un servidor estático.

## Variables de entorno
Crea un archivo `.env` dentro de la carpeta `backend` con la configuración de la base de datos y el servicio de IA si es necesario.
