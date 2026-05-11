# Musterlösungen – Integration der Services (DL10)

---

## 1. Services verstehen

Welche Services haben Sie in Ihrer `compose.yaml` definiert?

Antwort:
api, db, adminer, frontend

---

Welche Aufgabe hat jeder Service in Ihrem System?

Antwort:

* api: stellt die Anwendungsschnittstelle (Backend) bereit
* db: speichert die Daten in einer PostgreSQL-Datenbank
* adminer: ermöglicht den Zugriff auf die Datenbank über ein Webinterface
* frontend: stellt die Benutzeroberfläche dar

---

## 2. Service-Kommunikation

Welchen Servicenamen verwendet die API, um die Datenbank zu erreichen?

Antwort:
Den Servicenamen der Datenbank, z. B. `db`

---

Warum funktioniert `localhost` innerhalb eines Containers nicht für die Kommunikation mit anderen Services?

Antwort:
Weil `localhost` immer auf den eigenen Container zeigt und nicht auf andere Container im Netzwerk

---

Wie stellt Docker Compose sicher, dass sich Services gegenseitig finden können?

Antwort:
Durch ein gemeinsames Netzwerk mit automatischer DNS-Auflösung über Servicenamen

---

## 3. Ports und Zugriff

Über welche Ports sind folgende Services erreichbar?

* API
* Adminer
* Frontend

Antwort:
(z. B. abhängig von Lösung)

* API: 8000
* Adminer: 8080
* Frontend: 3000

---

Welcher Unterschied besteht zwischen:

* Container-Port
* Host-Port

Antwort:

* Container-Port: Port innerhalb des Containers
* Host-Port: Port auf dem lokalen Rechner, über den der Container erreichbar ist

---

## 4. Persistenz

Was passiert mit den Daten, wenn ein Container ohne Volume gelöscht wird?

Antwort:
Die Daten gehen verloren

---

Wie haben Sie die Persistenz für die Datenbank umgesetzt?

Antwort:
Durch ein Docker-Volume, das mit dem Datenbank-Container verbunden ist

---

Warum ist ein Volume für die Datenbank notwendig?

Antwort:
Damit Daten unabhängig vom Container gespeichert werden und nach einem Neustart erhalten bleiben

---

## 5. Compose-Konfiguration

Welche Elemente haben Sie in Ihrer `compose.yaml` definiert?

Antwort:
services, ports, environment, volumes, depends_on

---

Welche Umgebungsvariablen sind für die Datenbank-Verbindung notwendig?

Antwort: 
z. B.:
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

---

Wofür wird `depends_on` verwendet?

Antwort:
Um die Startreihenfolge von Services zu definieren

---

## 6. Systemtest

Hat das System beim ersten Start vollständig funktioniert?

Antwort:
Nein

---

Welche Probleme sind aufgetreten?

Antwort:
z. B.:

* keine Verbindung zur Datenbank
* falscher Host (localhost statt db)
* fehlende Umgebungsvariablen

---

Wie haben Sie diese Probleme gelöst?

Antwort:
Durch Anpassung der Compose-Konfiguration (Host, ENV, Volumes) und erneutes Testen

---

## 7. Verständnis

Beschreiben Sie kurz den Datenfluss in Ihrem System.

(Beispiel: Frontend → API → Datenbank)

Antwort:
Frontend → API → Datenbank
Adminer → Datenbank

---

Was passiert beim Befehl:

```bash
docker compose down
```

Antwort:
Alle Container werden gestoppt und entfernt, Netzwerke ebenfalls; Volumes bleiben bestehen (sofern nicht explizit gelöscht)

---

## 8. Reflexion

Was war für Sie heute die wichtigste Erkenntnis?

Antwort:
Dass Container über Servicenamen kommunizieren und nicht über localhost

---

Was war schwierig oder noch unklar?

Antwort:
Individuell (z. B. Netzwerkverständnis, Volumes, ENV-Konfiguration)
