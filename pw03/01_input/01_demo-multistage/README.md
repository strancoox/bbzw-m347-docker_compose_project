# Demo: Multi-Stage Builds
## M347 – Dienst mit Container anwenden

---

## Projektstruktur

```
01_demo-multistage/
├── Dockerfile.naive      ← Ohne Multi-Stage (~1 GB)
├── Dockerfile.multi      ← Mit Multi-Stage (~180 MB)
├── requirements.txt      ← Python-Abhängigkeiten
├── src/
│   └── main.py           ← FastAPI-App
└── README.md
```

---

## Schritt 1 – Projekt-Verzeichnis öffnen

```bash
cd 01_demo-multistage
```

---

## Schritt 2 – Naives Image bauen & Grösse messen

```bash
docker build -f Dockerfile.naive -t app-naive .
docker images app-naive
```

**Erwartetes Resultat:** Image ~1 GB

---

## Schritt 3 – Multi-Stage Image bauen & Grösse messen

```bash
docker build -f Dockerfile.multi -t app-multi .
docker images app-multi
```

**Erwartetes Resultat:** Image ~180 MB

---

## Schritt 4 – Layer vergleichen

```bash
docker history app-naive
docker history app-multi
```

Beobachte: Das Multi-Stage-Image hat deutlich weniger und kleinere Layer.

---

## Schritt 5 – Stage debuggen (in builder-Stage einsteigen)

```bash
docker build --target builder -f Dockerfile.multi -t app-debug .
docker run -it app-debug /bin/sh
```

Im Container kannst du jetzt die Build-Umgebung untersuchen:
```bash
pip list          # alle installierten Pakete sichtbar
ls -la /build/    # Verzeichnisinhalt prüfen
exit
```

---

## App starten (optional)

```bash
docker run -p 8000:8000 app-multi
# → http://localhost:8000
```
