# Fragen – Mini Compose Motivation

Name: Stranc Aleksander  
Klasse: INA24BL

---

## 1. Services verstehen

Welche Services sind in `compose.yaml` definiert?

Antwort: admin, web und web
  

---

Welcher Service verwendet ein fertiges Image (`image`)?

Antwort: web und admin
  

---

Welcher Service wird aus einem Dockerfile gebaut (`build`)?

Antwort: api 
  

---

## 2. Ports und Zugriff

Über welchen Host-Port ist der Web-Service **zu Beginn** erreichbar?

Antwort: 8080  
  

---

Welchen Port verwendet der API-Service?

Antwort: 5000 
  

---

Auf welchen Port haben Sie den Web-Service geändert?

Antwort: 8000
  

---

## 3. Verständnis Docker Compose

Warum ist Docker Compose in diesem Beispiel sinnvoll?

Antwort: Weil man so viel schneller mehrere Services aktivieren kann 
  

---

Was ist der Unterschied zwischen `image` und `build`?

Antwort: 

Image: Ein fertiges Image wird aus einer Quelle verwendet

Build: Ein Image wird im Dockerfile erstellt
  

---

Was macht der Befehl `docker compose up --build`?

Antwort: Startet die Services und führt das 'build' aus 
  

---

## 4. Fehleranalyse

Startete das System beim ersten Versuch vollständig?

Antwort: Nein 
  

---

Welcher Service hatte ein Problem?

Antwort: Der 'API' Service hatte ein Problem 
  

---

Was war die Ursache für das Problem?

Antwort: Der Build kontext war falsch. Der Pfad zum Dockerfile war nicht korrekt. 
  

---

Wie haben Sie das Problem gelöst?

Antwort: Richtigen Pfad angegeben ./api 
  

---

## 5. Docker Compose CLI

Was ist der Unterschied zwischen:

- `docker compose stop` stoppt die Container und Services nicht mehr erreichbar

- `docker compose pause` pausiert die Services und setzt die Services in ein Timeout 
  

---

Was zeigt der Befehl `docker compose logs` an?

Antwort: Der Befehl zeigt die Log-Ausgaben aller Container  
  

---

Was zeigt der Befehl `docker compose ps` an?

Antwort: Es zeigt den Status der Container an und welche Ports verwendet werden
  

---

## 6. Reflexion

Was war für Sie heute neu oder besonders wichtig?

Antwort: alles
  

---

Was ist noch unklar oder möchten Sie noch besser verstehen?

Antwort:  
  