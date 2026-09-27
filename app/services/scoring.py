"""Tầng 4 — Hybrid scoring V2 + bộ ablation cho mục 9 (công thức CÔNG KHAI).

    V2: score_total = W_HARD * score_hard + W_SOFT * score_soft + W_SEMANTIC * score_semantic
        W_HARD = 0.5, W_SOFT = 0.1, W_SEMANTIC = 0.4

LY DO SUA TU V1 (0.6 skill + 0.4 semantic, gop chung moi skill):
    Taxonomy cua A co 18 "Soft Skill" (Communication, Teamwork, Responsibility...)
    + 2 "Language Skill". V1 cong don ngang nhau voi ky nang cung -> CV match
    "Teamwork" duoc diem ngang CV match "Python", lam diem skill bi phinh boi
    cac skill mem de match. V2 tach rieng: hard skill la thanh phan chinh (0.5),
    soft skill chi la thanh phan phu (0.1), hien rieng trong breakdown.

Ablation (muc 9): 4 bien the CUNG interface score(variant_input) -> dict:
    - hybrid_v2:      cong thuc tren
    - keyword_only:   dem overlap tho, KHONG chuan hoa alias (chi match dung ten canonical)
    - embedding_only: chi cosine similarity
    - llm_only:       LLM cham truc tiep 0-100, khong qua cong thuc deterministic
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)

W_HARD = 0.5
W_SOFT = 0.1
W_SEMANTIC = 0.4

# Nhom ky nang mem trong taxonomy cua A — tach khoi skill_overlap chinh
SOFT_CATEGORIES = {"Soft Skill", "Language Skill"}

TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy" / "skills_taxonomy.json"

_category_map: dict[str, str] | None = None


def _load_category_map() -> dict[str, str]:
    global _category_map
    if _category_map is None:
        with open(TAXONOMY_PATH, encoding="utf-8") as f:
            _category_map = {s["canonical"]: s["category"] for s in json.load(f)["skills"]}
    return _category_map


def split_hard_soft(skills: list[str]) -> tuple[list[str], list[str]]:
    cats = _load_category_map()
    hard = [s for s in skills if cats.get(s) not in SOFT_CATEGORIES]
    soft = [s for s in skills if cats.get(s) in SOFT_CATEGORIES]
    return hard, soft


@dataclass
class PairInput:
    """Input chung cho moi bien the scoring."""

    cv_text: str
    cv_skills: list[str]
    jd_text: str
    jd_skills: list[str]
    cosine_sim: float = 0.0
    jd_evidence: str = ""
    client: object = None  # LLM client (chi llm_only dung)
    model: str | None = None


def _overlap_score(cv_skills: set[str], jd_skills: set[str]) -> tuple[float, list[str], list[str]]:
    matched = sorted(cv_skills & jd_skills)
    missing = sorted(jd_skills - cv_skills)
    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0
    return score, matched, missing


def score_hybrid_v2(inp: PairInput) -> dict:
    cv_hard, cv_soft = split_hard_soft(inp.cv_skills)
    jd_hard, jd_soft = split_hard_soft(inp.jd_skills)

    score_hard, matched_hard, missing_hard = _overlap_score(set(cv_hard), set(jd_hard))
    score_soft, matched_soft, _ = _overlap_score(set(cv_soft), set(jd_soft))
    score_semantic = max(0.0, min(100.0, inp.cosine_sim * 100))
    score_total = W_HARD * score_hard + W_SOFT * score_soft + W_SEMANTIC * score_semantic

    return {
        "variant": "hybrid_v2",
        "score_total": round(score_total, 1),
        "breakdown": {
            "hard_skill": {"score": round(score_hard, 1), "weight": W_HARD,
                           "matched": matched_hard, "missing": missing_hard},
            "soft_skill": {"score": round(score_soft, 1), "weight": W_SOFT,
                           "matched": matched_soft},
            "semantic": {"score": round(score_semantic, 1), "weight": W_SEMANTIC},
        },
        "evidence": {
            "jd_snippet": inp.jd_evidence,
            "matched_skills_in_cv": [s for s in matched_hard if s.lower() in inp.cv_text.lower()],
        },
    }


def score_keyword_only(inp: PairInput) -> dict:
    """Overlap tho: chi match DUNG ten canonical trong text, khong mo rong alias."""
    def exact_skills(text: str) -> set[str]:
        norm = unicodedata.normalize("NFC", text.lower())
        found = set()
        for canonical in _load_category_map():
            pat = r"(?<![\w+.#])" + re.escape(unicodedata.normalize("NFC", canonical.lower())) + r"(?![\w+#])"
            if re.search(pat, norm):
                found.add(canonical)
        return found

    cv_found, jd_found = exact_skills(inp.cv_text), exact_skills(inp.jd_text)
    score, matched, missing = _overlap_score(cv_found, jd_found)
    return {
        "variant": "keyword_only",
        "score_total": round(score, 1),
        "breakdown": {"keyword": {"score": round(score, 1), "weight": 1.0,
                                  "matched": matched, "missing": missing}},
        "evidence": {"jd_snippet": inp.jd_evidence},
    }


def score_embedding_only(inp: PairInput) -> dict:
    score = max(0.0, min(100.0, inp.cosine_sim * 100))
    return {
        "variant": "embedding_only",
        "score_total": round(score, 1),
        "breakdown": {"semantic": {"score": round(score, 1), "weight": 1.0}},
        "evidence": {},
    }


_LLM_JUDGE_PROMPT = """Chấm mức phù hợp giữa CV và JD sau trên thang 0-100 (0 = không liên quan, 100 = rất phù hợp).
Chỉ trả về JSON: {{"score": number, "reason": string (1-2 câu)}}

CV:
{cv}

JD:
{jd}"""


def score_llm_only(inp: PairInput) -> dict:
    """LLM cham truc tiep. Loi -> score_total = None (loai khoi thong ke, khong doan)."""
    from openai import OpenAI

    from app.config import settings

    client = inp.client or OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    model = inp.model or settings.llm_model
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": _LLM_JUDGE_PROMPT.format(
                cv=inp.cv_text[:4000], jd=inp.jd_text[:4000])}],
            response_format={"type": "json_object"},
            temperature=0,
            timeout=120,
        )
        data = json.loads(resp.choices[0].message.content)
        score = max(0.0, min(100.0, float(data["score"])))
        return {
            "variant": "llm_only",
            "score_total": round(score, 1),
            "breakdown": {"llm_judge": {"score": round(score, 1), "weight": 1.0}},
            "evidence": {"llm_reason": data.get("reason", "")},
        }
    except Exception as e:  # noqa: BLE001 — ablation: loi LLM thi bo qua cap nay
        log.warning("llm_only failed: %s", e)
        return {"variant": "llm_only", "score_total": None,
                "breakdown": {}, "evidence": {"error": str(e)}}


VARIANTS = {
    "hybrid_v2": score_hybrid_v2,
    "keyword_only": score_keyword_only,
    "embedding_only": score_embedding_only,
    "llm_only": score_llm_only,
}


def score_pair(cv_skills: list[str], jd_skills: list[str], cosine_sim: float,
               jd_evidence: str = "", cv_text: str = "", jd_text: str = "",
               variant: str = "hybrid_v2") -> dict:
    """Diem vao thong nhat — router goi ham nay."""
    inp = PairInput(cv_text=cv_text, cv_skills=cv_skills, jd_text=jd_text,
                    jd_skills=jd_skills, cosine_sim=cosine_sim, jd_evidence=jd_evidence)
    return VARIANTS[variant](inp)
