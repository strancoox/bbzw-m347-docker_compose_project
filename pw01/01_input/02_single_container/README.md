# Single Container (In-Memory Counter)

## Goal
Run a simple web application inside a single Docker container.

This step shows:
- how to build a Docker image
- how to run a container
- that data inside a container is not persistent

## How it works
The application is a small Python web server.

It stores a counter **in memory** (inside the running process).

Every time you click the button, the counter increases.

## Build the image

```bash
docker build -t demo-app .
````

## Run the container

```bash
docker run -p 8000:5001 demo-app
```

## Open in browser

```
http://localhost:8000
```

## Important observation

* The counter increases while the container is running
* If you stop and restart the container, the counter resets
