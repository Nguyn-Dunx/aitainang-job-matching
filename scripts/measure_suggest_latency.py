"""Đo latency thật của POST /api/cv/suggest-improvement trên server đang chạy.

Cách chạy (server phải đang chạy ở BASE_URL):
    .venv/Scripts/python.exe scripts/measure_suggest_latency.py --runs 3
    .venv/Scripts/python.exe scripts/measure_suggest_latency.py --cv cv_member_02_data_ai.json --runs 3

Phương pháp:
- Chọn JD = top-1 match THẬT của CV theo đúng luồng matching (pgvector -> score_pair),
  không chọn tay -> đảm bảo có gap thật để LLM phải sinh gợi ý.
- Mỗi lần đo: POST mới (use_cache=false mặc định), đo wall-time, ghi llm_status +
  model trả về trong response (bằng chứng model nào đã trả lời).
- In min/median/max sau N lần.
"""

from __future__ import annotations

import argparse
import json
import statistics
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

CV_DIR = Path("data/cv_samples")


def load_cv(name: str) -> dict:
    d = json.loads((CV_DIR / name).read_text(encoding="utf-8"))
    parts = [d.get("target_role", ""), d.get("target_industry", "")]
    parts += [e.get("description", "") for e in d.get("experience", [])]
    return {
        "skills": d["skills"],
        "experience": [e.get("description", "") for e in d.get("experience", []) if e.get("description")],
        "cv_text": " | ".join(p for p in parts if p),
    }


def top1_job(cv_skills: list[str], cv_text: str) -> dict:
    vec = embed_query(cv_text)
    with SessionLocal() as db:
        rows = db.execute(text("""
            SELECT id, title, parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT 9
        """), {"q": str(vec)}).all()
    best = None
    for r in rows:
        p = r.parsed or {}
        skills_info = p.get("skills_info") or {}
        res = score_pair(
            cv_skills=cv_skills,
            jd_skills=skills_info.get("skills", []),
            cosine_sim=r.sim,
            jd_evidence=skills_info.get("evidence_snippet", ""),
        )
        if best is None or res["score_total"] > best["score"]:
            best = {
                "job_id": str(r.id), "title": r.title,
                "jd_skills": skills_info.get("skills", []),
                "score": res["score_total"],
            }
    return best


def measure(base_url: str, job_id: str, cv: dict) -> dict:
    payload = json.dumps({
        "job_id": job_id,
        "cv_skills": cv["skills"],
        "cv_experience": cv["experience"],
        "cv_text": cv["cv_text"],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/cv/suggest-improvement",
        data=payload, headers={"Content-Type": "application/json"}, method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        elapsed = time.perf_counter() - t0
        return {
            "ok": True, "elapsed": elapsed,
            "llm_status": body.get("llm_status"),
            "model": body.get("model"),
            "n_suggestions": len(body.get("suggestions") or []),
            "delta": body.get("delta"),
        }
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "elapsed": time.perf_counter() - t0, "error": str(e)[:200]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8000")
    ap.add_argument("--cv", default="cv_member_01_backend.json")
    ap.add_argument("--runs", type=int, default=3)
    args = ap.parse_args()

    cv = load_cv(args.cv)
    job = top1_job(cv["skills"], cv["cv_text"])
    print(f"CV: {args.cv} | JD top-1: {job['title'][:60]} | job_id={job['job_id']} | score={job['score']:.1f}")

    results = []
    for i in range(args.runs):
        r = measure(args.base_url, job["job_id"], cv)
        results.append(r)
        if r["ok"]:
            print(f"  run {i + 1}: {r['elapsed']:.1f}s | llm_status={r['llm_status']} | "
                  f"model={r['model']} | suggestions={r['n_suggestions']} | delta={r['delta']}")
        else:
            print(f"  run {i + 1}: FAIL sau {r['elapsed']:.1f}s | {r['error']}")

    oks = [r for r in results if r["ok"]]
    if oks:
        times = [r["elapsed"] for r in oks]
        print(f"\nTổng kết {len(oks)}/{args.runs} lần OK:")
        print(f"  min={min(times):.1f}s median={statistics.median(times):.1f}s max={max(times):.1f}s")
        models = {r["model"] for r in oks}
        statuses = {r["llm_status"] for r in oks}
        print(f"  model trả lời: {models} | llm_status: {statuses}")
    else:
        print("\nTẤT CẢ các lần gọi FAIL - không có số liệu.")


if __name__ == "__main__":
    main()
