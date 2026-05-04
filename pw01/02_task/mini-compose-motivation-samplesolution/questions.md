# Fragen – Mini Compose Motivation (Musterlösung)

Name: <Nachname> <Vorname>  
Klasse: <Klasse>

---

## 1. Services verstehen

Welche Services sind in `compose.yaml` definiert?

Antwort:  
Die definierten Services sind `web`, `api` und `admin`.

---

Welcher Service verwendet ein fertiges Image (`image`)?

Antwort:  
Die Services `web` und `admin` verwenden ein fertiges Image (`nginx:alpine`).

---

Welcher Service wird aus einem Dockerfile gebaut (`build`)?

Antwort:  
Der Service `api` wird aus einem Dockerfile gebaut.

---

## 2. Ports und Zugriff

Über welchen Host-Port ist der Web-Service **zu Beginn** erreichbar?

Antwort:  
Der Web-Service ist zu Beginn über den Port `8080` erreichbar.

---

Welchen Port verwendet der API-Service?

Antwort:  
Der API-Service verwendet den Port `5001`.

---

Auf welchen Port haben Sie den Web-Service geändert?

Antwort:  
Der Web-Service wurde auf den Port `8000` geändert.

---

## 3. Verständnis Docker Compose

Warum ist Docker Compose in diesem Beispiel sinnvoll?

Antwort:  
Docker Compose ist sinnvoll, weil mehrere Services in einer einzigen Datei beschrieben und mit einem einzigen Befehl gestartet werden können. Dadurch wird das System übersichtlicher und einfacher reproduzierbar.

---

Was ist der Unterschied zwischen `image` und `build`?

Antwort:  
`image` bedeutet, dass ein fertiges Image verwendet wird (z. B. aus Docker Hub).  
`build` bedeutet, dass Docker aus einem Dockerfile ein eigenes Image erstellt.

---

Was macht der Befehl `docker compose up --build`?

Antwort:  
Der Befehl baut die Images neu und startet anschliessend alle definierten Services.

---

## 4. Fehleranalyse

Startete das System beim ersten Versuch vollständig?

Antwort:  
Nein, das System startete beim ersten Versuch nicht vollständig.

---

Welcher Service hatte ein Problem?

Antwort:  
Der Service `api` hatte ein Problem.

---

Was war die Ursache für das Problem?

Antwort:  
Der Build-Kontext war falsch gesetzt (`build: .` statt `build: ./api`), wodurch das Dockerfile nicht gefunden wurde.

---

Wie haben Sie das Problem gelöst?

Antwort:  
Der Build-Kontext wurde auf den richtigen Ordner angepasst (`build: ./api`).

---

## 5. Docker Compose CLI

Was ist der Unterschied zwischen:

- `docker compose stop`  
- `docker compose pause`  

Antwort:  
`stop` beendet den Container vollständig.  
`pause` friert den Container ein, er bleibt im Speicher, führt aber keine Prozesse aus.

---

Was zeigt der Befehl `docker compose logs` an?

Antwort:  
Der Befehl zeigt die Log-Ausgaben aller Container an, z. B. Fehlermeldungen oder Statusmeldungen.

---

Was zeigt der Befehl `docker compose ps` an?

Antwort:  
Der Befehl zeigt den aktuellen Status der Container, z. B. ob sie laufen und welche Ports verwendet werden.

---

## 6. Reflexion

Was war für Sie heute neu oder besonders wichtig?

Antwort:  
Wichtig war zu verstehen, wie mehrere Container gemeinsam gestartet werden und wie ein Compose-File aufgebaut ist.

---

Was ist noch unklar oder möchten Sie noch besser verstehen?

Antwort:  
Beispiel: Wie Container untereinander kommunizieren und wie Daten dauerhaft gespeichert werden (Volumes).