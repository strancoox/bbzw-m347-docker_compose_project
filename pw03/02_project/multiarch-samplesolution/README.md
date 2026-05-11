# Musterlösung: Multi-Architektur-Build

## Erwartete Ausgaben

### linux/arm/v7 (Raspberry Pi 2/3)
```json
{
  "message": "Hallo vom Multi-Arch-Container!",
  "architecture": "armv7l",
  "system": "Linux",
  "python": "3.12.x"
}
```

### linux/arm64 (Raspberry Pi 4/5)
```json
{
  "message": "Hallo vom Multi-Arch-Container!",
  "architecture": "aarch64",
  "system": "Linux",
  "python": "3.12.x"
}
```

### linux/amd64 (Laptop/Server)
```json
{
  "message": "Hallo vom Multi-Arch-Container!",
  "architecture": "x86_64",
  "system": "Linux",
  "python": "3.12.x"
}
```

---

## Alle Befehle in der richtigen Reihenfolge

```bash
# Builder einrichten
docker buildx create --name rpibuilder --use
docker buildx inspect --bootstrap

# ARMv7 lokal testen (Raspberry Pi 2/3)
docker buildx build --platform linux/arm/v7 --load -t arch-demo:armv7 .
docker run --rm -p 8000:8000 arch-demo:armv7

# ARM64 lokal testen (Raspberry Pi 4/5)
docker buildx build --platform linux/arm64 --load -t arch-demo:arm64 .
docker run --rm -p 8000:8000 arch-demo:arm64

# Multi-Arch pushen (alle drei Plattformen)
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t DEIN_USERNAME/arch-demo:latest \
  --push .

# Manifest prüfen
docker buildx imagetools inspect DEIN_USERNAME/arch-demo:latest
```
