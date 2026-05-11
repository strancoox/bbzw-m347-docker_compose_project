import platform
from fastapi import FastAPI

app = FastAPI(title="Multi-Arch Demo – Raspberry Pi")

@app.get("/")
def root():
    return {
        "message": "Hallo vom Multi-Arch-Container!",
        "architecture": platform.machine(),   # aarch64 / armv7l / x86_64
        "system":       platform.system(),
        "python":       platform.python_version(),
    }

@app.get("/health")
def health():
    return {"status": "ok"}
