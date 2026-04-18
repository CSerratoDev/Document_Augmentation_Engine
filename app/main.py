from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DataDolphin API",
    description="API for Data Dolphin, system for orquestation documents.This project is an advanced document orchestration system designed to transform physical or digital administrative processes into highly efficient paperless workflows. The agent leverages multimodal AI to reverse-engineern-page documents, identifying missing fields and automating the data injection process.",
    version="2.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173" #agregar la direccion de la nube
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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(documents_router)
app.include_router(companies_router)