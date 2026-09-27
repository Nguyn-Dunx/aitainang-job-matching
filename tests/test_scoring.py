"""Test Tang 4: scoring V2 (tach hard/soft) + bo ablation cung interface."""

from app.services.scoring import (
    PairInput,
    score_embedding_only,
    score_hybrid_v2,
    score_keyword_only,
    split_hard_soft,
)


def test_tach_hard_soft_skill():
    hard, soft = split_hard_soft(["Python", "Teamwork", "PostgreSQL", "Communication",
                                  "English Proficiency"])
    assert set(hard) == {"Python", "PostgreSQL"}
    assert set(soft) == {"Teamwork", "Communication", "English Proficiency"}


def test_soft_skill_khong_lam_phinh_diem_hard():
    """CV chi match soft skill phai co diem hard = 0 — V1 se bi phinh."""
    inp = PairInput(cv_text="Toi giao tiep tot", cv_skills=["Teamwork", "Communication"],
                    jd_text="Can Python, Django, Teamwork", jd_skills=["Python", "Django", "Teamwork"],
                    cosine_sim=0.5)
    r = score_hybrid_v2(inp)
    assert r["breakdown"]["hard_skill"]["score"] == 0.0
    assert r["breakdown"]["soft_skill"]["score"] == 100.0
    # 0.5*0 + 0.1*100 + 0.4*50 = 30
    assert r["score_total"] == 30.0


def test_trong_so_cong_khai_tong_bang_1():
    from app.services.scoring import W_HARD, W_SEMANTIC, W_SOFT
    assert abs(W_HARD + W_SOFT + W_SEMANTIC - 1.0) < 1e-9


def test_ablation_cung_output_shape():
    inp = PairInput(cv_text="Python Django", cv_skills=["Python"],
                    jd_text="Python Developer", jd_skills=["Python", "SQL"],
                    cosine_sim=0.8, jd_evidence="Kinh nghiem Python 2 nam")
    for fn in [score_hybrid_v2, score_keyword_only, score_embedding_only]:
        r = fn(inp)
        assert set(r.keys()) == {"variant", "score_total", "breakdown", "evidence"}
        assert 0 <= r["score_total"] <= 100


def test_keyword_only_khong_mo_rong_alias():
    # "py" la alias cua Python trong taxonomy — keyword_only KHONG duoc match
    inp = PairInput(cv_text="Toi code py hang ngay", cv_skills=[],
                    jd_text="Tuyen Python developer", jd_skills=[], cosine_sim=0.0)
    r = score_keyword_only(inp)
    assert "Python" not in r["breakdown"]["keyword"]["matched"]
