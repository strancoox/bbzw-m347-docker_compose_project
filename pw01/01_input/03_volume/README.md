# Volumes and persistence

## Goal
Understand how data can survive outside of a container.

This step shows:
- what happens without a volume
- how a bind mount works
- how a named volume works

## Important note

Running the container **without a volume** is the same idea as in `02_single_container`.

In this step:
- the application code is stored in `/app`
- the data is stored in `/data/counter.txt`

This makes volume usage cleaner and easier to understand.

---

## Build the image

```bash
docker build -t demo-app .
````

---

## 1. Run without a volume

```bash
docker run -p 8000:5001 demo-app
```

Open in browser:

`http://localhost:8000`

### Observation

* the counter increases
* the file is stored inside the container
* if you remove the container, the data is gone

---

## 2. Run with a bind mount

A bind mount connects a real folder from the host into the container.

First create a local folder:

```bash
mkdir -p data
```

Then run:

```bash
docker run -p 8000:5001 -v "$(pwd)/data:/data" demo-app
```

### What this means

* `$(pwd)/data` = local folder on your host
* `/data` = folder inside the container

### Observation

* the counter increases
* `counter.txt` appears in your local `data` folder
* if you remove the container and start it again, the data is still there

### Advantage

* you can directly see the files on the host

### Disadvantage

* the container depends on this host path

---

## 3. Run with a named volume

A named volume is managed by Docker.

```bash
docker run -p 8000:5001 -v counter_data:/data demo-app
```

### What this means

* `counter_data` is the name of the volume
* Docker manages the storage location
* the container uses this volume at `/data`

### Observation

* the counter increases
* if you remove the container, the data is still kept in the volume
* a new container can use the same volume again

### Advantage

* good for persistent data
* common for databases

### Key idea

The container can be removed, but the volume remains.

---

## Open in browser

`http://localhost:8000`

---

## Summary

### Without volume

* simple
* data is lost when the container is removed

### Bind mount

* data is visible on the host
* useful for development
* depends on a host path

### Named volume

* managed by Docker
* data survives container removal
* good for persistent container data

---

## Cleanup examples

Remove container:

```bash
docker ps
docker rm -f <container_name_or_id>
```

Remove named volume:

```bash
docker volume rm counter_data
```
