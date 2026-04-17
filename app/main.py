from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Real Estate API",
    description="API for Real Estate System",
    version="1.0.0"
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