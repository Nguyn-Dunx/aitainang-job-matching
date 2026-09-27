"""Tầng 3 phía truy vấn — embed Career Profile / CV tại thời điểm query.

Model BGE-M3 đã de-risk (scripts/de_risk_embedding.py): dim=1024, ~64ms/câu CPU.
Model được load lazy 1 lần (singleton) — load mất vài phút, không được load lại mỗi request.
"""

from __future__ import annotations

import threading

MODEL_NAME = "BAAI/bge-m3"
_model = None
_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer

                _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_query(text: str) -> list[float]:
    """Encode 1 câu/đoạn (Career Profile, CV text) thành vector 1024-dim, L2-normalized."""
    return _get_model().encode([text], normalize_embeddings=True)[0].tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    return _get_model().encode(texts, normalize_embeddings=True).tolist()
