# Auftrag: Multi-Architektur-Builds (Raspberry Pi)
## Modul 347 – Dienst mit Container anwenden 

---

## Lernziele

Nach diesem Auftrag kannst du:
- erklären, warum dieselbe App für verschiedene CPU-Architekturen gebaut werden muss
- einen `buildx`-Builder einrichten
- ein Image für `linux/arm/v7` (Raspberry Pi 2/3) und `linux/arm64` (Raspberry Pi 4/5) bauen
- ein ARM-Image lokal mit QEMU testen, ohne echte Hardware zu benötigen
- ein Multi-Arch-Manifest in eine Registry pushen und prüfen

---

## Zeitbedarf

ca. 45 Minuten

---

## Voraussetzungen

- Docker Desktop ist installiert und läuft
- `docker buildx` ist verfügbar (`docker buildx version`)
- Internetverbindung (für Registry-Push optional: Docker Hub Account)
- Auftrag Multi-Stage abgeschlossen (empfohlen)

---

## Hintergrund: Raspberry Pi und Architekturen

| Raspberry Pi Modell | Architektur | Docker-Plattform-String |
|---|---|---|
| Raspberry Pi 2 / 3 (32-Bit) | ARMv7 | `linux/arm/v7` |
| Raspberry Pi 4 / 5 (64-Bit) | ARM64 / AArch64 | `linux/arm64` |
| Entwickler-Laptop / Server | x86-64 | `linux/amd64` |

Ein auf deinem Laptop gebautes `linux/amd64`-Image **läuft nicht nativ** auf einem Raspberry Pi.
Mit Multi-Arch-Builds erstellst du ein einziges Image-Tag, das automatisch die richtige Variante liefert.

> **QEMU:** Docker Desktop hat QEMU integriert. Das bedeutet: du kannst ARM-Images
> auch ohne Raspberry Pi lokal bauen und testen — QEMU emuliert die ARM-CPU.

---

## Ausgangslage

Du erhältst eine einfache FastAPI-App, die beim Aufruf ihre laufende Architektur ausgibt:

```
multiarch/
├── Dockerfile
├── requirements.txt
└── src/
    └── main.py
```

---

## Schritt 1 – Projekt kennenlernen

**1.1** Schaue dir `src/main.py` an. Was gibt die App zurück?

**1.2** Baue das Image zunächst normal (für deinen lokalen Rechner):

```bash
docker build -t arch-demo:local .
docker run --rm -p 8000:8000 arch-demo:local
```

Öffne [http://localhost:8000](http://localhost:8000)

> Du wirst bei deinem Rechner `x86_64` oder `aarch64` sehen, je nach Architektur.

---

## Schritt 2 – buildx-Builder einrichten

Der Standard-Docker-Builder unterstützt nur die lokale Plattform.
Für Multi-Arch brauchen wir einen dedizierten Builder.

**2.1** Prüfe ob bereits ein Builder existiert:

```bash
docker buildx ls
```

**2.2** Erstelle einen neuen Builder:

```bash
docker buildx create --name rpibuilder --use
```

**2.3** Starte den Builder und prüfe die unterstützten Plattformen:

```bash
docker buildx inspect --bootstrap
```

> **Erwartete Ausgabe:** Unter `Platforms` solltest du u.a. sehen:
> `linux/amd64, linux/arm64, linux/arm/v7`
>
> Falls du einen Fehler erhältst (Timeout auf WSL2), versuche:
> ```bash
> docker buildx rm rpibuilder
> docker buildx create --name rpibuilder --driver-opt network=host --use
> docker buildx inspect --bootstrap
> ```

---

## Schritt 3 – ARM-Image für Raspberry Pi bauen (lokal testen)

Zuerst baust du nur für `linux/arm/v7` (Raspberry Pi 2/3) und lädst das Image lokal.

**3.1** Baue das Image für ARMv7:

```bash
docker buildx build \
  --platform linux/arm/v7 \
  --load \
  -t arch-demo:armv7 .
```

> **Hinweis:** Der Build dauert länger als gewohnt (1–3 Minuten).
> QEMU emuliert die ARM-Architektur beim Kompilieren der Python-Pakete.

**3.2** Führe das ARM-Image auf deinem Rechner aus:

```bash
docker run --rm -p 8000:8000 arch-demo:armv7
```

Öffne [http://localhost:8000](http://localhost:8000)

> **Was siehst du jetzt bei `architecture`?**
> Du solltest `armv7l` sehen — das ist der ARM 32-Bit Wert.
> QEMU hat die Ausführung übernommen, obwohl dein Rechner kein Raspberry Pi ist!

**3.3** Wiederhole den Test für Raspberry Pi 4/5 (`linux/arm64`):

```bash
docker buildx build \
  --platform linux/arm64 \
  --load \
  -t arch-demo:arm64 .

docker run --rm -p 8000:8000 arch-demo:arm64
```

> Was zeigt `architecture` jetzt an? 

---

## Schritt 4 – Beide Plattformen in einem Image bündeln

Jetzt baust du ein echtes Multi-Arch-Image, das beide Raspberry-Pi-Varianten abdeckt.

> **Voraussetzung:** Du benötigst einen Docker Hub Account für `--push`.
> Falls du keinen Account hast, überspringe den Push-Schritt und
> verwende nur `--load` mit einer Plattform.

**4.1** Login bei Docker Hub:

```bash
docker login
```

**4.2** Baue und pushe für beide ARM-Architekturen gleichzeitig:

```bash
docker buildx build \
  --platform linux/arm/v7,linux/arm64 \
  -t DEIN_USERNAME/arch-demo:rpi \
  --push .
```

> Ersetze `DEIN_USERNAME` durch deinen Docker Hub Benutzernamen.

**4.3** Optionally: alle drei Plattformen (inkl. Laptop/Server):

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t DEIN_USERNAME/arch-demo:latest \
  --push .
```

---

## Schritt 5 – Manifest prüfen

Nach dem Push kannst du überprüfen, welche Plattformen im Image enthalten sind.

**5.1** Inspiziere das Manifest:

```bash
docker buildx imagetools inspect DEIN_USERNAME/arch-demo:rpi
```

**Erwartete Ausgabe (gekürzt):**
```
Manifests:
  Platform: linux/arm/v7   Digest: sha256:...
  Platform: linux/arm64    Digest: sha256:...
```

> **Was bedeutet das?** Wenn ein Raspberry Pi 4 (`linux/arm64`) dieses Image pullt,
> bekommt er automatisch die `arm64`-Variante. Ein Raspberry Pi 3 (`linux/arm/v7`)
> bekommt die `armv7`-Variante. Kein manuelles Taggen nötig.

---

## Schritt 6 – Dockerfile verstehen: BUILDPLATFORM vs. TARGETPLATFORM

Öffne das `Dockerfile` und schaue dir die erste Zeile an:

```dockerfile
FROM python:3.12-slim AS builder
```

**6.1** Was passiert wenn du `--platform=$BUILDPLATFORM` ergänzt?

```dockerfile
FROM --platform=$BUILDPLATFORM python:3.12-slim AS builder
```

> **Experiment:** Ändere das Dockerfile, baue neu für `linux/arm/v7` und beobachte
> den Unterschied in der Buildzeit.
>
> **Achtung:** Bei Paketen mit nativem C-Code (wie `pydantic`) kann das zu Fehlern führen,
> weil die Pakete für die falsche Architektur kompiliert werden.
> Mehr dazu im Abschnitt «Häufige Fehler» unten.

**6.2** Verfügbare Build-ARGs — füge diese Zeilen in dein Dockerfile ein und beobachte die Ausgabe:

```dockerfile
ARG TARGETARCH
ARG TARGETPLATFORM
RUN echo "Zielplattform: $TARGETPLATFORM, Architektur: $TARGETARCH"
```

---

## Häufige Fehler

| Fehler | Ursache | Lösung |
|---|---|---|
| `ModuleNotFoundError: pydantic_core._pydantic_core` | Pakete wurden für falsche Architektur kompiliert | `FROM --platform=$BUILDPLATFORM` entfernen |
| `context deadline exceeded` beim Builder | WSL2 Socket-Timeout | Builder neu erstellen mit `--driver-opt network=host` |
| `WARNING: requested image platform does not match` | Image läuft unter QEMU-Emulation | Normal — kein Fehler, nur ein Hinweis |
| `--load` schlägt fehl bei mehreren Plattformen | `--load` unterstützt nur eine Plattform | `--push` verwenden oder eine Plattform auswählen |

---

## Schritt 7 – Reflexion

Beantworte folgende Fragen:

1. Was ist der Unterschied zwischen `linux/arm/v7` und `linux/arm64`? Welche Raspberry-Pi-Modelle verwenden welche Architektur?
2. Warum dauert der Build für ARM länger als für amd64?
3. Was ist ein Manifest und welchen Vorteil bringt es gegenüber separaten Image-Tags?
4. Wann würdest du `--platform=$BUILDPLATFORM` verwenden — und wann nicht?

---

## Hilfestellungen

- `docker buildx ls` — zeigt alle vorhandenen Builder
- `docker buildx rm <name>` — löscht einen Builder
- `docker run --rm --platform linux/arm/v7 <image>` — erzwingt eine bestimmte Plattform beim Start
- `platform.machine()` in Python gibt die CPU-Architektur zurück
- Offizielle Doku: [docs.docker.com/build/building/multi-platform](https://docs.docker.com/build/building/multi-platform/)
