"""QA end-to-end: chay luong that (match -> suggest-improvement) 3 lan voi 3 CV
khac nhau, ghi MOI bat thuong (loi cung + cham + khong nhat quan).

Luu y: /upload can file .pdf/.docx that (repo khong co san), nen phan matching
duoc chay bang dung logic cua /upload (embed -> pgvector -> score_pair), con
buoc 6 goi /api/cv/suggest-improvement qua TestClient (dung code path that).

Cach chay:
    .venv/Scripts/python.exe scripts/qa_e2e.py
"""

from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db import SessionLocal
from app.main import app
from app.services.embedding import embed_query
from app.services.scoring import score_pair

CVS = [
    "cv_member_01_backend.json",
    "cv_member_02_data_ai.json",
    "cv_member_03_frontend_product.json",
]
CV_DIR = Path("data/cv_samples")


def build_cv_text(d: dict) -> str:
    parts = [d.get("target_role", ""), " ".join(d.get("skills", []))]
    for e in d.get("experience", []):
        parts.append(f"{e.get('title','')} {e.get('company','')} {e.get('description','')}")
    return " | ".join(p for p in parts if p)


def top_match(cv_skills: list[str], cv_text: str, k: int = 5) -> dict | None:
    vec = embed_query(cv_text)
    with SessionLocal() as db:
        rows = db.execute(text("""
            SELECT id, title, parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT :k
        """), {"q": str(vec), "k": k * 3}).all()
    best = None
    for r in rows:
        p = r.parsed or {}
        si = p.get("skills_info") or {}
        res = score_pair(
            cv_skills=cv_skills, jd_skills=si.get("skills", []),
            cosine_sim=r.sim, jd_evidence=si.get("evidence_snippet", ""),
        )
        if best is None or res["score_total"] > best["score"]:
            best = {"job_id": str(r.id), "title": r.title, "score": res["score_total"]}
    return best


def main() -> None:
    client = TestClient(app)
    issues: list[str] = []
    match_times: list[float] = []
    suggest_times: list[float] = []

    for name in CVS:
        d = json.loads((CV_DIR / name).read_text(encoding="utf-8"))
        cv_text = build_cv_text(d)
        print(f"\n=== {name} ===")

        t0 = time.perf_counter()
        top = top_match(d["skills"], cv_text)
        mt = time.perf_counter() - t0
        match_times.append(mt)
        if not top:
            issues.append(f"[CHAN] {name}: khong tim duoc match")
            continue
        print(f"  match OK {mt:.1f}s | top={top['title'][:50]} | score={top['score']:.1f}")

        payload = {
            "job_id": top["job_id"],
            "cv_skills": d["skills"],
            "cv_experience": [e.get("description", "") for e in d.get("experience", []) if e.get("description")],
            "cv_text": cv_text,
        }
        t0 = time.perf_counter()
        r2 = client.post("/api/cv/suggest-improvement", json=payload)
        sg = time.perf_counter() - t0
        suggest_times.append(sg)
        if r2.status_code != 200:
            issues.append(f"[CHAN] {name}: /suggest tra {r2.status_code}")
            print(f"  suggest FAIL {r2.status_code} sau {sg:.1f}s")
            continue
        b2 = r2.json()
        print(f"  suggest OK {sg:.1f}s | llm_status={b2.get('llm_status')} | "
              f"model={b2.get('model')} | suggestions={len(b2.get('suggestions') or [])} | delta={b2.get('delta')}")
        if b2.get("llm_status") != "ok":
            issues.append(f"[KHO CHIU] {name}: llm_status={b2.get('llm_status')} (khong co goi y that)")
        if sg > 45:
            issues.append(f"[KHO CHIU] {name}: suggest {sg:.1f}s > 45s (nguoi dung cho lau)")

    print("\n=== TONG KET ===")
    if match_times:
        print(f"match: min={min(match_times):.1f}s median={statistics.median(match_times):.1f}s max={max(match_times):.1f}s")
    if suggest_times:
        print(f"suggest: min={min(suggest_times):.1f}s median={statistics.median(suggest_times):.1f}s max={max(suggest_times):.1f}s")
    print(f"\nVan de phat hien ({len(issues)}):")
    for i in issues:
        print(f"  - {i}")
    if not issues:
        print("  (khong co)")


if __name__ == "__main__":
    main()
