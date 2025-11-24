FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY ./app ./app

# Expor porta
EXPOSE 8000

# Comando para iniciar (sem --reload em producao)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
