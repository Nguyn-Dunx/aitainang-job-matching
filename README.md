# aitainang — Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam

Nền tảng AI chấm độ khớp CV–JD bằng ngữ nghĩa song ngữ (Việt–Anh), giải thích từng điểm
thiếu, và đồng hành sửa CV theo vòng lặp đo được (delta score trước/sau).

Bối cảnh: Bảng C — Cuộc thi Sáng tạo trẻ Quốc gia về AI 2026. Xem `AGENTS.md` cho kiến trúc
đã chốt, quy tắc dữ liệu và tiêu chí BGK.

## Kiến trúc pipeline 5 tầng

1. **Ingestion & Parsing** — PyMuPDF đọc PDF/DOCX; fallback Docling cho layout phức tạp. *(T2)*
2. **Structured Extraction** — LLM structured output + JSON schema (skills, years, education,
   responsibilities), có validation + retry + fallback regex. *(T2)*
3. **Retrieval** — embedding đa ngôn ngữ (BGE-M3 / multilingual-e5, dim 1024) + pgvector,
   top-K JD. *(T3)*
4. **Scoring & Explanation** — hybrid: skill overlap theo taxonomy + cosine embedding + LLM
   đánh giá. Công thức trọng số công khai trong code và README này. *(T3)*
5. **CV Improvement** — gợi ý sửa CV theo gap của 1 JD, chấm lại → delta score. *(T4)*

## Cấu trúc repo

```
app/            FastAPI backend (main, config, db, models, routers)
data/           Dữ liệu D1–D4 (xem data/DATA_SOURCES.md) — quy tắc ẩn danh trong AGENTS.md
docs/           Tài liệu, PROMPT_LOG.md (bắt buộc nộp — mục 13 Mẫu 3)
scripts/        Script thu thập/xử lý dữ liệu
tests/          pytest
.github/        CI: ruff + pytest trên mọi push/PR
```

## Chạy dev local

```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env                                     # điền LLM_API_KEY khi có

docker compose up -d db                                  # PostgreSQL 16 + pgvector
python -c "from app.db import init_db; init_db()"        # tạo extension + bảng
uvicorn app.main:app --reload                            # http://localhost:8000/docs
```

Kiểm tra: `ruff check app tests` và `pytest -q` (giống CI).

## Schema DB (T1)

- `cvs` — file gốc, raw_text (T1 parsing), parsed JSONB (T2), embedding vector(1024) (T3)
- `jds` — như trên, thêm `source_url` làm minh chứng nguồn dữ liệu (mục 3 Mẫu 3)
- `match_results` — điểm từng thành phần (skill/semantic/llm/total) + gaps + explanation
  JSONB: mọi điểm số đều kèm breakdown, không hộp đen

## Công thức chấm điểm (sẽ chốt ở T3)

`score_total = w_skill * score_skill + w_semantic * score_semantic + w_llm * score_llm`

Trọng số `w_*` sẽ được chốt sau ablation (4 biến thể: keyword / embedding-only / LLM-only /
full hybrid) và ghi trực tiếp trong module scoring.

## Lộ trình

- **T1** (xong): repo, skeleton FastAPI, schema DB, CI lint+test
- **T2**: Tầng 1+2 — parsing + extraction, parse đúng ≥90% trên 30 CV mẫu
- **T3**: Tầng 3+4 — embedding + pgvector retrieval + hybrid scoring, baseline/ablation
- **T4**: Tầng 5 + deploy Docker Compose có health-check, URL public

---

## Trạng thái & Blockers (cập nhật 2026-09-26)

- [ ] **LLM extraction (Tầng 2) đang bị chặn**: cần `LLM_API_KEY` trong `.env`
  (mặc định NVIDIA NIM, xem `.env.example`). **Việc này do con người quyết định** —
  chọn nhà cung cấp, tạo key, điền vào `.env` (KHÔNG commit `.env`). Sau khi có key,
  kiểm tra bằng `python scripts/test_llm_api.py`.
- [ ] Bộ JD `data/processed/jds.json` sẽ được A cập nhật (bổ sung JD nhóm Data/AI) —
  Tầng 3 (embedding) và Tầng 2 phía JD chỉ chạy SAU khi có bản mới, tránh làm lại.
- [x] Tầng 1+2 cho CV (D2): parser + extraction + rule fallback — xong, 14/14 test pass.

## Database dùng chung (Neon)

DB production/dev của cả đội là **1 instance Neon duy nhất** (Postgres managed, có pgvector).
A, B, C đều dùng chung `DATABASE_URL` trong `.env` — **KHÔNG tự dựng Postgres local/Docker riêng**
để tránh lệch dữ liệu giữa 3 máy.

- Lấy connection string từ nhóm trưởng, điền vào `.env` (file này đã nằm trong `.gitignore`,
  TUYỆT ĐỐI không commit — lộ ra là ai cũng đọc/ghi được DB thật).
- Lần đầu setup: `python scripts/migrate_002_jd_filter_columns.py` rồi
  `python scripts/import_jds_json.py` (chỉ 1 người chạy, các máy khác dùng chung dữ liệu).
- `docker-compose.yml` chỉ còn là phương án dự phòng offline.

## Tầng 4 — Công thức chấm điểm V1 (công khai, không hộp đen)

    score_total = 0.6 × score_skill + 0.4 × score_semantic

- `score_skill` = |skills CV ∩ skills JD| / |skills JD| × 100 — cả hai phía đều là
  canonical name trong taxonomy 235 skill (data/taxonomy/skills_taxonomy.json)
- `score_semantic` = cosine(embedding CV, embedding JD) × 100 — BGE-M3, 1024-dim
- Mọi điểm trả về kèm breakdown 2 chiều + evidence (skill khớp + trích đoạn JD)
- V1 chưa có score_llm (LLM đánh giá trách nhiệm) — bổ sung bản sau

API: `POST /api/cv/upload` (multipart file PDF/DOCX; params: mode=llm|rule, top_k,
location, level, industry_group) → parsed_cv (schema Tầng 2) + matches có giải thích.

Minh bạch Tầng 2 JD (mục 9 hồ sơ): 450 JD — LLM thật 325 (72.2%), rule fallback 125 (27.8%).
