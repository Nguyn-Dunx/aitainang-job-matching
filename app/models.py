"""Schema DB ban đầu: CV, JD, kết quả matching.

Embedding dim = 1024: khớp BGE-M3 và multilingual-e5-large (chốt model ở T3).
"""

import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

EMBEDDING_DIM = 1024


class CV(Base):
    __tablename__ = "cvs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(Text, default="")  # Tầng 1: parsing
    parsed: Mapped[dict] = mapped_column(JSONB, default=dict)  # Tầng 2: extraction có schema
    embedding = mapped_column(Vector(EMBEDDING_DIM), nullable=True)  # Tầng 3
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    matches: Mapped[list["MatchResult"]] = relationship(
        back_populates="cv", cascade="all, delete-orphan"
    )


class JD(Base):
    __tablename__ = "jds"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), default="")
    company: Mapped[str] = mapped_column(String(255), default="")
    source_url: Mapped[str] = mapped_column(String(512), default="")  # minh chứng nguồn (mục 3)
    raw_text: Mapped[str] = mapped_column(Text, default="")
    parsed: Mapped[dict] = mapped_column(JSONB, default=dict)
    # PA2: điều kiện lọc chính ở Tầng 3 — cột riêng có index, KHÔNG nhét vào JSONB
    location_normalized: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    level_normalized: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    industry_group: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    embedding = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    matches: Mapped[list["MatchResult"]] = relationship(
        back_populates="jd", cascade="all, delete-orphan"
    )


class MatchResult(Base):
    """Kết quả chấm 1 cặp CV–JD. Mọi điểm đều kèm breakdown — không hộp đen."""

    __tablename__ = "match_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cvs.id", ondelete="CASCADE"), index=True)
    jd_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jds.id", ondelete="CASCADE"), index=True)

    # Tầng 4: hybrid scoring — công thức trọng số ghi trong code scoring + README
    score_skill: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_semantic: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_llm: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_total: Mapped[float | None] = mapped_column(Float, nullable=True)

    gaps: Mapped[dict] = mapped_column(JSONB, default=dict)  # Tầng 5: gap theo thứ tự ưu tiên
    explanation: Mapped[dict] = mapped_column(JSONB, default=dict)  # evidence trích từ CV/JD
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cv: Mapped[CV] = relationship(back_populates="matches")
    jd: Mapped[JD] = relationship(back_populates="matches")
