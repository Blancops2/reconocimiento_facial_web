FROM python:3.9.11-slim-buster

# 1. Instala dependencias del sistema CRÍTICAS primero
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura un entorno virtual limpio
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Instala dependencias con build optimizado
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copia la aplicación
COPY . .
CMD ["streamlit", "run", "app.py"]