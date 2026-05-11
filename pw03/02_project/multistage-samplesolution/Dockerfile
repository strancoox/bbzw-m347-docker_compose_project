# ── Musterlösung: Multi-Stage Build ──────────────────────────────────────────

# Stage 1 – Builder
# Alle Build-Abhängigkeiten landen hier – nicht im finalen Image
FROM python:3.12 AS builder
WORKDIR /build

# requirements.txt zuerst kopieren → pip install wird gecacht
# solange sich requirements.txt nicht ändert
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 – Runtime
# Nur das Nötigste: slim-Image + installierte Pakete + Quellcode
FROM python:3.12-slim
WORKDIR /app

# Nur die installierten Pakete aus Stage 1 übernehmen
COPY --from=builder /root/.local /root/.local

# Quellcode zuletzt kopieren (ändert sich häufiger als Abhängigkeiten)
COPY src/ .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
