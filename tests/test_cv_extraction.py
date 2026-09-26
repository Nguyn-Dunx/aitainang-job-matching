"""Test Tầng 2 cho CV: rule fallback (deterministic) + schema validation.
Không gọi LLM thật trong test — LLM được test riêng bằng scripts/test_llm_api.py."""

from pathlib import Path

import pytest

from app.services.cv_extraction import CVSchema, extract_cv, extract_cv_rule
from app.services.cv_parser import parse_cv

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def single_column_text():
    if not (FIXTURES / "cv_single_column.pdf").exists():
        pytest.skip("Chưa có fixture — chạy: python scripts/make_synthetic_cvs.py")
    return parse_cv(FIXTURES / "cv_single_column.pdf").text


def test_rule_trich_skills_theo_taxonomy(single_column_text):
    cv = extract_cv_rule(single_column_text)
    assert isinstance(cv, CVSchema)
    for skill in ["Python", "SQL", "Git", "Docker"]:
        assert skill in cv.skills, f"Thiếu skill: {skill}"


def test_rule_tach_section(single_column_text):
    cv = extract_cv_rule(single_column_text)
    assert cv.experience, "Phải tách được mục kinh nghiệm"
    assert "FPT Software" in cv.experience[0].description
    assert cv.education, "Phải tách được mục học vấn"
    assert cv.projects, "Phải tách được mục dự án"


def test_rule_khong_bia_ten(single_column_text):
    # Nguyên tắc chống hallucination: rule không đoán tên
    cv = extract_cv_rule(single_column_text)
    assert cv.full_name is None


def test_rule_cv_thieu_muc_tra_ve_mang_rong():
    text = "LE MINH CUONG\n\nSkills\nPython, Pandas, SQL\n"
    cv = extract_cv_rule(text)
    assert cv.experience == []
    assert cv.education == []
    assert "Python" in cv.skills


def test_extract_cv_mode_rule_qua_diem_vao_chung(single_column_text):
    cv = extract_cv(single_column_text, mode="rule")
    assert isinstance(cv, CVSchema)


def test_extract_cv_llm_loi_thi_fallback_rule(monkeypatch, single_column_text):
    """LLM hỏng (không có API key / JSON hỏng) -> tự fallback về rule, không crash."""
    import app.services.cv_extraction as mod

    def boom(*args, **kwargs):
        raise RuntimeError("LLM unavailable")

    monkeypatch.setattr(mod, "extract_cv_llm", boom)
    cv = extract_cv(single_column_text, mode="llm")
    assert isinstance(cv, CVSchema)
    assert "Python" in cv.skills


def test_schema_validate_json_hop_le():
    data = {
        "full_name": None,
        "skills": ["Python"],
        "education": [{"degree": "Cử nhân", "major": "CNTT", "institution": None, "year": "2025"}],
        "experience": [],
        "projects": [{"name": "Web", "description": "...", "tech_stack": ["Django"]}],
        "languages": [],
        "years_of_experience": 0.5,
    }
    cv = CVSchema.model_validate(data)
    assert cv.skills == ["Python"]
    assert cv.projects[0].tech_stack == ["Django"]
