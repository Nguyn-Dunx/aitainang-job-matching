"""Tầng 4 — Hybrid scoring V1 (công thức CÔNG KHAI, không hộp đen).

    score_total = W_SKILL * score_skill + W_SEMANTIC * score_semantic

    W_SKILL    = 0.6  (skill overlap la tin hieu manh nhat cho matching IT)
    W_SEMANTIC = 0.4  (cosine embedding bat ngu nghia ngoai taxonomy)

- score_skill   = |CV skills ∩ JD skills| / |JD skills| * 100
  (ca 2 phia deu la canonical name trong taxonomy 235 skill cua A)
- score_semantic = cosine(cv_embedding, jd_embedding) * 100
- evidence: moi skill khop kem doan trich trong JD (evidence_snippet tu Tang 2)
  va cho biet skill do co trong CV o dau.

V1 CHUA co: diem LLM danh gia trach nhiem (score_llm) — them o ban sau.
"""

from __future__ import annotations

W_SKILL = 0.6
W_SEMANTIC = 0.4


def score_pair(cv_skills: list[str], jd_skills: list[str], cosine_sim: float,
               jd_evidence: str = "", cv_text: str = "") -> dict:
    """Chấm 1 cặp CV–JD. Trả về điểm + breakdown + evidence, không chỉ 1 số."""
    cv_set, jd_set = set(cv_skills), set(jd_skills)
    matched = sorted(cv_set & jd_set)
    missing = sorted(jd_set - cv_set)

    score_skill = (len(matched) / len(jd_set) * 100) if jd_set else 0.0
    score_semantic = max(0.0, min(100.0, cosine_sim * 100))
    score_total = W_SKILL * score_skill + W_SEMANTIC * score_semantic

    return {
        "score_total": round(score_total, 1),
        "breakdown": {
            "skill": {
                "score": round(score_skill, 1),
                "weight": W_SKILL,
                "matched": matched,
                "missing": missing,
            },
            "semantic": {
                "score": round(score_semantic, 1),
                "weight": W_SEMANTIC,
            },
        },
        "evidence": {
            "jd_snippet": jd_evidence,
            "matched_skills_in_cv": [s for s in matched if s.lower() in cv_text.lower()],
        },
    }
