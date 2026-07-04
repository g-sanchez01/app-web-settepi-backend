FROM python:3.11

WORKDIR /app

# =========================
# Dependencias del sistema
# =========================
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# =========================
# Microsoft ODBC Driver 18
# =========================
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# =========================
# Dependencias Python
# =========================
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# Código fuente
# =========================
COPY . .

# =========================
# Cloud Run port
# =========================
EXPOSE 8080

# =========================
# Start command (IMPORTANTE: usa PORT dinámico)
# =========================
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]