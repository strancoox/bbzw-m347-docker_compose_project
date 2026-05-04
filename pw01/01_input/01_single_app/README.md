# Run the App locally (without Docker)

## Goal
Run the application locally using Python.

This step shows:
- how the application works without Docker
- that Docker is not required to understand the app
- the starting point before containerization

## Setup virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
````

## Install dependencies

No external dependencies are required for this step.

## Run the application

```bash
python3 app.py
```

## Open in browser

[http://localhost:5001](http://localhost:5001)

## What you should see

* A simple webpage with a button
* Clicking the button increases a counter

## Important observation

* The counter is stored in memory
* If you stop and restart the app, the counter resets
