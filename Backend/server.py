from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.Routes.metrics_routes import router as analyze_router
import uvicorn
import os
from typing import List

# Attempt to load .env from the Backend directory if python-dotenv is installed.
# This is optional; if python-dotenv is not available the code will fall back
# to environment variables already set in the system.
try:
    # Use dynamic import to avoid static import errors when python-dotenv
    # is not installed in the environment (keeps linters quiet).
    import importlib

    _dotenv = importlib.import_module("dotenv")
    _load = getattr(_dotenv, "load_dotenv", None)
    if callable(_load):
        _env_path = os.path.join(os.path.dirname(__file__), ".env")
        _load(dotenv_path=_env_path)
except Exception:
    # If python-dotenv isn't available, continue using values from os.environ.
    pass

app = FastAPI(title="Qualitas Quality Metrics API", version="1.0")

# === CORS Setup ===
# Allow origins can be configured with the CORS_ALLOW_ORIGINS env var as a
# comma-separated list. If not provided, default to allow all origins ("*").
_allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS")
if _allow_origins_env:
    # split by comma and strip whitespace
    allow_origins: List[str] = [o.strip() for o in _allow_origins_env.split(",") if o.strip()]
else:
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Routes ===
app.include_router(analyze_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to Qualitas Metrics API"}


if __name__ == "__main__":
    # Read host and port from env with sensible defaults.
    _host = os.getenv("HOST", "0.0.0.0")
    try:
        _port = int(os.getenv("PORT", "8000"))
    except ValueError:
        _port = 8000

    # Allow enabling reload via env var (useful in development).
    _reload = os.getenv("RELOAD", "true").lower() in ("1", "true", "yes")

    uvicorn.run("Backend.server:app", host=_host, port=_port, reload=_reload)