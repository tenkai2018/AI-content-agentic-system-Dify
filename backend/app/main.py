"""
FastAPI Application Entry Point
AI Content Agentic System — Backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import router
from app.db.models import Base
from app.db.session import engine

settings = get_settings()

# ==============================================================================
# FastAPI App
# ==============================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "System Logging API cho Content Machine. "
        "Lưu trữ và giám sát các hoạt động từ Dify, n8n và Frontend."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ==============================================================================
# CORS Middleware
# Cho phép Next.js frontend (localhost:3000) gọi API
# ==============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Register Routers
# ==============================================================================

app.include_router(router)


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)


# ==============================================================================
# Root Endpoint
# ==============================================================================

@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health",
    }
