"""Chay Tang 5 that cho cap CV demo x JD top-match (khong chon tay).

- Lay top-match bang dung logic /upload (embed CV -> pgvector -> score_pair).
- Goi POST /api/cv/suggest-improvement qua TestClient (dung code path that).
- Luu ket qua vao data/demo_cache/ (endpoint tu luu khi llm_status=ok).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db import SessionLocal
from app.main import app
from app.services.embedding import embed_query
from app.services.scoring import score_pair

SAMPLE = Path("data/cv_samples/cv_member_01_backend.json")


def build_cv_text(d: dict) -> str:
    parts = [d.get("target_role", ""), " ".join(d.get("skills", []))]
    for e in d.get("experience", []):
        parts.append(f"{e.get('title','')} {e.get('company','')} {e.get('description','')}")
    return " | ".join(p for p in parts if p)


def main() -> int:
    d = json.loads(SAMPLE.read_text(encoding="utf-8"))
    cv_skills = d["skills"]
    cv_experience = [e.get("description", "") for e in d.get("experience", []) if e.get("description")]
    cv_text = build_cv_text(d)

    # --- Tang 3: top-match that (giong /upload) ---
    cv_vec = embed_query(cv_text)
    with SessionLocal() as db:
        rows = db.execute(text("""
            SELECT id, title, parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT 30
        """), {"q": str(cv_vec)}).all()

    scored = []
    for r in rows:
        si = (r.parsed or {}).get("skills_info") or {}
        res = score_pair(cv_skills=cv_skills, jd_skills=si.get("skills", []),
                         cosine_sim=r.sim, jd_evidence=si.get("evidence_snippet", ""),
                         cv_text=cv_text)
        scored.append((res["score_total"], str(r.id), r.title))
    scored.sort(reverse=True)
    top = scored[0]
    print(f"TOP MATCH: {top[2]} | id={top[1]} | score={top[0]}")

    # --- Tang 5: goi endpoint that ---
    client = TestClient(app)
    resp = client.post("/api/cv/suggest-improvement", json={
        "job_id": top[1], "cv_skills": cv_skills, "cv_experience": cv_experience,
        "cv_text": cv_text, "cv_id": d["id"],
    })
    print("HTTP", resp.status_code)
    body = resp.json()
    print("llm_status:", body.get("llm_status"))
    print("model:", body.get("model"))
    print("delta:", body.get("delta"))
    print("n_suggestions:", len(body.get("suggestions", [])))
    print("generated_at:", body.get("generated_at"))
    print("message:", body.get("message"))

    if body.get("llm_status") == "ok" and body.get("suggestions"):
        print("CACHE SAVED -> data/demo_cache/")
        return 0
    print("KHONG co run that (llm_status != ok)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
