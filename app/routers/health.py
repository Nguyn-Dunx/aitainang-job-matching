"""Health-check — T4 dùng cho deploy (Render/Railway/Compose healthcheck)."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}
