"""FastAPI Application Entry Point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for model warm-up and DB connections."""
    configure_logging()
    logger.info("Starting DocIntel Platform Backend", version="1.0.0", env=settings.environment)
    yield
    logger.info("Shutting down DocIntel Platform Backend")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Multimodal Document Intelligence Platform with CV, Scikit-Learn, LangGraph, and FAISS RAG.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/healthz", tags=["Health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok", "app": "docintel"}
