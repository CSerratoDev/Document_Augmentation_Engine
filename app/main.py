import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DataDolphin API",
    description="API for Data Dolphin, system for orquestation documents.This project is an advanced document orchestration system designed to transform physical or digital administrative processes into highly efficient paperless workflows. The agent leverages multimodal AI to reverse-engineern-page documents, identifying missing fields and automating the data injection process.",
    version="2.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers.user_router import router as user_router
from app.routers.documents_router import router as documents_router
from app.routers.companies_router import router as companies_router
from app.routers.auth_router import router as auth_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(documents_router)
app.include_router(companies_router)