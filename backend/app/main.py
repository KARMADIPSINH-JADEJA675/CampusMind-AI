from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router
from app.routes.campus import router as campus_router


app = FastAPI(
    title="CampusMind AI",
    description="Intelligent Campus Assistant using Generative AI and MCP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(campus_router)


@app.get("/")
async def root():
    return {
        "name": "CampusMind AI",
        "status": "running",
        "message": "Intelligent Campus Assistant API",
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "CampusMind AI Backend",
    }