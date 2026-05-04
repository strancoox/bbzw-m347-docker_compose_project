# Run the system with Docker Compose

## Goal
Run a multi-container application in a simpler and more structured way.

This step shows:
- how to define multiple services in one file
- how to start the whole system with one command
- how Docker Compose makes multi-container setups easier

## Scenario

This is the same basic system as in the previous step:
- one web application
- one Redis service

The difference is how the system is started and managed.

## Why this step?

In the previous step, the setup worked, but it required several manual commands:
- create a network
- start Redis
- build the web image
- start the web container

Now the whole setup is described in one file.

## Services in this step

- `web` = Python web application
- `redis` = Redis service

## Start the system

```bash
docker compose up --build
````

## Open in browser

`http://localhost:8000`

## What you should see

* a simple webpage with a button
* each click increases the counter
* the value is stored in Redis

## Important observation

This step uses the same idea as before:

* multiple containers
* one application depends on another service

But now the setup is easier to manage because:

* the services are defined in one file
* the system is started with one command
* the configuration is easier to read and reproduce

## Stop the system

```bash
docker compose down
```

## Compose file

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5001"

  redis:
    image: redis:7-alpine
````

### Line by line

#### `services:`

This is the top-level section of the file.

It tells Docker that the following entries are services that belong to the same application.

---

#### `web:`

This defines the first service.

`web` is the name of the web application service.

This name is also important for the internal setup of the system.

---

#### `build: .`

This tells Docker to build the image for the `web` service from the current folder.

The current folder contains:

* the `Dockerfile`
* the application code
* the requirements file

So Docker can build the web application image directly from this directory.

---

#### `ports:`

This section defines port mapping between the host and the container.

It makes the web application reachable from outside the container.

---

#### `- "8000:5001"`

This means:

* `8000` = port on the host
* `5001` = port inside the container

So when you open `http://localhost:8000` in the browser, the request is forwarded to port `5001` inside the `web` container.

---

#### `redis:`

This defines the second service.

`redis` is the name of the Redis service.

This name is important because the web application uses `redis` as the hostname when connecting to Redis.

---

#### `image: redis:7-alpine`

This tells Docker to use the official Redis image.

* `redis` = image name
* `7-alpine` = image tag

So Docker does not need to build this service from a Dockerfile.
It can pull the ready-made image and start it directly.

### Why is there no network section?

In the previous step, the network had to be created manually.

Here, this is no longer necessary.

Docker automatically creates an internal default network for all services in the same Compose project.

That means:

* `web` and `redis` are automatically connected
* the `web` service can reach Redis using the hostname `redis`
* no extra `docker network create ...` command is needed
