"""POST /api/cv/upload — parse -> extract -> embed -> retrieve top-K -> score (Tang 1-4).

Response shape khop voi UI C da dung (UploadCVPage/MatchingPage):
parsed CV theo schema Tang 2 + danh sach matches kem score/breakdown/evidence.

Query params:
- mode: "llm" (mac dinh, fallback rule khi loi) | "rule" (nhanh, deterministic)
- top_k: so JD tra ve (mac dinh 10)
- location / level / industry_group: loc metadata truoc khi xep hang (Tang 3)
"""

import logging
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, UploadFile
from pydantic import BaseModel
from sqlalchemy import text

from app.db import SessionLocal
from app.models import CV, MatchResult
from app.services.cv_extraction import extract_cv
from app.services.cv_improve import (
    cache_key,
    compute_gap,
    generate_suggestions,
    load_cache,
    now_iso,
    rescore_with_skills,
    save_cache,
)
from app.services.cv_parser import parse_cv
from app.services.embedding import embed_query
from app.services.scoring import score_pair

router = APIRouter(prefix="/api/cv", tags=["cv"])

log = logging.getLogger(__name__)


def _to_ui_shape(parsed, filename: str) -> dict:
    """Map CVSchema -> shape C dang dung trong mock (UploadCVPage)."""
    edu = parsed.education[0] if parsed.education else None
    return {
        "candidate_id": parsed.full_name or "Ứng viên (Ẩn danh)",
        "target_title": parsed.target_role or "",
        "years_of_experience": parsed.years_of_experience,
        "education": {
            "institution": edu.institution if edu else None,
            "degree": edu.degree if edu else None,
            "graduation_year": edu.year if edu else None,
            "gpa": None,
        },
        "skills": parsed.skills,
        "experience": [
            {
                "id": i + 1,
                "company": e.company or "",
                "role": e.title or "",
                "period": e.duration or "",
                "responsibilities": [e.description] if e.description else [],
            }
            for i, e in enumerate(parsed.experience)
        ],
        "uploaded_filename": filename,
    }


@router.post("/upload")
async def upload_cv(
    file: UploadFile,
    mode: str = Query("llm", pattern="^(llm|rule)$"),
    top_k: int = Query(10, ge=1, le=50),
    location: str | None = None,
    level: str | None = None,
    industry_group: str | None = None,
):
    suffix = Path(file.filename).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Tang 1 + 2
    parsed_file = parse_cv(tmp_path)
    cv = extract_cv(parsed_file.text, mode=mode)
    Path(tmp_path).unlink(missing_ok=True)

    # Tang 3: embed CV, loc metadata, vector search top-K*3 roi cham diem lai
    cv_vec = embed_query(parsed_file.text)
    filters, params = ["embedding IS NOT NULL"], {"q": str(cv_vec), "k": top_k * 3}
    if location:
        filters.append("location_normalized = :location")
        params["location"] = location
    if level:
        filters.append("level_normalized = :level")
        params["level"] = level
    if industry_group:
        filters.append("industry_group = :industry_group")
        params["industry_group"] = industry_group

    with SessionLocal() as db:
        rows = db.execute(text(f"""
            SELECT id, title, location_normalized, level_normalized, industry_group,
                   parsed, 1 - (embedding <=> CAST(:q AS vector)) AS sim
            FROM jds WHERE {' AND '.join(filters)}
            ORDER BY embedding <=> CAST(:q AS vector) LIMIT :k
        """), params).all()

    # Tang 4: hybrid scoring V2 (0.5 hard_skill + 0.1 soft_skill + 0.4 semantic)
    matches = []
    for r in rows:
        p = r.parsed or {}
        meta = p.get("metadata") or {}
        skills_info = p.get("skills_info") or {}
        result = score_pair(
            cv_skills=cv.skills,
            jd_skills=skills_info.get("skills", []),
            cosine_sim=r.sim,
            jd_evidence=skills_info.get("evidence_snippet", ""),
            cv_text=parsed_file.text,
        )
        matches.append({
            "id": str(r.id),
            "title": r.title,
            "company": meta.get("company_name", "Đơn vị tuyển dụng"),
            "location": r.location_normalized,
            "level": r.level_normalized,
            "industry_group": r.industry_group,
            "salary": meta.get("salary", "Thỏa thuận"),
            "job_type": meta.get("job_type", ""),
            "benefits": (meta.get("benefits") or "").split("•")[:4] if meta.get("benefits") else [],
            "score": result["score_total"],
            "breakdown": result["breakdown"],
            "evidence": result["evidence"],
        })
    matches.sort(key=lambda m: m["score"], reverse=True)
    matches = matches[:top_k]

    # Tang 6: luu phien cham THAT (CV + match_results) de Dashboard doc lai.
    # Loi luu khong duoc lam hong ket qua upload -> bat exception, chi log.
    session_id = None
    try:
        with SessionLocal() as db:
            cv_row = CV(
                filename=file.filename or "cv.pdf",
                raw_text=parsed_file.text,
                parsed=cv.model_dump(),
                embedding=cv_vec,
            )
            db.add(cv_row)
            db.flush()
            for m in matches:
                bd = m.get("breakdown") or {}
                db.add(MatchResult(
                    cv_id=cv_row.id,
                    jd_id=uuid.UUID(m["id"]),
                    score_skill=(bd.get("hard_skill") or {}).get("score"),
                    score_semantic=(bd.get("semantic") or {}).get("score"),
                    score_llm=None,
                    score_total=m["score"],
                    gaps={"missing_hard": (bd.get("hard_skill") or {}).get("missing", [])},
                    explanation=m.get("evidence") or {},
                ))
            db.commit()
            session_id = str(cv_row.id)
    except Exception as e:  # noqa: BLE001
        log.warning("Khong luu duoc phien cham vao DB: %s", e)

    return {
        "parsed_cv": _to_ui_shape(cv, file.filename),
        "parse_warnings": parsed_file.warnings,
        "extraction_mode": mode,
        "session_id": session_id,
        "matches": matches,
    }


@router.get("/history")
def get_history(limit: int = Query(5, ge=1, le=20)):
    """Tang 6: lich su phien cham THAT tu DB (khong mock).

    Tra ve danh sach CV da upload (moi nhat truoc) + top match cua phien gan nhat.
    Dashboard doc truc tiep tu day de khong hien ten cong ty/diem gia.
    """
    with SessionLocal() as db:
        cv_rows = db.execute(text("""
            SELECT c.id, c.filename, c.parsed, c.created_at,
                   count(m.id) AS jobs_matched,
                   max(m.score_total) AS top_score
            FROM cvs c
            LEFT JOIN match_results m ON m.cv_id = c.id
            GROUP BY c.id
            ORDER BY c.created_at DESC
            LIMIT :limit
        """), {"limit": limit}).all()

        sessions = []
        for r in cv_rows:
            p = r.parsed or {}
            sessions.append({
                "cv_id": str(r.id),
                "filename": r.filename,
                "candidate_id": p.get("full_name") or "Ứng viên (Ẩn danh)",
                "target_title": p.get("target_role") or "",
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "jobs_matched": int(r.jobs_matched or 0),
                "top_score": round(float(r.top_score), 1) if r.top_score is not None else None,
            })

        latest = None
        if sessions:
            latest_id = sessions[0]["cv_id"]
            mrows = db.execute(text("""
                SELECT m.id, m.score_total, m.gaps, j.title, j.parsed,
                       j.location_normalized, j.level_normalized, j.industry_group
                FROM match_results m
                JOIN jds j ON j.id = m.jd_id
                WHERE m.cv_id = :cid
                ORDER BY m.score_total DESC NULLS LAST
            """), {"cid": latest_id}).all()
            matches = []
            for m in mrows:
                meta = (m.parsed or {}).get("metadata") or {}
                matches.append({
                    "id": str(m.id),
                    "title": m.title,
                    "company": meta.get("company_name", "Đơn vị tuyển dụng"),
                    "score": round(float(m.score_total), 1) if m.score_total is not None else None,
                    "industry_group": m.industry_group,
                    "location": m.location_normalized,
                    "level": m.level_normalized,
                })
            gap_skills = (mrows[0].gaps or {}).get("missing_hard", []) if mrows else []
            latest = {
                "cv_id": latest_id,
                "filename": sessions[0]["filename"],
                "created_at": sessions[0]["created_at"],
                "matches": matches,
                "gap_skills": gap_skills,
            }

        top_scores = [s["top_score"] for s in sessions if s["top_score"] is not None]
        return {
            "sessions": sessions,
            "latest": latest,
            "stats": {
                "sessions": len(sessions),
                "jobs_matched": sum(s["jobs_matched"] for s in sessions),
                "top_score": max(top_scores) if top_scores else None,
            },
        }


class SuggestImprovementRequest(BaseModel):
    """Input Tầng 5: CV đã parse (không cần re-parse) + job_id của 1 JD."""
    job_id: str  # UUID của JD trong bảng jds
    cv_skills: list[str]
    cv_experience: list[str] = []  # các bullet mô tả kinh nghiệm hiện có
    cv_text: str = ""  # optional: embed để có cosine_sim thật; bỏ trống -> semantic = 0 cả 2 lần
    accepted_skills: list[str] | None = None  # None = chấp nhận tất cả skill trong gợi ý
    cv_id: str | None = None  # optional: khoá cache ổn định theo (cv_id, job_id)


def _status_message(llm_status: str, has_suggestions: bool, has_gap: bool) -> str:
    """Thông báo tiếng Việt cho người dùng theo trạng thái thật của LLM."""
    if llm_status == "timeout":
        return ("Máy chủ gợi ý AI phản hồi quá lâu nên tạm thời chưa có gợi ý. "
                "Vui lòng thử lại sau ít phút.")
    if llm_status == "unavailable":
        return ("Dịch vụ gợi ý AI hiện không khả dụng nên chưa tạo được gợi ý. "
                "Vui lòng thử lại sau.")
    if not has_gap:
        return "CV của bạn đã đáp ứng đủ kỹ năng JD yêu cầu — không có khoảng trống để gợi ý."
    if not has_suggestions:
        return "Chưa tạo được gợi ý cho JD này. Vui lòng thử lại."
    return ("Gợi ý dạng điều kiện dựa trên kỹ năng còn thiếu; điểm dự kiến nếu bạn "
            "bổ sung kinh nghiệm này.")


@router.post("/suggest-improvement")
def suggest_improvement(req: SuggestImprovementRequest, use_cache: bool = Query(False)):
    """Tầng 5: gợi ý sửa CV theo gap thật của 1 JD + chấm lại điểm (delta thật).

    - Gap lấy từ scoring hiện có (missing hard/soft skills), không tính lại từ đầu.
    - LLM chỉ gợi ý dựa trên missing skills; gợi ý lệch danh sách bị loại (chống bịa).
    - Delta = score_hybrid_v2(CV + accepted) - score_hybrid_v2(CV gốc), cùng cosine_sim
      -> delta thuần túy từ thành phần skill; semantic giữ nguyên.
    - llm_status: "ok" | "unavailable" | "timeout". Khi không có gợi ý, delta = null
      (KHÔNG trả 0 như thể là kết quả).
    - ?use_cache=true: trả kết quả thành công gần nhất đã lưu (cached=true, generated_at).
      KHÔNG tự dùng cache khi người dùng không yêu cầu.
    """
    key = cache_key(req.cv_id, req.job_id, req.cv_skills, req.cv_text)

    if use_cache:
        cached = load_cache(key)
        if cached is not None:
            return {**cached, "cached": True}

    import uuid
    is_valid_uuid = False
    try:
        uuid.UUID(str(req.job_id))
        is_valid_uuid = True
    except (ValueError, TypeError):
        is_valid_uuid = False

    with SessionLocal() as db:
        if is_valid_uuid:
            row = db.execute(text(
                "SELECT id, title, parsed, embedding FROM jds WHERE id = :id"
            ), {"id": req.job_id}).first()
        elif str(req.job_id).isdigit():
            offset = max(0, int(req.job_id) - 1)
            row = db.execute(text(
                "SELECT id, title, parsed, embedding FROM jds OFFSET :offset LIMIT 1"
            ), {"offset": offset}).first()
        else:
            row = db.execute(text(
                "SELECT id, title, parsed, embedding FROM jds LIMIT 1"
            )).first()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy JD id={req.job_id}")

    p = row.parsed or {}
    skills_info = p.get("skills_info") or {}
    jd_skills = skills_info.get("skills", [])
    jd_evidence = skills_info.get("evidence_snippet", "")

    gap = compute_gap(req.cv_skills, jd_skills)
    missing_all = gap["missing_hard"] + gap["missing_soft"]

    gen = generate_suggestions(
        job_title=row.title,
        missing_skills=missing_all,
        experience_texts=req.cv_experience,
    )
    suggestions = gen["suggestions"]
    llm_status = gen["llm_status"]
    model_used = gen["model"]

    accepted = req.accepted_skills
    if accepted is None:
        accepted = sorted({s["skill"] for s in suggestions})
    else:
        # Chi cho phep skill nam trong gap that - chan client tu them skill ngoai
        accepted = [s for s in accepted if s.lower() in {m.lower() for m in missing_all}]

    # Chi cham diem khi thuc su co skill de them; neu khong -> delta = null (khong gia 0).
    if accepted:
        cosine_sim = 0.0
        if req.cv_text:
            cv_vec = embed_query(req.cv_text)
            with SessionLocal() as db:
                sim_row = db.execute(text(
                    "SELECT 1 - (embedding <=> CAST(:q AS vector)) AS sim FROM jds WHERE id = :id"
                ), {"q": str(cv_vec), "id": row.id}).first()
            cosine_sim = sim_row.sim if sim_row and sim_row.sim is not None else 0.0

        scores = rescore_with_skills(
            cv_skills=req.cv_skills,
            accepted_skills=accepted,
            jd_skills=jd_skills,
            cosine_sim=cosine_sim,
            jd_evidence=jd_evidence,
            cv_text=req.cv_text,
        )
    else:
        scores = {
            "score_before": None, "score_after": None, "delta": None,
            "breakdown_before": None, "breakdown_after": None,
        }

    payload = {
        "job_id": str(row.id),
        "job_title": row.title,
        "gap": gap,
        "suggestions": suggestions,
        "accepted_skills": accepted,
        **scores,
        "llm_status": llm_status,
        "model": model_used,
        "message": _status_message(llm_status, bool(suggestions), bool(missing_all)),
        "cached": False,
        "generated_at": None,
        "note": ("delta chi den tu thanh phan skill overlap; semantic giu nguyen "
                 "(khong re-embed CV sau khi sua). Goi y dang dieu kien, khong bia kinh nghiem."),
    }

    # Chi luu cache khi co ket qua THAT (LLM ok + co goi y).
    if llm_status == "ok" and suggestions:
        payload["generated_at"] = now_iso()
        save_cache(key, {k: v for k, v in payload.items() if k != "cached"})

    return payload
