# Checklist bản nộp — Cuộc thi Sáng tạo AI (aitainang)

> Cập nhật lần cuối: 29/09/2026. Trạng thái: **Sẵn sàng** / **Chờ người dùng** / **Chưa xong**.

## 1. Bắt buộc nộp

| # | Hạng mục | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | **PDF Mẫu 3** (`mau3_draft.pdf`) | **Chưa xong** | Đã điền TÊN 3 thí sinh (Nguyễn Tuấn Dũng, Trần Hữu Đạt, Nguyễn Quang Huy) vào `docs/mau3_draft.md` (29/09). Các ô còn lại (ngày sinh, trường, địa chỉ, SĐT, email) vẫn trống — cần bổ sung trước khi build. PDF hiện có trên đĩa là bản CŨ 13 trang. Sau khi đủ thông tin: chạy `scripts/build_pdf.py`, kiểm ≤ 20 trang, đủ 13 mục + bảng thí sinh không cắt chữ. |
| 2 | **Video demo** (2 video) | **Chờ người dùng** | Người dùng tự quay. **Dùng `?use_cache=true`** cho bước gợi ý sửa CV: cache cặp CV demo × JD top-match đã hợp lệ bằng Ultra (`data/demo_cache/488958d63147c91e.json`), trả trong 0,04 s — tránh đoạn chờ 65–120 s trong video 5 phút. |
| 3 | **Link GitHub** (`https://github.com/Nguyn-Dunx/aitainang-job-matching`) | **Sẵn sàng** | Branch `main` đã push; 34/34 test pass; `ruff check` sạch toàn repo (app + tests + scripts); frontend `vite build` OK. |
| 4 | **Prompt Log trên Google Drive** | **Chờ người dùng** | Người dùng tự upload thư mục `submission/prompt_log/` (PROMPT_LOG.md + PROMPT_LOG_COLLECTION_GUIDE.md) và mở quyền xem. Bản redacted đã qua `redact_secrets.py --verify` (exit 0, không còn chuỗi khớp mẫu secret) — ngày 29/09/2026. |

## 2. Trạng thái kỹ thuật (minh chứng kèm bản nộp)

| Hạng mục | Trạng thái | Bằng chứng |
|---|---|---|
| Test suite | Sẵn sàng | `pytest -q`: 34 passed |
| Lint | Sẵn sàng | `ruff check app tests scripts`: All checks passed (15 lỗi scripts/ đã xử lý 29/09) |
| Frontend build | Sẵn sàng | `vite build` exit 0 |
| Prompt Log sạch secret | Sẵn sàng | `redact_secrets.py --verify` exit 0 |
| Số liệu trong tài liệu | Sẵn sàng | `docs/FACT_AUDIT.md` — mọi con số đều đo thật, đã bổ sung latency LLM 29/09 |

## 3. Việc còn mở — cần quyết định / thao tác của người dùng

| # | Việc | Ai làm | Chi tiết |
|---|---|---|---|
| 1 | Điền bảng "Thông tin thí sinh" (3 thành viên) vào `docs/mau3_draft.md` | Người dùng | Sau đó yêu cầu build lại PDF (BƯỚC 3 của quy trình). |
| 2 | **Quyết định model chính/fallback Tầng 5** | Người dùng | Đã đổi theo yêu cầu: chính = Ultra (`LLM_TIMEOUT_S=110`), phụ = Super (`LLM_FALLBACK_TIMEOUT_S=50`). Đo lại thật 29/09 qua endpoint: **Ultra với 110 s KHÔNG ổn định 3/3** — 1/3 lần Ultra tự trả lời (80,6 s), 2/3 lần rơi về Super (1 do 503, 1 do Ultra vượt 110 s → tổng 121,3 s). Không tự nâng timeout. Cần quyết định: giữ nguyên, hay đổi lại Super làm chính (nhanh + ổn định hơn), hay bỏ Ultra. |
| 3 | QA end-to-end 6 bước × 3 lần (BƯỚC 2 của quy trình) | **Sẵn sàng (một phần)** | Đã chạy 29/09 qua `scripts/qa_e2e.py` với 3 CV khác nhau: match 0,9–27,5 s (27,5 s là cold-start nạp model lần đầu; warm 0,9–1,7 s), suggest 10,6–36,9 s, cả 3 lần `llm_status=ok`, 4 gợi ý/lần, delta 13,3/23,7/20,7. **0 lỗi mức chặn.** Lưu ý "khó chịu": cold-start ~27 s và suggest tới ~37 s (dưới ngưỡng 45 s nhưng người dùng phải chờ). Chưa test được bước 1–2 (`/upload` cần file .pdf/.docx thật, repo không có sẵn) — nên quay video với 1 CV PDF thật để phủ bước này. |
| 4 | Quay 2 video demo | Người dùng | Sau khi mục 1–3 ở bảng này đóng. |
| 5 | Upload Prompt Log lên Drive + mở quyền | Người dùng | Thư mục sẵn sàng, đã verify sạch. |

## 4. Thứ tự hoàn thiện đề xuất

1. Điền thông tin thí sinh → build PDF → kiểm 20 trang.
2. Chốt phương án fallback LLM (a/b/c) → cập nhật `.env`/code nếu đổi.
3. Chạy QA end-to-end 3 lần, sửa lỗi mức "chặn/khó chịu".
4. Quay video → upload Prompt Log → nộp.
