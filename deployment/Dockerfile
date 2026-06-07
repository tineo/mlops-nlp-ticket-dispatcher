FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema y de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar datos de NLTK en tiempo de construcción
RUN python -c "import nltk; nltk.download('stopwords')"

# Copiar el código fuente y estructura
COPY src/ /app/src/

# En Azure Kubernetes Service (AKS), el modelo entrenado se puede
# inyectar como un volumen persistente o descargar durante el inicio.
# Para empaquetar la PoC local, asumiremos que "model" ya existe en /app/model
# después del entrenamiento.
# COPY model/ /app/model/

ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/model

EXPOSE 8000

# Lanzar el servidor ASGI FastAPI usando Uvicorn
CMD ["uvicorn", "src.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
