# Sistema Inteligente de Enrutamiento de Tickets de Soporte (MLOps PoC)

![MLOps Architecture](https://img.shields.io/badge/Architecture-Azure_ML_%7C_AKS_%7C_MLflow-blue)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)

Este repositorio contiene una Prueba de Concepto (PoC) de nivel portafolio que demuestra un ciclo de vida completo de MLOps aplicado al Procesamiento de Lenguaje Natural (NLP). El sistema toma tickets de soporte entrantes de clientes, procesa el texto, predice el departamento correspondiente y asigna el ticket automáticamente.

## 🚀 Arquitectura y Tecnologías Clave

El pipeline fue construido con el paradigma de producción en mente, aplicando principios MLOps:

1. **Procesamiento de Datos (Data Pipeline):**
   - **NLTK / Expresiones Regulares**: Limpieza profunda del texto, remoción de puntuación y *stop words* para aislar el núcleo semántico del mensaje del cliente.
2. **Entrenamiento y Tracking (MLflow + Azure ML):**
   - **Scikit-Learn**: Uso de `TfidfVectorizer` y `LogisticRegression` construidos dentro de un `Pipeline` para garantizar reproducibilidad en inferencia.
   - **MLflow**: Integrado para el registro automático de métricas (Accuracy), hiperparámetros y almacenamiento del modelo en formato estandarizado.
3. **Integración Continua (CI/CD):**
   - **GitHub Actions**: Pipeline de CI que ejecuta **Pytest** automáticamente tras cada `push` para validar que las lógicas de negocio (como el preprocesamiento) no se han roto.
4. **Despliegue y Empaquetado (Serving):**
   - **FastAPI**: API REST asíncrona de altísimo rendimiento para exponer el modelo.
   - **Docker / Kubernetes (AKS)**: La API y el modelo están dockerizados con manifiestos YAML listos para ser desplegados en Azure Kubernetes Service (AKS).
5. **Monitoreo Continuo:**
   - **Evidently AI**: Script conceptual de detección de "Data Drift" (deriva de datos) para alertar cuando el lenguaje de los clientes en producción se desvíe estadísticamente de los datos de entrenamiento base.

---

## 📂 Estructura del Proyecto

```text
mlops-nlp-ticket-dispatcher/
├── data/                    # Almacenamiento local de datasets y logs (ignorado en git)
├── src/
│   ├── data/
│   │   └── preprocess.py    # Funciones de limpieza de texto NLP
│   ├── model/
│   │   └── train.py         # Script de entrenamiento y tracking MLflow
│   └── serving/
│       └── app.py           # Inferencia usando FastAPI
├── tests/
│   └── test_preprocess.py   # Unit tests ejecutados por CI
├── deployment/
│   ├── Dockerfile           # Imagen de producción
│   └── k8s/                 # Manifiestos de Kubernetes (Deployment, Service)
├── monitoring/
│   └── drift_detection.py   # Script de análisis estadístico de drift
└── .github/workflows/
    └── ci.yaml              # Pipeline de GitHub Actions
```

---

## 💻 Ejecución Local (Guía Rápida)

Sigue estos pasos para probar la PoC en tu máquina local:

### 1. Instalación de Dependencias

Se recomienda usar un entorno virtual (`venv` o `conda`).
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

### 2. Ejecutar Pruebas Unitarias
Valida que el componente de procesamiento de lenguaje natural funciona correctamente:
```bash
pytest tests/
```

### 3. Entrenar el Modelo
Ejecuta el pipeline de ML. Esto creará una carpeta temporal `mlruns` (tracking local de MLflow) y guardará el binario del modelo en la carpeta local `model`. Si no hay dataset real, el script generará datos de prueba automáticamente.
```bash
python src/model/train.py
```

### 4. Levantar la API de Inferencia
Inicia el servidor web FastAPI para probar predicciones en tiempo real.
```bash
# Definimos la variable de entorno para que FastAPI sepa dónde buscar el modelo
export MODEL_PATH=model
uvicorn src.serving.app:app --host 0.0.0.0 --port 8000
```

### 5. Probar el Endpoint REST
Con la API corriendo en el puerto 8000, puedes enviarle peticiones POST:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"ticket": "Necesito devolver un producto roto que compré ayer"}'
```

---

## 📈 Siguientes Pasos (Evolución a Producción)

Para llevar esta PoC a un entorno 100% de producción en Azure:
1. Conectar **MLflow Tracking URI** al Workspace de Azure Machine Learning.
2. Modificar el bloque de carga del modelo en FastAPI para descargarlo directamente del **Azure ML Model Registry**.
3. Configurar **Azure DevOps** o GitHub Actions para compilar el `Dockerfile` y empujar la imagen a **Azure Container Registry (ACR)** automáticamente tras un PR exitoso.
4. Desplegar los manifiestos de `deployment.yaml` usando `kubectl apply -f deployment/k8s/` hacia el clúster AKS.
