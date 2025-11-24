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

# Expor porta (Railway define PORT automaticamente)
EXPOSE 8000

# Usar shell form para interpretar a variavel $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
