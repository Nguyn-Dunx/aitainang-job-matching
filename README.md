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

## Công thức chấm điểm (đã chốt ở T3)

`score_total = w_skill * score_skill + w_semantic * score_semantic + w_llm * score_llm`

Trọng số `w_*` đã được chốt sau ablation (4 biến thể: keyword / embedding-only / LLM-only /
full hybrid) và ghi trực tiếp trong module scoring.

## Lộ trình (đã hoàn tất)

- **T1** (xong): repo, skeleton FastAPI, schema DB, CI lint+test
- **T2** (xong): Tầng 1+2 — parsing + extraction, LLM structured output + rule fallback
- **T3** (xong): Tầng 3+4 — embedding + pgvector retrieval + hybrid scoring V2, ablation 4 biến thể
- **T4** (xong): deploy Docker Compose có health-check
- **T5** (xong): Tầng 5 — CV improvement + delta score, endpoint `POST /api/cv/suggest-improvement`

---

## Trạng thái hiện tại (cập nhật 2026-09-29)

- [x] **Tầng 1–5 đã xong**: parsing → extraction → retrieval → scoring → CV improvement.
- [x] **Ablation 4 biến thể** (hybrid_v2 / keyword_only / embedding_only / llm_only) —
  cùng interface trong `app/services/scoring.py`, kết quả trong `docs/mau3_draft.md` (mục 9).
- [x] **`docs/FACT_AUDIT.md`** — đối chiếu số liệu hồ sơ với dữ liệu thật, sửa mục 3–7/9/10.
- [x] **PDF hồ sơ Mẫu 3** đã xuất: `mau3_draft.pdf` (13 trang, hạn 20).
- [x] LLM extraction chạy thật qua NVIDIA NIM (key trong `.env`, KHÔNG commit).
- [x] Bộ JD đã cập nhật: 450 JD — LLM thật 325 (72.2%), rule fallback 125 (27.8%).

Tra cứu nhanh: [`docs/API.md`](docs/API.md) (endpoint + ví dụ) ·
[`docs/FACT_AUDIT.md`](docs/FACT_AUDIT.md) (đối chiếu số liệu).

## Database dùng chung (Neon)

DB production/dev của cả đội là **1 instance Neon duy nhất** (Postgres managed, có pgvector).
A, B, C đều dùng chung `DATABASE_URL` trong `.env` — **KHÔNG tự dựng Postgres local/Docker riêng**
để tránh lệch dữ liệu giữa 3 máy.

- Lấy connection string từ nhóm trưởng, điền vào `.env` (file này đã nằm trong `.gitignore`,
  TUYỆT ĐỐI không commit — lộ ra là ai cũng đọc/ghi được DB thật).
- Lần đầu setup: `python scripts/migrate_002_jd_filter_columns.py` rồi
  `python scripts/import_jds_json.py` (chỉ 1 người chạy, các máy khác dùng chung dữ liệu).
- `docker-compose.yml` chỉ còn là phương án dự phòng offline.

## Tầng 4 — Công thức chấm điểm V2 (công khai, không hộp đen)

    score_total = 0.5 × score_hard_skill + 0.1 × score_soft_skill + 0.4 × score_semantic

- `score_hard_skill` = |hard skills CV ∩ JD| / |hard skills JD| × 100 — canonical name
  trong taxonomy 235 skill, LOẠI nhóm mềm ("Soft Skill", "Language Skill")
- `score_soft_skill` = overlap riêng trên nhóm mềm — trọng số nhỏ (0.1), hiển thị riêng
- `score_semantic` = cosine(embedding CV, embedding JD) × 100 — BGE-M3, 1024-dim
- Lý do tách (sửa từ V1): V1 cộng dồn mọi skill ngang nhau → match "Teamwork" được
  điểm ngang match "Python", làm phình điểm. V2: hard skill là tín hiệu chính.
- Mọi điểm kèm breakdown 3 chiều + evidence (skill khớp + trích đoạn JD)
- Ablation (mục 9): hybrid_v2 / keyword_only / embedding_only / llm_only — cùng
  interface trong app/services/scoring.py; chưa có score_llm trong hybrid (bản sau)

Minh bạch Tầng 2 JD (mục 9 hồ sơ): 450 JD — LLM thật 325 (72.2%), rule fallback 125 (27.8%).
