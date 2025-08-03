#!/bin/bash
set -e

# Instalar Python 3.9 específicamente
apt-get update && apt-get install -y python3.9 python3.9-dev

# Configurar Python 3.9 como predeterminado
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Instalar dependencias del sistema
apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev

# Instalar pip para Python 3.9
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

# Instalar dependencias Python
python3.9 -m pip install --upgrade pip setuptools wheel
python3.9 -m pip install -r requirements.txt