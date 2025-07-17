"""Модуль конфигурации FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src import api_constants
from src.heroes.router import heroes_router

app = FastAPI(
    title="SuperHero API", swagger_ui_parameters={"operationsSorter": "method"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_constants.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=api_constants.CORS_METHODS,
)

app.include_router(heroes_router, prefix="/api/v1")


@app.get(
    "/",
    response_class=HTMLResponse,
)
def home():
    return """
    <html>
    <head><title>SuperHero API</title></head>
    <body>
    <h1>SuperHero API</h1>
    <ul>
    <li><a href="/docs">Документация Swagger</a></li>
    <li><a href="/redoc">Документация ReDoc</a></li>
    </ul>
    </body>
    </html>
    """
