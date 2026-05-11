from fastapi import FastAPI

app = FastAPI(title="Multi-Stage Demo")

@app.get("/")
def root():
    return {"message": "Hallo von der FastAPI-App!"}

@app.get("/health")
def health():
    return {"status": "ok"}
