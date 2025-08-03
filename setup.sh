#!/bin/bash
set -e

# Instalar dependencias del sistema
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt