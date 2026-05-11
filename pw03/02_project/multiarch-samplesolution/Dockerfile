# ── Musterlösung: Multi-Architektur-Build (Raspberry Pi) ─────────────────────
# syntax=docker/dockerfile:1
#
# Unterstützte Plattformen:
#   linux/amd64    – Laptop / Server
#   linux/arm64    – Raspberry Pi 4 / 5
#   linux/arm/v7   – Raspberry Pi 2 / 3
#
# WICHTIG: Kein --platform=$BUILDPLATFORM im Builder!
# pydantic enthält nativen C-Code und muss für die Zielarchitektur kompiliert werden.
# Mit $BUILDPLATFORM würden die Pakete für den Host (amd64) gebaut und das
# ARM-Image würde mit "ModuleNotFoundError: pydantic_core._pydantic_core" abstürzen.

# Stage 1 – Builder (läuft auf Zielplattform, QEMU emuliert wenn nötig)
FROM python:3.12-slim AS builder
WORKDIR /build

# Verfügbare Build-ARGs (automatisch von BuildKit gesetzt):
# BUILDPLATFORM  = Plattform des Build-Hosts  (z. B. linux/amd64)
# TARGETPLATFORM = Zielplattform              (z. B. linux/arm/v7)
# TARGETOS / TARGETARCH = Einzelne Komponenten
ARG TARGETPLATFORM
ARG TARGETARCH
RUN echo "Baue für: TARGETPLATFORM=$TARGETPLATFORM, TARGETARCH=$TARGETARCH"

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 – Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
