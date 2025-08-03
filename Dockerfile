FROM python:3.9.11-slim-buster

# 1. Actualiza repositorios y limpia cache
RUN apt-get update -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 2. Configura entorno Python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["streamlit", "run", "app.py"]