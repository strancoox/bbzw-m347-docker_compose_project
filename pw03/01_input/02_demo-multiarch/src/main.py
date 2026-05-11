import platform
from fastapi import FastAPI

app = FastAPI(title="Multi-Arch Demo")

@app.get("/")
def root():
    return {
        "message": "Hallo vom Multi-Arch-Container!",
        "architecture": platform.machine(),   # zeigt arm64 oder x86_64
        "system":       platform.system(),
        "python":       platform.python_version(),
    }

@app.get("/health")
def health():
    return {"status": "ok"}
