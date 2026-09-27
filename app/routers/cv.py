"""POST /api/cv/upload — parse -> extract -> embed -> retrieve top-K -> score (Tang 1-4).

Response shape khop voi UI C da dung (UploadCVPage/MatchingPage):
parsed CV theo schema Tang 2 + danh sach matches kem score/breakdown/evidence.

Query params:
- mode: "llm" (mac dinh, fallback rule khi loi) | "rule" (nhanh, deterministic)
- top_k: so JD tra ve (mac dinh 10)
- location / level / industry_group: loc metadata truoc khi xep hang (Tang 3)
"""

import tempfile
from pathlib import Path

from fastapi import APIRouter, Query, UploadFile
from sqlalchemy import text

from app.db import SessionLocal
from app.services.cv_extraction import extract_cv
from app.services.cv_parser import parse_cv
from app.services.embedding import embed_query
from app.services.scoring import score_pair

router = APIRouter(prefix="/api/cv", tags=["cv"])


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

    # Tang 4: hybrid scoring V1
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

    return {
        "parsed_cv": _to_ui_shape(cv, file.filename),
        "parse_warnings": parsed_file.warnings,
        "extraction_mode": mode,
        "matches": matches,
    }
