from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.Routes.metrics_routes import router as analyze_router
import uvicorn

app = FastAPI(title="Qualitas Quality Metrics API", version="1.0")

# === CORS Setup ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your React domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Routes ===
app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Qualitas Metrics API 🚀"}

if __name__ == "__main__":
    uvicorn.run("Backend.server:app", host="0.0.0.0", port=8000, reload=True)