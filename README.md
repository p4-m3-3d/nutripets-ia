# 🐾 NutriPets AI Pro — Panel Clínico & Motor RAG

NutriPets AI es un asistente clínico inteligente de nutrición animal que combina el poder de la **búsqueda semántica (RAG)** con un sistema relacional para ofrecer recomendaciones dietéticas, resolver consultas frecuentes y activar escudos de emergencia ante la detección de ingredientes tóxicos para perros y gatos.

La plataforma cuenta con un backend robusto de alto rendimiento y una interfaz médica premium basada en *Glassmorphic Design* con capacidades de memoria contextual fluida y renderizado dinámico.

---

## 🏗️ Arquitectura del Sistema

El ecosistema está diseñado bajo una arquitectura híbrida de datos:
* **Capa Relacional (MySQL):** Gestiona las entidades base como especies, etapas vitales, categorías clínicas y el histórico de feedback de usuarios.
* **Capa Vectorial (ChromaDB):** Indexa el conocimiento profundo (recetas avanzadas, guías digestivas, toxinas y preguntas frecuentes) convirtiendo la información en embeddings para realizar búsquedas conceptuales e inmediatas.
* **Orquestación (FastAPI + LLM):** Valida las consultas, gestiona el historial de conversación en memoria y genera respuestas personalizadas procesadas mediante Ollama u OpenAI.

---

## ⚡ Características Clave

### 🤖 Motor de Inteligencia Artificial & RAG
* **Detección de Alertas Críticas:** Escaneo en tiempo real de más de 30 toxinas, plantas (como lirios) y químicos del hogar, activando un protocolo de emergencia visual instantáneo si la mascota está en riesgo.
* **Contexto de Sesión Dinámico:** El sistema recuerda la especie (Perro/Gato) y la etapa de vida (Cachorro/Adulto/Senior) durante la conversación para refinar las respuestas sin que el usuario deba repetirlas.
* **Clasificación Cruzada:** Filtrado inteligente de recetas clínicas basadas en categorías específicas (Renal, Control de Peso, Hipoalergénica, Digestiva).

### 🎨 Interfaz Avanzada (UI/UX Premium)
* **Diseño Glassmorphism:** Interfaz oscura, limpia y estilizada con desenfoques de fondo (`backdrop-blur`) optimizada para entornos clínicos o de visualización prolongada.
* **Typing Indicator Fluido:** Feedback visual animado mientras el motor RAG computa los embeddings y genera la respuesta.
* **Renderizado Markdown Nativo:** Conversión automática de listas, negritas y tablas generadas por la IA a HTML estructurado y elegante gracias a `marked.js`.
* **Inspector de Metadatos:** Un panel desplegable integrado en cada mensaje para auditar qué entidades detectó la IA y cuántas fuentes RAG utilizó.
* **Módulo de Feedback Clínico:** Botones de calificación (*Thumbs Up/Down*) conectados directamente al backend para el entrenamiento continuo del modelo.

---

## 🛠️ Requisitos del Sistema

* **Python 3.11 o superior**
* **MySQL Server** (Instancia activa y configurada)
* **Ollama / OpenAI API** (Dependiendo del proveedor de LLM seleccionado)
* Un navegador web moderno (Chrome, Edge, Firefox, Safari)

---

## 🚀 Instalación y Despliegue

### 1. Configuración del Backend

Navega al directorio del backend, inicializa el entorno virtual e instala las dependencias requeridas:

cd backend
python -m venv venv

# Activar en Linux/macOS:
source venv/bin/activate  
# Activar en Windows:
venv\Scripts\activate  

pip install -r requirements.txt


### 2. Variables de Entorno (.env)

Crea un archivo `.env` en la raíz de la carpeta `backend` siguiendo esta estructura base:

DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nutripets_db
OLLAMA_HOST=http://localhost:11434
# Si usas OpenAI opcionalmente:
# OPENAI_API_KEY=tu_sk_key


### 3. Lanzamiento del Servidor

Inicia el servicio web asíncrono con Uvicorn:

uvicorn app.main:app --reload

* **API disponible en:** http://127.0.0.1:8000
* **Documentación interactiva (Swagger UI):** http://127.0.0.1:8000/docs

---

## 💾 Carga Inicial e Indexación Vectorial

Para poblar las tablas relacionales de MySQL y construir los índices de vectores en ChromaDB con el set de datos expandido, ejecuta los siguientes endpoints en orden (puedes hacerlo desde la documentación de Swagger):

1.  **Poblar Base de Datos Relacional:**
    `POST /loader/all` -> Lee los archivos maestros de configuración y estructuras.
2.  **Generar Embeddings e Indexar RAG:**
    `POST /ai/index` -> Procesa de forma masiva los JSON de recetas, FAQs, consejos e ingredientes tóxicos hacia el almacén de vectores.

---

## 💻 Acceso al Frontend

La interfaz de usuario no requiere de compiladores complejos (como Node.js/Vite) al consumir los estilos de última generación directamente. 

Simplemente abre el archivo de forma local en tu navegador favorito o sírvelo mediante una extensión estática (como *Live Server* en VS Code):

frontend/index.html

---

## 📂 Estructura del Proyecto

```text
├── backend/
│   ├── app/
│   │   ├── main.py          # Punto de entrada de la API FastAPI
│   │   ├── core/            # Configuración, seguridad y variables de entorno
│   │   ├── database/        # Conexión a MySQL y esquemas ORM
│   │   └── services/        # Lógica del RAG, embeddings y conexión con LLM
│   ├── data/                # Archivos JSON origen (recetas, toxic_ingredients, etc.)
│   └── requirements.txt     # Dependencias de Python
└── frontend/
    └── index.html           # Panel clínico interactivo (Tailwind v4 + Lucide + Marked)