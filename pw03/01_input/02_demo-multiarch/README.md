# Demo: Multi-Architektur-Builds
## M347 – Dienst mit Container anwenden

Die App gibt beim Start die laufende CPU-Architektur aus, so siehst du
direkt, ob QEMU die ARM-Emulation übernommen hat.

---

## Projektstruktur

```
02_demo-multiarch/
├── Dockerfile        ← Multi-Stage + Multi-Arch
├── requirements.txt
├── src/
│   └── main.py       ← FastAPI-App (gibt Architektur aus)
└── README.md
```

---

## Schritt 1 – Builder einrichten (einmalig)

```bash
docker buildx create --name multibuilder --use
docker buildx inspect --bootstrap
```

**Erwartete Ausgabe:** Liste der unterstützten Plattformen, u.a.:
`linux/amd64, linux/arm64, linux/arm/v7`

---

## Schritt 2 – Image für ARM lokal bauen und laden

```bash
docker buildx build --platform linux/arm64 --load -t demo-multiarch:arm64 .
```

> `--load` lädt das Image in die lokale Docker Engine.
> Nur eine Plattform gleichzeitig möglich.

---

## Schritt 3 – ARM-Image lokal ausführen (QEMU emuliert)

```bash
docker run --rm -p 8000:8000 demo-multiarch:arm64
```

Browser öffnen: http://localhost:8000

**Erwartete Ausgabe:**
```json
{
  "message": "Hallo vom Multi-Arch-Container!",
  "architecture": "aarch64",
  "system": "Linux",
  "python": "3.12.x"
}
```

`aarch64` = ARM 64-Bit — QEMU hat die Emulation übernommen!

---

## Schritt 4 – Zum Vergleich: natives amd64-Image

```bash
docker buildx build \
  --platform linux/amd64 \
  --load \
  -t demo-multiarch:amd64 .

docker run --rm -p 8000:8000 demo-multiarch:amd64
```

**Erwartete Ausgabe:** `"architecture": "x86_64"`

---

## Schritt 5 – Beide Plattformen gleichzeitig bauen (Push)

> Voraussetzung: Docker Hub Login (`docker login`)

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t DEIN_USERNAME/demo-multiarch:1.0 \
  --push .
```

---

## Schritt 6 – Manifest prüfen

```bash
docker buildx imagetools inspect DEIN_USERNAME/demo-multiarch:1.0
```

**Erwartete Ausgabe:** Zwei Manifests — eines für amd64, eines für arm64.

---

## Bonus: Architektur im Build-Prozess ausgeben

Im Dockerfile ist `ARG TARGETARCH` gesetzt. Baue mit verbose Output:

```bash
docker buildx build \
  --platform linux/arm64 \
  --progress=plain \
  --load \
  -t demo-multiarch:arm64 . 2>&1 | grep -i "arch\|platform\|baue"
```
