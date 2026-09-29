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
    assert out["llm_status"] == "ok"
    assert out["model"] is not None
    assert len(out["suggestions"]) == 1
    assert out["suggestions"][0]["skill"] == "Docker"


def test_generate_suggestions_gap_rong_tra_ve_rong():
    from app.services.cv_improve import generate_suggestions
    out = generate_suggestions("Backend", [], ["x"])
    assert out["suggestions"] == []
    assert out["llm_status"] == "ok"  # khong co gap KHONG phai loi LLM


def test_generate_suggestions_timeout_bao_dung_trang_thai():
    """LLM timeout -> llm_status='timeout', suggestions rong (khong bia)."""
    from app.services import cv_improve

    def _fake_create(**kwargs):
        raise TimeoutError("Request timed out.")

    class FakeClient:
        class chat:
            class completions:
                create = staticmethod(_fake_create)

    out = cv_improve.generate_suggestions(
        job_title="Backend", missing_skills=["Docker"], experience_texts=["x"],
        client=FakeClient(),
    )
    assert out["suggestions"] == []
    assert out["llm_status"] == "timeout"


def test_generate_suggestions_unavailable_bao_dung_trang_thai():
    from app.services import cv_improve

    def _fake_create(**kwargs):
        raise RuntimeError("503 Service Unavailable")

    class FakeClient:
        class chat:
            class completions:
                create = staticmethod(_fake_create)

    out = cv_improve.generate_suggestions(
        job_title="Backend", missing_skills=["Docker"], experience_texts=["x"],
        client=FakeClient(),
    )
    assert out["suggestions"] == []
    assert out["llm_status"] == "unavailable"


def test_cache_roundtrip(tmp_path, monkeypatch):
    """save_cache/load_cache luu va doc lai dung payload."""
    from app.services import cv_improve

    monkeypatch.setattr(cv_improve, "_CACHE_DIR", tmp_path)
    key = cv_improve.cache_key("cv1", "job1", ["Python"])
    assert cv_improve.load_cache(key) is None
    cv_improve.save_cache(key, {"delta": 12.3, "generated_at": "2026-09-29T00:00:00Z"})
    got = cv_improve.load_cache(key)
    assert got["delta"] == 12.3
    assert got["generated_at"] == "2026-09-29T00:00:00Z"


def test_cache_key_on_dinh_theo_cv_id():
    from app.services.cv_improve import cache_key
    assert cache_key("cv1", "job1", ["Python"]) == cache_key("cv1", "job1", ["SQL"])
    assert cache_key("cv1", "job1", ["Python"]) != cache_key("cv2", "job1", ["Python"])
