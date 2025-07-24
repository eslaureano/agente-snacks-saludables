# 🤖 Agente GenAI de Marketing para Snacks Saludables

Esta aplicación es un **catálogo interactivo** que utiliza **Inteligencia Artificial Generativa (GenAI)** para automatizar tareas de marketing digital y análisis de productos en el contexto de una línea de **snacks saludables**.

---

## 🚀 ¿Qué hace esta app?

### 🔹 1. Catálogo visual desde imágenes locales
Carga automáticamente las imágenes de productos desde la carpeta `/imagenes_snacks` y las presenta como una galería inicial para seleccionar.

### 🔹 2. Generación automática de descripción
Al seleccionar una imagen, la app:
- Busca un texto base asociado en `/rag_docs`
- Utiliza un modelo LLM (GPT-4) para generar una descripción comercial en **formato persuasivo** y amigable
- También se puede adaptar para **extraer texto real del empaque con OCR** 

### 🔹 3. Creación de imagen promocional
A partir de la descripción, se genera una imagen **estilo campaña publicitaria para redes sociales** usando DALL·E (OpenAI API).

### 🔹 4. Análisis de comentarios sociales
Permite subir o pegar comentarios de usuarios y la app:
- Clasifica en positivo / negativo / neutro
- Muestra un **gráfico dinámico** con los resultados

### 🔹 5. 🔍 RAG simulado: Pregunta sobre el producto
Utiliza un **sistema de búsqueda de texto** basado en FAISS y embeddings para:
- Consultar información sobre cada snack
- Responder preguntas usando texto de `rag_docs` como contexto

---

## ⚙️ Instrucciones de ejecución

### 🔸 1. Requisitos
Instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

Asegúrate de tener un archivo `.env` con tu clave OpenAI

```
OPENAI_API_KEY=sk-project-xxxxxxxxxxxxxxxxxxxx
```

### 🔸 2. Generar el índice RAG
Antes de lanzar la app, ejecuta el siguiente script:

```bash
python rag_loader.py
```

Esto crea la carpeta `faiss_index/` con los vectores para búsqueda semántica.

### 🔸 3. Ejecutar la app

```bash
streamlit run app.py
```

---

## 🧩 Estructura del proyecto

```
.
├── app.py                 # Aplicación principal Streamlit
├── tools.py              # Herramientas LLM: descripción, imagen, feedback
├── rag_loader.py         # Construcción del índice FAISS
├── requirements.txt      # Dependencias necesarias
│
├── rag_docs/             # Textos por producto
├── imagenes_snacks/      # Imágenes de empaque
├── feedback/             # CSV con comentarios de usuarios
```

---

## 📦 Tecnologías usadas

- **LangChain + OpenAI** (GPT-4 + DALL·E)
- **FAISS** para búsqueda semántica (RAG)
- **Streamlit** como interfaz de usuario
- **Matplotlib** para análisis de comentarios


