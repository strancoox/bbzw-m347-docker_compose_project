# Auftrag: Multi-Stage Builds
## Modul 347 – Dienst mit Container anwenden 

---

## Lernziele

Nach diesem Auftrag kannst du:
- erklären, warum naive Dockerfiles zu grosse Images erzeugen
- ein Dockerfile mit mehreren Stages schreiben
- die Layer-Reihenfolge cache-optimal gestalten
- eine einzelne Stage gezielt bauen und debuggen

---

## Zeitbedarf

ca. 45 Minuten

---

## Voraussetzungen

- Docker Desktop ist installiert und läuft
- Grundkenntnisse Dockerfile (`FROM`, `COPY`, `RUN`, `CMD`)
- Terminal / WSL geöffnet

---

## Ausgangslage

Du erhältst eine kleine FastAPI-Applikation mit folgendem Aufbau:

```
multistage/
├── Dockerfile         
├── requirements.txt
└── src/
    └── main.py
```

Das vorhandene `Dockerfile` funktioniert, hat aber zwei grosse Probleme:
1. Es ist **nicht cache-optimal** aufgebaut
2. Es verwendet **kein Multi-Stage Build** — Build-Tools landen im finalen Image

---

## Schritt 1 – Ausgangslage verstehen

**1.1** Baue das vorhandene Image und miss die Grösse:

```bash
docker build -t app-vorher .
docker images app-vorher
```

Notiere die Image-Grösse: _______ MB

**1.2** Schaue dir die Layer an:

```bash
docker history app-vorher
```

> **Frage:** Welche Layer findest du problematisch? Warum?

---

## Schritt 2 – Cache-Reihenfolge korrigieren

Öffne das `Dockerfile`. Du wirst feststellen, dass der Quellcode **vor** den Abhängigkeiten kopiert wird.

**2.1** Warum ist das ein Problem für den Build-Cache?

> **Tipp:** Überlege, was passiert wenn du eine Zeile in `main.py` änderst. Welche Layer werden neu gebaut?

**2.2** Korrigiere die Reihenfolge im `Dockerfile`:
- Zuerst nur `requirements.txt` kopieren
- Dann `pip install` ausführen
- Erst dann den restlichen Quellcode kopieren

**2.3** Baue erneut und ändere danach eine Kleinigkeit in `src/main.py` (z. B. den Begrüssungstext). Baue nochmals:

```bash
docker build -t app-cache .
# (Änderung in main.py vornehmen)
docker build -t app-cache .
```

> **Beobachtung:** Welche Schritte werden mit `CACHED` markiert?

---

## Schritt 3 – Multi-Stage Build einführen

Jetzt kommt der eigentliche Auftrag. Du erweiterst das Dockerfile um eine zweite Stage.

**3.1** Benenne die erste Stage:

```dockerfile
FROM python:3.12 AS builder
```

**3.2** Installiere die Abhängigkeiten im Builder mit `--user`:

```bash
pip install --user -r requirements.txt
```

> **Warum `--user`?** Damit die Pakete unter `/root/.local` landen und einfach in die nächste Stage kopiert werden können.

**3.3** Füge eine zweite Stage hinzu, die nur das Nötigste enthält:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**3.4** Baue das neue Image und vergleiche die Grösse:

```bash
docker build -t app-nachher .
docker images app-vorher app-nachher
```

Notiere die neue Grösse: _______ MB
Einsparung: _______ %

---

## Schritt 4 – App testen

**4.1** Starte den Container:

```bash
docker run --rm -p 8000:8000 app-nachher
```

**4.2** Öffne im Browser: [http://localhost:8000](http://localhost:8000)

Erwartete Ausgabe:
```json
{"message": "Hallo von der FastAPI-App!"}
```

**4.3** Prüfe, ob Build-Tools im finalen Image fehlen:

```bash
docker run --rm app-nachher pip --version
```

> Was beobachtest du? Warum ist das gut für die Sicherheit?

---

## Schritt 5 – Stage gezielt debuggen

Manchmal möchtest du nur eine bestimmte Stage bauen, um Fehler zu untersuchen.

**5.1** Baue nur die `builder`-Stage:

```bash
docker build --target builder -t app-debug .
```

**5.2** Steige in den Container ein:

```bash
docker run -it app-debug /bin/sh
```

**5.3** Untersuche die Umgebung:

```bash
pip list          # alle installierten Pakete sichtbar?
ls -la /build/    # was ist im Verzeichnis?
exit
```

> **Frage:** Welchen Nutzen hat `--target` beim Debugging?

---

## Schritt 6 – Reflexion

Beantworte folgende Fragen schriftlich (Lernjournal oder direkt hier):

1. Was ist der Hauptvorteil von Multi-Stage Builds gegenüber einem einstufigen Dockerfile?
2. Warum sollte `requirements.txt` vor dem Quellcode kopiert werden?
3. In welchen Projekten aus deinem Berufsalltag würdest du Multi-Stage Builds einsetzen?

---

## Hilfestellungen

- `docker history <image>` zeigt alle Layer mit Grösse
- `docker run -it <image> /bin/sh` öffnet eine Shell im Container
- `docker images` listet alle lokalen Images mit Grösse
- Offizielle Doku: [docs.docker.com/build/building/multi-stage](https://docs.docker.com/build/building/multi-stage/)
