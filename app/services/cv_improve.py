"""Tầng 5 — Gợi ý sửa CV theo gap của 1 JD + chấm lại điểm (delta thật).

Nguyên tắc:
- Gap lấy từ đúng hàm scoring hiện có (split_hard_soft + _overlap_score), KHÔNG tính lại từ đầu.
- LLM CHỈ được gợi ý dựa trên missing skills thật; prompt cấm bịa kinh nghiệm CV không có
  (gợi ý phải viết dạng điều kiện: "nếu bạn đã từng..., hãy thêm bullet...").
- Delta = score_pair(CV + accepted_skills) - score_pair(CV gốc), cùng cosine_sim
  -> delta thuần túy từ thành phần skill, semantic giữ nguyên (ghi rõ trong response).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

from app.services.scoring import (
    PairInput,
    _overlap_score,
    score_hybrid_v2,
    split_hard_soft,
)

log = logging.getLogger(__name__)

_SUGGEST_PROMPT = """Bạn là chuyên gia tư vấn CV. JD "{job_title}" yêu cầu các kỹ năng mà CV chưa có:
{missing_skills}

Kinh nghiệm hiện có trong CV:
{experience}

Hãy đề xuất 2-4 gợi ý CỤ THỂ để cải thiện CV cho JD này. QUY TẮC BẮT BUỘC:
- Mỗi gợi ý gắn với ĐÚNG 1 kỹ năng trong danh sách thiếu ở trên, không thêm kỹ năng khác.
- KHÔNG được bịa kinh nghiệm/dự án CV không có. Viết dạng điều kiện, ví dụ:
  "Nếu bạn đã từng dùng Docker trong đồ án, hãy thêm bullet: 'Container hóa ứng dụng bằng Docker...'".
- Gợi ý phải là bullet cụ thể đưa vào phần mô tả công việc, không nói chung chung.
- Mỗi gợi ý tối đa 2 câu, ngắn gọn.

Chỉ trả về JSON: {{"suggestions": [{{"skill": string, "text": string}}]}}"""


def _extract_json(text: str | None) -> dict | None:
    if not text:
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def compute_gap(cv_skills: list[str], jd_skills: list[str]) -> dict:
    """Gap thật từ scoring hiện có: missing hard/soft skills."""
    cv_hard, cv_soft = split_hard_soft(cv_skills)
    jd_hard, jd_soft = split_hard_soft(jd_skills)
    _, matched_hard, missing_hard = _overlap_score(set(cv_hard), set(jd_hard))
    _, matched_soft, missing_soft = _overlap_score(set(cv_soft), set(jd_soft))
    return {
        "matched_hard": matched_hard,
        "missing_hard": missing_hard,
        "matched_soft": matched_soft,
        "missing_soft": missing_soft,
    }


def generate_suggestions(
    job_title: str,
    missing_skills: list[str],
    experience_texts: list[str],
    client=None,
    model: str | None = None,
) -> dict:
    """LLM sinh 2-4 gợi ý, ràng buộc chỉ dùng missing_skills thật.

    Trả về dict: {"suggestions": [...], "llm_status": "ok"|"unavailable"|"timeout",
    "model": str|None}. Trạng thái trung thực để endpoint KHÔNG trả delta 0 như thể
    là kết quả khi LLM lỗi.

    Chuỗi retry 2 lượt: model chính (timeout đầy đủ) -> fallback (timeout rút ngắn
    15s) -> tổng tối đa ~60s cho endpoint. Gợi ý có skill ngoài danh sách missing
    bị loại bỏ (chống bịa).
    """
    from openai import OpenAI

    from app.config import settings

    if not missing_skills:
        # Không có gap -> không phải lỗi LLM; không gọi API.
        return {"suggestions": [], "llm_status": "ok", "model": None}

    client = client or OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key,
                              max_retries=0)  # khong retry internal: fallback cham som hon
    prompt = _SUGGEST_PROMPT.format(
        job_title=job_title,
        missing_skills="\n".join(f"- {s}" for s in missing_skills),
        experience="\n".join(f"- {t}" for t in experience_texts[:3]) or "(chưa có mô tả)",
    )
    attempts = [
        (model or settings.llm_model, True, settings.llm_timeout_s),
        (settings.llm_fallback_model, True, min(settings.llm_timeout_s, 15)),
    ]
    last_status = "unavailable"
    for m, use_format, tmo in attempts:
        try:
            kwargs: dict = {"model": m,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0, "timeout": tmo}
            if use_format:
                kwargs["response_format"] = {"type": "json_object"}
            resp = client.chat.completions.create(**kwargs)
            data = _extract_json(resp.choices[0].message.content)
            if not data or not isinstance(data.get("suggestions"), list):
                last_status = "unavailable"  # content rong/khong dung schema
                continue
            allowed = {s.lower() for s in missing_skills}
            out = [
                {"skill": str(s["skill"]), "text": str(s["text"])}
                for s in data["suggestions"]
                if isinstance(s, dict) and str(s.get("skill", "")).lower() in allowed and s.get("text")
            ]
            if out:
                return {"suggestions": out[:4], "llm_status": "ok", "model": m}
            last_status = "unavailable"
        except Exception as e:  # noqa: BLE001 - log roi thu model tiep theo
            msg = str(e).lower()
            last_status = "timeout" if ("timeout" in msg or "timed out" in msg) else "unavailable"
            log.warning("generate_suggestions loi (model=%s, fmt=%s): %s", m, use_format, e)
    return {"suggestions": [], "llm_status": last_status, "model": None}


# --- Cache ket qua thanh cong gan nhat theo (cv_id, job_id) ---------------------
# Muc dich: cho phep quay demo bang ket qua THAT da chay truoc do khi NVIDIA NIM
# suy giam. KHONG tu dong dung cache khi nguoi dung khong yeu cau (?use_cache=true).

_CACHE_DIR = Path("data/demo_cache")


def cache_key(cv_id: str | None, job_id: str, cv_skills: list[str], cv_text: str = "") -> str:
    """Khoa cache on dinh. Uu tien cv_id; neu khong co thi bam tu noi dung CV."""
    if cv_id:
        raw = f"{cv_id}|{job_id}"
    else:
        raw = f"{job_id}|{','.join(sorted(cv_skills))}|{cv_text[:200]}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def save_cache(key: str, payload: dict) -> None:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (_CACHE_DIR / f"{key}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_cache(key: str) -> dict | None:
    f = _CACHE_DIR / f"{key}.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def rescore_with_skills(
    cv_skills: list[str],
    accepted_skills: list[str],
    jd_skills: list[str],
    cosine_sim: float,
    jd_evidence: str = "",
    cv_text: str = "",
) -> dict:
    """Chấm lại điểm khi người dùng chấp nhận thêm accepted_skills vào CV.

    Dùng đúng score_hybrid_v2 hiện có; cosine_sim giữ nguyên (không re-embed)
    -> delta thuần túy từ thành phần skill overlap.
    """
    before = score_hybrid_v2(PairInput(
        cv_text=cv_text, cv_skills=cv_skills, jd_text="", jd_skills=jd_skills,
        cosine_sim=cosine_sim, jd_evidence=jd_evidence,
    ))
    merged = list(dict.fromkeys([*cv_skills, *accepted_skills]))  # giữ thứ tự, khử trùng
    after = score_hybrid_v2(PairInput(
        cv_text=cv_text, cv_skills=merged, jd_text="", jd_skills=jd_skills,
        cosine_sim=cosine_sim, jd_evidence=jd_evidence,
    ))
    return {
        "score_before": before["score_total"],
        "score_after": after["score_total"],
        "delta": round(after["score_total"] - before["score_total"], 1),
        "breakdown_before": before["breakdown"],
        "breakdown_after": after["breakdown"],
    }
