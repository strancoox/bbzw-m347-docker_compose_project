# Musterlösungen – Konfiguration und Umgebungsvariablen (DL11)

---

## 1. Konfiguration

Welche Werte sind aktuell hardcoded in `compose.yml` und `app/main.py`?

Antwort:
In `compose.yml`:
- `DATABASE_URL` (vollständige Verbindungszeichenfolge mit Passwort)
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

In `app/main.py`:
- `DATABASE_URL = "postgresql://ticketuser:secret@db:5432/ticketdb"` direkt als String

---

Warum ist es ein Problem, Passwörter direkt in `compose.yml` einzutragen?

Antwort:
`compose.yml` wird ins Git-Repository eingecheckt und ist für alle Personen mit Repository-Zugriff sichtbar. Das Git-Verlauf ist permanent – ein einmal hochgeladenes Passwort bleibt auch nach späterem Löschen in der History auffindbar. Ausserdem sind hardcodierte Passwörter nicht wiederverwendbar: Für jede Umgebung (Entwicklung, Produktion) müsste die Datei manuell angepasst werden.

---

Was ist der Unterschied zwischen `.env` und `.env.example`?

Antwort:
- `.env`: enthält **echte Werte** (Passwörter, Zugangsdaten). Wird **nicht** ins Git eingecheckt.
- `.env.example`: enthält nur die **Schlüsselnamen** ohne echte Werte (z. B. `POSTGRES_PASSWORD=changeme`). Wird ins Git eingecheckt und dient anderen Entwicklerinnen als Vorlage, welche Variablen benötigt werden.

---

Warum muss `.env` in `.gitignore` eingetragen sein?

Antwort:
Damit Git die Datei vollständig ignoriert und sie nicht ins Repository hochgeladen wird. Denke daran, der Git-Verlauf ist permanent ersichtlich! Auch nach späterem Entfernen der Datei noch in der History vorhanden und können wiederhergestellt werden. Die `.gitignore` ist die einzige zuverlässige Schutzebene gegen versehentliches Committen.

---

## 2. Variablen in Compose

Wie referenziert man eine Variable aus `.env` in `compose.yml`?

Antwort:
Mit der Syntax `${VARIABLE_NAME}`. Docker Compose liest die `.env`-Datei automatisch beim Start und ersetzt alle Platzhalter durch die entsprechenden Werte.

Beispiel:
```yaml
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

---

Was passiert, wenn eine Variable in `.env` fehlt, aber in `compose.yml` verwendet wird?

Antwort:
Docker Compose gibt eine Warnung aus und setzt den Wert als leeren String. Der Container startet möglicherweise trotzdem, verhält sich aber falsch – z. B. schlägt die Datenbankverbindung fehl, weil `DATABASE_URL` unvollständig ist. Mit `docker compose config` lässt sich prüfen, ob alle Variablen korrekt aufgelöst wurden.

---

Was zeigt der Befehl `docker compose config`? Wann ist er nützlich?

Antwort:
Der Befehl gibt die vollständig aufgelöste Compose-Konfiguration aus – alle `${VARIABLE}`-Platzhalter sind durch die echten Werte aus `.env` ersetzt. Er ist nützlich zur Überprüfung vor dem Start: Man sieht sofort, ob alle Variablen korrekt substituiert werden oder ob Werte fehlen.

---

## 3. Dockerfile und Build

Warum wird `requirements.txt` in einem eigenen `COPY`-Schritt vor dem App-Code kopiert?

Antwort:
Wegen des Docker **Layer-Cache**. Docker speichert jeden Schritt als eigenen Layer. Da sich `requirements.txt` selten ändert, muss `pip install` nur neu ausgeführt werden, wenn sich die Abhängigkeiten tatsächlich ändern. Ändert sich nur der App-Code, wird der `pip install`-Layer aus dem Cache verwendet – der Build ist dadurch deutlich schneller.

```dockerfile
COPY app/requirements.txt .          # ← nur bei Abhängigkeitsänderung neu
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app                         # ← bei jedem Code-Change neu
```

---

Was bewirkt `.dockerignore`? Welche Dateien sollten darin stehen?

Antwort:
`.dockerignore` definiert Dateien und Ordner, die beim `docker build` **nicht** in den Build-Kontext übertragen werden. Das verkleinert das Image und verhindert, dass sensible Dateien versehentlich ins Image gelangen.

Typische Einträge:
```
.env
.git
__pycache__/
*.pyc
.venv/
.pytest_cache/
```

Besonders wichtig: `.env` gehört hier rein, damit Passwörter nicht im Image landen – auch wenn `.gitignore` die Datei aus Git fernhält.

---

## 4. Systemtest

Funktioniert `/db-check` nach Ihrer Konfigurationsanpassung?

Antwort:
Ja – nach korrekter Konfiguration liefert der Endpunkt:
```json
{"db": "connected"}
```

---

Was zeigt der Endpunkt `/db-check` an, wenn die Verbindung funktioniert?

Antwort:
```json
{"db": "connected"}
```

Bei einem Fehler (z. B. falsche Zugangsdaten oder nicht erreichbare DB):
```json
{"db": "error", "detail": "...Fehlermeldung..."}
```

---

## 5. Reflexion

Was war der wichtigste Schritt in dieser Woche?

Antwort:
Das Einführen von `.env` und das Verständnis, dass **Konfiguration vom Code getrennt** gehört. Passwörter und Verbindungsparameter sind keine Code-Konstanten, sondern Umgebungsabhängigkeiten. Dieses Prinzip (bekannt als «12-Factor App – Config») ist in jedem professionellen Projekt Standard.

---

Was ist noch unklar oder möchten Sie besser verstehen?

Antwort:
Individuell – mögliche Themen: Wie werden `.env`-Dateien in Produktionssystemen verwaltet? Was sind Alternativen zu `.env` (z. B. Secrets Manager, Vault)?
