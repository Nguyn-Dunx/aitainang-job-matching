"""Tầng 2 cho CV — trích xuất có cấu trúc từ text CV thô.

- llm: gọi API OpenAI-compatible (mặc định NVIDIA NIM, xem app/config.py), output JSON
  theo schema, validate bằng pydantic, retry 1 lần khi JSON hỏng.
- rule: fallback deterministic — tách section theo heading Việt/Anh thường gặp +
  match kỹ năng theo taxonomy D4 (data/taxonomy/skills_taxonomy.json).

Nguyên tắc chống hallucination (AGENTS.md): LLM chỉ được trích thông tin CÓ trong CV,
schema validation bắt buộc; khi nghi ngờ thì để null thay vì đoán.
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

log = logging.getLogger(__name__)

MAX_CV_CHARS = 8000
TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy" / "skills_taxonomy.json"


class EducationItem(BaseModel):
    degree: str | None = None
    major: str | None = None
    institution: str | None = None
    year: str | None = None


class ExperienceItem(BaseModel):
    title: str | None = None
    company: str | None = None
    duration: str | None = None  # giữ nguyên văn, vd "06/2024 - 12/2024"
    description: str = ""


class ProjectItem(BaseModel):
    name: str | None = None
    description: str = ""
    tech_stack: list[str] = Field(default_factory=list)


class CVSchema(BaseModel):
    """Schema CV có cấu trúc. CV đã ẩn danh nên full_name/email/phone thường là null."""

    full_name: str | None = None
    target_role: str | None = None
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    years_of_experience: float | None = None


# ----------------------------- LLM extraction -----------------------------

_LLM_SYSTEM = (
    "Bạn là bộ trích xuất thông tin CV (resume parser) cho CV tiếng Việt lẫn tiếng Anh. "
    "Chỉ trả về JSON hợp lệ theo schema yêu cầu, không giải thích thêm. "
    "Chỉ trích thông tin CÓ THẬT trong CV; không suy diễn, không bịa. "
    "Trường không có trong CV thì để null hoặc mảng rỗng."
)

_LLM_INSTRUCTION = """Trích xuất CV sau thành JSON theo schema:
{{
  "full_name": string|null,
  "target_role": string|null,
  "summary": string,
  "skills": [string],
  "education": [{{"degree": string|null, "major": string|null, "institution": string|null, "year": string|null}}],
  "experience": [{{"title": string|null, "company": string|null, "duration": string|null, "description": string}}],
  "projects": [{{"name": string|null, "description": string, "tech_stack": [string]}}],
  "languages": [string],
  "years_of_experience": number|null
}}

CV:
{text}"""


def extract_cv_llm(text: str, client=None, model: str | None = None) -> CVSchema:
    from openai import OpenAI

    from app.config import settings

    client = client or OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key,
                             max_retries=0)
    model = model or settings.llm_model
    payload = _LLM_INSTRUCTION.format(text=text[:MAX_CV_CHARS])

    last_err: Exception | None = None
    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _LLM_SYSTEM},
                    {"role": "user", "content": payload},
                ],
                response_format={"type": "json_object"},
                temperature=0,
                timeout=settings.llm_timeout_s,
            )
            data = json.loads(resp.choices[0].message.content)
            return CVSchema.model_validate(data)
        except (json.JSONDecodeError, ValidationError, KeyError, IndexError) as e:
            last_err = e
            log.warning("LLM CV extraction attempt %d failed: %s", attempt + 1, e)
    raise RuntimeError(f"LLM CV extraction failed after 2 attempts: {last_err}")


# ----------------------------- Rule fallback ------------------------------

_SECTION_HEADERS = {
    "skills": ["kỹ năng", "ky nang", "skills", "technical skills", "kỹ năng chuyên môn"],
    "education": ["học vấn", "hoc van", "education", "quá trình đào tạo"],
    "experience": ["kinh nghiệm", "kinh nghiem", "experience", "work experience", "kinh nghiệm làm việc"],
    "projects": ["dự án", "du an", "projects", "project"],
    "languages": ["ngoại ngữ", "ngon ngu", "languages"],
}


def _norm(s: str) -> str:
    return unicodedata.normalize("NFC", s.lower())


def _split_sections(text: str) -> dict[str, str]:
    """Tách CV thành các section theo heading. Phần trước heading đầu tiên = 'header'."""
    lines = text.splitlines()
    sections: dict[str, list[str]] = {"header": []}
    current = "header"
    for line in lines:
        stripped = line.strip()
        norm = _norm(stripped).strip(":•-–— ")
        matched = None
        if stripped and len(stripped) < 60:
            for key, headers in _SECTION_HEADERS.items():
                if any(norm == h or norm.startswith(h) for h in headers):
                    matched = key
                    break
        if matched:
            current = matched
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _match_skills(text: str, taxonomy_path: Path = TAXONOMY_PATH) -> list[str]:
    with open(taxonomy_path, encoding="utf-8") as f:
        skills = json.load(f)["skills"]
    norm_text = _norm(text)
    found = []
    for skill in skills:
        for alias in sorted(skill.get("aliases", []), key=len, reverse=True):
            pat = r"(?<![\w+.#])" + re.escape(_norm(alias)) + r"(?![\w+#])"
            if re.search(pat, norm_text):
                found.append(skill["canonical"])
                break
    return sorted(set(found))


def extract_cv_rule(text: str, taxonomy_path: Path = TAXONOMY_PATH) -> CVSchema:
    sections = _split_sections(text)
    header = sections.get("header", "")
    return CVSchema(
        full_name=None,  # rule không đoán tên — tránh nhầm dòng đầu làm tên
        summary=header[:500],
        skills=_match_skills(text, taxonomy_path),
        experience=[ExperienceItem(description=sections["experience"])] if sections.get("experience") else [],
        projects=[ProjectItem(description=sections["projects"])] if sections.get("projects") else [],
        education=[EducationItem(degree=sections["education"][:200])] if sections.get("education") else [],
        languages=[sections["languages"][:200]] if sections.get("languages") else [],
        years_of_experience=None,
    )


def extract_cv(text: str, mode: str = "llm", **kwargs) -> CVSchema:
    """Điểm vào thống nhất. mode='llm' tự fallback về rule khi LLM lỗi."""
    if mode == "rule":
        return extract_cv_rule(text, kwargs.get("taxonomy_path", TAXONOMY_PATH))
    if mode == "llm":
        try:
            return extract_cv_llm(text, kwargs.get("client"), kwargs.get("model"))
        except Exception as e:  # noqa: BLE001 — fallback boundary: moi loi LLM deu phai ve rule
            log.warning("LLM extraction unavailable, fallback to rule: %s", e)
            return extract_cv_rule(text, kwargs.get("taxonomy_path", TAXONOMY_PATH))
    raise ValueError(f"Unknown mode: {mode}")
