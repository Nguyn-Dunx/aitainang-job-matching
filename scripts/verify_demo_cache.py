"""Xac nhan cache demo con hop le: goi /suggest-improvement?use_cache=true cho cap
CV demo x JD top-match, kiem tra tra ve cached=true va model dung.

Cach chay:
    .venv/Scripts/python.exe scripts/verify_demo_cache.py
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy import text

from app.db import SessionLocal
from app.services.embedding import embed_query
from app.services.scoring import score_pair

CV = "cv_member_01_backend.json"
BASE = "http://127.0.0.1:8000"


def main() -> None:
    d = json.loads((Path("data/cv_samples") / CV).read_text(encoding="utf-8"))
    parts = [d.get("target_role", ""), " ".join(d.get("skills", []))]
    for e in d.get("experience", []):
        parts.append(f"{e.get('title','')} {e.get('company','')} {e.get('description','')}")
    cv_text = " | ".join(p for p in parts if p)

    vec = embed_query(cv_text)
    with SessionLocal() as db:
        rows = db.execute(text("""
            SELECT id, title, parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT 15
        """), {"q": str(vec)}).all()
    best = None
    for r in rows:
        si = (r.parsed or {}).get("skills_info") or {}
        res = score_pair(cv_skills=d["skills"], jd_skills=si.get("skills", []),
                         cosine_sim=r.sim, jd_evidence=si.get("evidence_snippet", ""))
        if best is None or res["score_total"] > best["score"]:
            best = {"job_id": str(r.id), "title": r.title, "score": res["score_total"]}

    payload = json.dumps({
        "job_id": best["job_id"], "cv_skills": d["skills"],
        "cv_experience": [e.get("description", "") for e in d.get("experience", []) if e.get("description")],
        "cv_text": cv_text,
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE}/api/cv/suggest-improvement?use_cache=true",
                                 data=payload, headers={"Content-Type": "application/json"}, method="POST")
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    el = time.perf_counter() - t0
    print(f"JD top-match: {best['title'][:50]} | job_id={best['job_id']}")
    print(f"cached={body.get('cached')} | model={body.get('model')} | "
          f"llm_status={body.get('llm_status')} | suggestions={len(body.get('suggestions') or [])} | "
          f"generated_at={body.get('generated_at')} | tra ve trong {el:.2f}s")
    if body.get("cached") and body.get("model") == "nvidia/nemotron-3-ultra-550b-a55b":
        print("=> CACHE HOP LE voi model chinh moi (Ultra).")
    else:
        print("=> CACHE KHONG HOP LE / KHONG CO - can chay lai de cache bang Ultra.")


if __name__ == "__main__":
    main()
