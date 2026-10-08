from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import router as sources_router

# Создание таблиц БД при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CCTV Management System API",
    version="1.0.0",
    description="API для управления источниками видеопотока"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sources_router)