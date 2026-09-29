"""Đánh giá delta Tầng 5 trên nhiều cặp: 3 CV nội bộ x top-3 match thật.

Cách chạy:
    .venv/Scripts/python.exe scripts/eval_improve_delta.py

Phương pháp:
- Top-3 match lấy từ đúng luồng matching thật (pgvector top_k*3 ứng viên ->
  score_pair -> xếp hạng), KHÔNG chọn tay.
- Với mỗi cặp: delta = score_hybrid_v2(CV + toàn bộ gap hard-skill) -
  score_hybrid_v2(CV gốc), cùng cosine_sim (semantic giữ nguyên).
- Đây là CẬN TRÊN LÝ THUYẾT theo giả định người dùng xác nhận thêm toàn bộ
  kỹ năng còn thiếu (chưa cần LLM sinh gợi ý, chưa tính soft-skill gap).

Xuất: bảng từng cặp + min/median/max -> data/labeled/improve_delta_report.md
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from app.db import SessionLocal
from app.services.cv_improve import compute_gap, rescore_with_skills
from app.services.embedding import embed_query
from app.services.scoring import score_pair

CV_DIR = Path("data/cv_samples")
TOP_K = 3
OUT = Path("data/labeled/improve_delta_report.md")


def load_cvs() -> list[dict]:
    cvs = []
    for f in sorted(CV_DIR.glob("cv_member_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        parts = [d.get("target_role", ""), d.get("target_industry", "")]
        parts += [e.get("description", "") for e in d.get("experience", [])]
        cvs.append({
            "file": f.name,
            "skills": d["skills"],
            "cv_text": " | ".join(p for p in parts if p),
        })
    return cvs


def top_matches(cv_skills: list[str], cv_text: str, top_k: int) -> list[dict]:
    """Đúng luồng /api/cv/upload: pgvector top_k*3 -> score_pair -> top-k."""
    vec = embed_query(cv_text)
    with SessionLocal() as db:
        rows = db.execute(text("""
            SELECT id, title, parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT :k
        """), {"q": str(vec), "k": top_k * 3}).all()
    scored = []
    for r in rows:
        p = r.parsed or {}
        skills_info = p.get("skills_info") or {}
        res = score_pair(
            cv_skills=cv_skills,
            jd_skills=skills_info.get("skills", []),
            cosine_sim=r.sim,
            jd_evidence=skills_info.get("evidence_snippet", ""),
        )
        scored.append({
            "job_id": str(r.id), "title": r.title, "sim": r.sim,
            "jd_skills": skills_info.get("skills", []),
            "score": res["score_total"],
        })
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]


def main() -> None:
    cvs = load_cvs()
    pairs = []
    for cv in cvs:
        for m in top_matches(cv["skills"], cv["cv_text"], TOP_K):
            gap = compute_gap(cv["skills"], m["jd_skills"])
            accepted = gap["missing_hard"]  # cận trên: xác nhận toàn bộ gap hard-skill
            r = rescore_with_skills(
                cv_skills=cv["skills"], accepted_skills=accepted,
                jd_skills=m["jd_skills"], cosine_sim=m["sim"],
            )
            pairs.append({
                "cv": cv["file"], "job": m["title"], "job_id": m["job_id"],
                "n_missing_hard": len(accepted), "missing_hard": accepted,
                "before": r["score_before"], "after": r["score_after"],
                "delta": r["delta"],
            })

    deltas = [p["delta"] for p in pairs]
    lines = [
        "# Bảng delta Tầng 5 — 3 CV nội bộ × top-3 match thật (28/09/2026)",
        "",
        (
            "> **Bản chất số liệu:** điểm ƯỚC TÍNH theo giả định người dùng xác nhận thêm "
            "toàn bộ kỹ năng cứng còn thiếu (cận trên lý thuyết, không qua LLM sinh gợi ý, "
            "không tính gap soft-skill). Semantic giữ nguyên (không re-embed CV sau khi sửa)."
        ),
        (
            "> Top-3 match lấy từ đúng luồng matching thật (pgvector → score_pair → xếp hạng), "
            "không chọn tay."
        ),
        "",
        "| # | CV | JD | Số skill thiếu (hard) | Trước | Sau | Delta |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(pairs, 1):
        lines.append(
            f"| {i} | {p['cv']} | {p['job']} | {p['n_missing_hard']} "
            f"| {p['before']} | {p['after']} | **+{p['delta']}** |"
        )
    lines += [
        "",
        f"- Số cặp: {len(pairs)}",
        f"- Delta min: **+{min(deltas)}**",
        f"- Delta median: **+{statistics.median(deltas)}**",
        f"- Delta max: **+{max(deltas)}**",
        "",
        (
            "_Ghi chú: đây là cận trên lý thuyết cho mục đích kiểm chứng cơ chế chấm lại điểm; "
            "delta thật khi người dùng chỉ xác nhận một phần gợi ý sẽ thấp hơn._"
        ),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nDa luu: {OUT}")


if __name__ == "__main__":
    main()
