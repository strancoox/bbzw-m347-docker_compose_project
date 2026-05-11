# Fragen – Integration der Services (DL10)

Name: <Nachname> <Vorname>
Klasse: <Klasse>

---

## 1. Services verstehen

Welche Services haben Sie in Ihrer `compose.yaml` definiert?

Antwort: 
- `api` 
- `db` 
- `adminer`
- `frontend`

---

Welche Aufgabe hat jeder Service in Ihrem System?

Antwort: 
- api - stellt die Schnittstelle fürs Backend bereit
- db - speichert die Daten in Postgress Datenbank
- adminer - nicht verstanden
- frontend - zeigt die Ausgabe des Services im Browser

---

## 2. Service-Kommunikation

Welchen Servicenamen verwendet die API, um die Datenbank zu erreichen?

Antwort: db

---

Warum funktioniert `localhost` innerhalb eines Containers nicht für die Kommunikation mit anderen Services?

Antwort: Localhost ist nur für Lokale Container und kann nicht mit anderen Services im Netzwerk kommunizieren

---

Wie stellt Docker Compose sicher, dass sich Services gegenseitig finden können?

Antwort: Durch ein Docker Netzwerk

---

## 3. Ports und Zugriff

Über welche Ports sind folgende Services erreichbar?

* API
* Adminer
* Frontend

Antwort:
api - 8000
adminer - 8000
frontend - 3000

---

Welcher Unterschied besteht zwischen:

* Container-Port
* Host-Port

Antwort:

---

## 4. Persistenz

Was passiert mit den Daten, wenn ein Container ohne Volume gelöscht wird?

Antwort: Die Daten werden nicht erhalten

---

Wie haben Sie die Persistenz für die Datenbank umgesetzt?

Antwort: Durch ein Volume, welches in der Datenbank liegt

---

Warum ist ein Volume für die Datenbank notwendig?

Antwort: Damit die Daten auch ohne den Contianer gespeichert werden und erhalten bleiben

---

## 5. Compose-Konfiguration

Welche Elemente haben Sie in Ihrer `compose.yaml` definiert?

Antwort: services, ports, images, environment, volumes, depends_on

---

Welche Umgebungsvariablen sind für die Datenbank-Verbindung notwendig?

Antwort: ${POSTGRES_DB}, ${POSTGRES_USER}, ${POSTGRES_PASSWORD}, 

---

Wofür wird `depends_on` verwendet?

Antwort: Damit wird die Reihenfolge, in welcher Docker die Services startet beeinflusst

---

## 6. Systemtest

Hat das System beim ersten Start vollständig funktioniert?

Antwort: Nein

---

Welche Probleme sind aufgetreten?

Antwort: Es gab keine Verbindung zur Datenbank und es gab keine Umgebungsvariablen

---

Wie haben Sie diese Probleme gelöst?

Antwort: Durch die Änderungen in Compose file

---

## 7. Verständnis

Beschreiben Sie kurz den Datenfluss in Ihrem System.

(Beispiel: Frontend → API → Datenbank)

Antwort: Frontend - API - Datenbank - Adminer - Datenbank

---

Was passiert beim Befehl:

```bash
docker compose down
```

Antwort: Container und Netzwerke werden gestoppt und enfernt 

---

## 8. Reflexion

Was war für Sie heute die wichtigste Erkenntnis?

Antwort: Der Aufbau einer compose Datei und die Funktion der Umgebungsvariablen

---

Was war schwierig oder noch unklar?

Antwort: Es selbst zu programmieren und ohne hilfe zu lösen
