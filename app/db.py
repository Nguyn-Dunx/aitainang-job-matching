"""Kết nối PostgreSQL + pgvector (SQLAlchemy 2.0)."""

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


# create_engine không mở kết nối ngay — an toàn để import trong test.
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: mỗi request một session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Tạo extension pgvector + toàn bộ bảng. T2/T3 sẽ chuyển sang Alembic nếu cần."""
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    from app import models  # noqa: F401  (đăng ký model trước khi create_all)

    Base.metadata.create_all(engine)
