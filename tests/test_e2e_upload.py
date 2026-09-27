"""Test end-to-end: upload CV synthetic -> parse -> extract -> embed -> retrieve -> score.

Chay voi mode=rule (deterministic, khong goi LLM). Can: Neon DB co 450 JD + embedding.
    python -m pytest tests/test_e2e_upload.py -q
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_upload_cv_backend_tim_dung_nganh(client):
    cv_path = FIXTURES / "cv_single_column.pdf"  # CV Backend: Python, Django, PostgreSQL
    if not cv_path.exists():
        pytest.skip("Chưa có fixture — chạy: python scripts/make_synthetic_cvs.py")

    with open(cv_path, "rb") as f:
        resp = client.post("/api/cv/upload?mode=rule&top_k=5",
                           files={"file": ("cv.pdf", f, "application/pdf")})
    assert resp.status_code == 200, resp.text[:500]
    data = resp.json()

    # Shape khop UI cua C
    cv = data["parsed_cv"]
    for key in ["candidate_id", "target_title", "years_of_experience",
                "education", "skills", "experience", "uploaded_filename"]:
        assert key in cv, f"parsed_cv thieu truong: {key}"
    assert "Python" in cv["skills"]

    # Matches: co diem + breakdown + evidence, khong phai 1 so vo danh
    assert len(data["matches"]) > 0
    top = data["matches"][0]
    for key in ["id", "title", "score", "breakdown", "evidence", "industry_group"]:
        assert key in top, f"match thieu truong: {key}"
    assert 0 <= top["score"] <= 100
    assert set(top["breakdown"].keys()) == {"skill", "semantic"}
    assert top["breakdown"]["skill"]["weight"] == 0.6  # cong thuc cong khai

    # CV backend Python/Django -> top-5 phai nghieng ve Software Engineering
    groups = [m["industry_group"] for m in data["matches"]]
    assert groups.count("Software Engineering") >= 2, f"Top-5 lech nganh: {groups}"

    # Diem phai giam dan (da sort)
    scores = [m["score"] for m in data["matches"]]
    assert scores == sorted(scores, reverse=True)
