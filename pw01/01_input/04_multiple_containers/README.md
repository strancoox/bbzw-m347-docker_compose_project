# Run multiple containers manually

## Goal
Run an application that depends on a second container.

This step shows:
- how two containers can work together
- how containers communicate over a Docker network
- that multi-container setups require more manual coordination

## Scenario

The web application no longer stores the counter in a local file.

Instead, it uses Redis (key-value database) as a separate service.

So we now need:
- one container for the web app
- one container for Redis

## Important idea

Both containers must:
- run at the same time
- be connected to the same network
- use the correct names

## 1. Create a network

```bash
docker network create demo-network
````

## 2. Start Redis

```bash
docker run -d --name redis --network demo-network redis:7-alpine
```

## 3. Build the web image

```bash
docker build -t demo-web .
```

## 4. Start the web container

```bash
docker run -d --name web --network demo-network -p 8000:5001 demo-web
```

## 5. Open in browser

`http://localhost:8000`

## Key idea

A multi-container setup is possible without extra tooling.

But it becomes more complex:

* more commands
* more coordination
* more room for mistakes

## Cleanup

Remove the containers:

```bash
docker rm -f web redis
```

Remove the network:

```bash
docker network rm demo-network
```

## Next step

In the next step, the whole multi-container setup will be described in a single file and started together.
