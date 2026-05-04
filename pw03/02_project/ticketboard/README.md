# Konfiguration und Umgebungsvariablen

## Ziel

In diesem Auftrag bereinigen Sie die Konfiguration des TicketBoard-Systems.

Sie lernen dabei:

* warum Passwörter und Konfigurationswerte **nicht im Code** stehen dürfen
* wie **Umgebungsvariablen** und `.env`-Dateien sauber eingesetzt werden
* wie Compose-Variablen substituiert werden (`${VARIABLE}`)
* wie `.gitignore` und `.env.example` zusammenspielen

---

## Hinweise

* Arbeiten Sie strukturiert – eine Aufgabe nach der anderen
* Testen Sie nach jeder Änderung mit `docker compose up --build`
* Das Ziel ist das Verstehen der Zusammenhänge, nicht nur das Ergebnis

---

## Ausgangslage

Alex hat die API erweitert: Sie verbindet sich nun mit der Datenbank.

**Neu in dieser Version:**
- Datenbankverbindung via SQLAlchemy
- Endpunkt `/db-check` prüft die Verbindung

**Problem:** Die Zugangsdaten und Konfigurationswerte stehen aktuell **hardcoded** – sowohl in `compose.yml` als auch in `app/main.py`. Das ist unsicher und nicht wiederverwendbar.

**Deine Aufgabe:** Führe eine saubere Konfiguration mit `.env` ein.

---

## Abgabe / Nachweis

Am Ende dieser Woche sollte:

* das System mit **einem Befehl startbar** sein
* `/db-check` die Datenbankverbindung bestätigen
* **kein einziges Passwort** im Code oder in `compose.yml` stehen
* folgende Dokumentation vorhanden sein:

```
docs/
├── statusbericht-woche3.md
└── questions.md (Fragen beantwortet)
```

---

## Arbeitsauftrag

Bearbeiten Sie den Auftrag in Ihrem eigenen Repository:

```bash
cp -rf ticketboard ~/bbzw/bbzw-m347-<klasse>_<nachname>_<vorname>/pw03/02_project/
```

---

### 1. Ausgangslage analysieren

Öffnen Sie folgende Dateien und identifizieren Sie alle **hardcodierten Werte**:

* `compose.yml`
* `app/main.py`

Notieren Sie: Welche Werte sind Konfiguration und sollten in `.env`?

---

### 2. `.env` verwenden

Eine `.env`-Datei ist bereits vorhanden. Öffnen Sie diese und prüfen Sie den Inhalt.

Erweitern Sie die Datei falls nötig – sie soll alle Konfigurationswerte enthalten, die aktuell hardcoded sind.

---

### 3. `.gitignore` erstellen

Erstellen Sie im Projektordner eine Datei `.gitignore`:

```
.env
__pycache__/
*.pyc
.venv/
```

> Warum ist dieser Schritt kritisch? Das Git-Repository speichert **jeden Commit dauerhaft** –
> ein einmal hochgeladenes Passwort bleibt für immer im Verlauf sichtbar.

---

### 4. `.env.example` prüfen

Eine `.env.example`-Datei ist bereits vorhanden. Prüfen Sie:

* Enthält sie **alle** Schlüssel aus `.env`?
* Enthält sie **keine** echten Passwörter?

Diese Datei wird ins Git eingecheckt und zeigt anderen Entwicklern, welche Variablen benötigt werden.

---

### 5. `compose.yml` auf Variablen umstellen

Ersetzen Sie alle hardcodierten Werte in `compose.yml` durch Variablen aus `.env`.

Docker Compose liest `.env` automatisch und ersetzt `${VARIABLE_NAME}` im YAML.

**Ziel für den api-Service:**

```yaml
environment:
  DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

**Ziel für den db-Service:**

```yaml
environment:
  POSTGRES_DB: ${POSTGRES_DB}
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

Überprüfen Sie das Ergebnis mit:

```bash
docker compose config
```

Dieser Befehl zeigt die fertig aufgelöste Compose-Konfiguration – alle `${VARIABLE}` sollten durch echte Werte ersetzt sein.

---

### 6. `app/main.py` anpassen

Ersetzen Sie die hardcodierte `DATABASE_URL` in `main.py` durch einen Umgebungsvariablen-Aufruf:

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL")
```

Der Container erhält den Wert zur Laufzeit über `compose.yml`.

---

### 7. System starten und testen

```bash
docker compose up --build
```

Testen Sie folgende Endpunkte im Browser:

| Endpunkt | URL | Erwartetes Ergebnis |
|----------|-----|---------------------|
| Health | http://localhost:8000/health | `{"status": "ok"}` |
| DB-Check | http://localhost:8000/db-check | `{"db": "connected"}` |
| Adminer | http://localhost:8080 | Weboberfläche sichtbar |
| Frontend | http://localhost:3000 | Weboberfläche sichtbar |

---

### 8. Systemtest mit Neustart

1. System stoppen: `docker compose down`
2. System neu starten: `docker compose up --build`
3. Endpunkte erneut prüfen – alles sollte weiterhin funktionieren

---

## Statusbericht

Erstellen Sie:

```
docs/statusbericht-woche3.md
```

Inhalt:
* umgesetzte Arbeiten
* aktueller Stand
* Probleme
* nächste Schritte

---

## Fragen

Beantworten Sie die Fragen in:

```
docs/questions.md
```
