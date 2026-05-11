# syntax=docker/dockerfile:1

# Stage 1 – Build
# BUILDPLATFORM = Plattform des Build-Hosts (z. B. linux/amd64)
# Abhängigkeiten werden immer auf dem Host gebaut (schneller als QEMU-Emulation)
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 – Runtime
# Dieses Stage läuft auf der ZIEL-Plattform (z. B. linux/arm64)
FROM python:3.12-slim

WORKDIR /app

# Installierte Pakete aus dem Builder übernehmen
COPY --from=builder /root/.local /root/.local

# App-Code kopieren
COPY src/ .

# Plattform-Info beim Start ausgeben (zeigt dass ARM wirklich läuft)
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
