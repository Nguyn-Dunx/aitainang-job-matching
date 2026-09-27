"""Entrypoint FastAPI — điều phối pipeline 5 tầng (skeleton T1)."""

from fastapi import FastAPI

from app.routers import cv, health

app = FastAPI(
    title="aitainang API",
    version="0.1.0",
    description="Trợ lý nghề nghiệp cá nhân hóa: chấm độ khớp CV–JD, giải thích, gợi ý sửa CV.",
)

app.include_router(health.router)
app.include_router(cv.router)
