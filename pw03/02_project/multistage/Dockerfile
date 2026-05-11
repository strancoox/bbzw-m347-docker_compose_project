# Dieses Dockerfile hat zwei Probleme – finde und behebe sie:
# 1. Die Layer-Reihenfolge ist nicht cache-optimal
# 2. Es verwendet kein Multi-Stage Build

FROM python:3.12
WORKDIR /app

# Problem: Quellcode wird vor den Abhängigkeiten kopiert
COPY src/ .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
