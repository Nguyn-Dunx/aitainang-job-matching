"""Test Tầng 5: gap + rescore (không gọi LLM thật) + chống bịa skill."""

from app.services.cv_improve import compute_gap, rescore_with_skills


def test_compute_gap_dung_ham_scoring_hien_co():
    gap = compute_gap(["Python", "Teamwork"], ["Python", "Docker", "Teamwork"])
    assert "Python" in gap["matched_hard"]
    assert "Docker" in gap["missing_hard"]
    assert "Teamwork" in gap["matched_soft"]


def test_rescore_delta_tang_khi_them_skill_con_thieu():
    r = rescore_with_skills(
        cv_skills=["Python", "SQL"],
        accepted_skills=["Docker", "Kubernetes"],
        jd_skills=["Python", "SQL", "Docker", "Kubernetes"],
        cosine_sim=0.5,
    )
    assert r["score_before"] < r["score_after"]
    assert r["delta"] == round(r["score_after"] - r["score_before"], 1)
    assert r["delta"] > 0


def test_rescore_delta_zero_khi_khong_them_gi():
    r = rescore_with_skills(
        cv_skills=["Python"], accepted_skills=[], jd_skills=["Python"], cosine_sim=0.5,
    )
    assert r["delta"] == 0.0


def test_generate_suggestions_loc_skill_ngoai_gap(monkeypatch):
    """LLM tra ve skill khong nam trong missing -> bi loai (chong bia)."""
    from app.services import cv_improve

    class FakeMsg:
        content = '{"suggestions": [{"skill": "Docker", "text": "Neu ban da dung Docker..."},' \
                  ' {"skill": "Blockchain", "text": "bia khong co trong gap"}]}'

    def _fake_create(**kwargs):
        return type("R", (), {"choices": [type("C", (), {"message": FakeMsg()})()]})()

    class FakeClient:
        class chat:
            class completions:
                create = staticmethod(_fake_create)

    out = cv_improve.generate_suggestions(
        job_title="Backend", missing_skills=["Docker", "Kubernetes"],
        experience_texts=["Lam API FastAPI"], client=FakeClient(),
    )
    assert len(out) == 1
    assert out[0]["skill"] == "Docker"


def test_generate_suggestions_gap_rong_tra_ve_rong():
    from app.services.cv_improve import generate_suggestions
    assert generate_suggestions("Backend", [], ["x"]) == []
