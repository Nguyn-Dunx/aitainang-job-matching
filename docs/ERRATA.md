# ERRATA — Đính chính thông tin đã công bố (aitainang)

> Mục đích: ghi lại trung thực mọi thông tin **đã từng ghi sai** trong hồ sơ, báo cáo, Prompt Log
> hoặc kịch bản video, kèm nội dung đúng và ngày đính chính. **Không sửa/xoá dòng Prompt Log cũ** —
> chỉ thêm errata tại đây để giữ nguyên vết kiểm toán (audit trail).
>
> Ngày đính chính: **29/09/2026**. Người thực hiện: B (AI/Backend Lead).

## E1 — Sai nhà cung cấp LLM: "OpenRouter" → **NVIDIA NIM**

**Mô tả lỗi.** Nhiều tài liệu mô tả LLM trích xuất kỹ năng (Tầng 2) chạy qua **OpenRouter**.
Thực tế codebase **chưa từng** gọi OpenRouter. Provider thật là **NVIDIA NIM**
(`https://integrate.api.nvidia.com/v1`), model chính `moonshotai/kimi-k3`, fallback
`nvidia/nemotron-3-ultra-550b-a55b` (xem `app/config.py`, `.env.example`, `app/services/cv_extraction.py`).

**Nội dung đúng.** LLM trích xuất kỹ năng gọi qua **NVIDIA NIM API**, model `moonshotai/kimi-k3`
(fallback `nvidia/nemotron-3-ultra-550b-a55b`), temperature=0, structured JSON.

**Các vị trí đã ghi sai và đã sửa (29/09/2026):**

| # | File | Vị trí | Nội dung sai (cũ) | Nội dung đúng (mới) |
|---|---|---|---|---|
| E1.1 | `docs/AI_TOOLS_DECLARATION.md` | dòng 17 | "`moonshotai/kimi-k3` qua **OpenRouter**" | "qua **NVIDIA NIM** (`https://integrate.api.nvidia.com/v1`)" |
| E1.2 | `docs/DEMO_SCRIPT.md` | dòng 11 | "một LLM (Kimi-K3 qua OpenRouter)" | "một LLM (Kimi-K3 qua NVIDIA NIM)" |
| E1.3 | `docs/mau3_draft.md` | mục 4.1 (dòng 184) | "LLM (OpenRouter, model `moonshotai/kimi-k3`" | "LLM (NVIDIA NIM, model `moonshotai/kimi-k3`" |
| E1.4 | `docs/mau3_draft.md` | mục 5 (dòng 206) | "`moonshotai/kimi-k3` qua OpenRouter" | "qua NVIDIA NIM (`https://integrate.api.nvidia.com/v1`)" |
| E1.5 | `docs/mau3_draft.md` | mục 6 (dòng 232) | "gọi qua OpenRouter API" | "gọi qua NVIDIA NIM API" |
| E1.6 | `docs/mau3_draft.md` | mục 8.1 (dòng 332) | "qua OpenRouter API" | "qua NVIDIA NIM API" |
| E1.7 | `docs/mau3_draft.md` | mục 9 (dòng 393) | "gồm cả LLM-only qua OpenRouter" | "gồm cả LLM-only qua NVIDIA NIM" |
| E1.8 | `docs/mau3_draft.md` | mục 10.1 (dòng 424) | sơ đồ "[OpenRouter API] (LLM extraction)" | "[NVIDIA NIM API] (LLM extraction)" |
| E1.9 | `docs/mau3_draft.md` | mục 10.3 (dòng 446) | "Nếu mất mạng/OpenRouter lỗi" | "Nếu mất mạng/NVIDIA NIM lỗi" |
| E1.10 | `docs/mau3_draft.md` | mục 11.1 (dòng 465) | "Khóa API (OpenRouter, Gemini)" | "Khóa API (NVIDIA NIM, Gemini)" |
| E1.11 | `app/services/scoring.py` | dòng 166 (comment) | "4/10 loi content=None khi OpenRouter dinh tuyen sang provider khong ho tro response_format" | "4/10 loi content=None; NGUYEN NHAN CHUA XAC DINH — nghi do provider khong ho tro response_format, chua co bang chung" |
| E1.12 | `scripts/check_llm_api.py` | dòng 1 (docstring) | "Nemotron fallback qua OpenRouter/NIM" | "Nemotron fallback qua NVIDIA NIM" |

**Ghi chú về Prompt Log.** Các dòng `[PROMPT LOG]` hiện có trong `docs/PROMPT_LOG.md` **không** ghi
sai tên provider (chúng chỉ nói "chờ xác nhận API key provider" / "LLM SDK chưa chốt"). Vì vậy
không có dòng Prompt Log nào cần đính chính cho lỗi E1; các dòng cũ được **giữ nguyên**, errata này
là bản ghi bổ sung.

## E2 — Nguyên nhân lỗi `content=None` (suy luận có căn cứ, cập nhật 29/09/2026)

**Mô tả.** Trong pilot 10 cặp, 4/10 lần gọi LLM-only trả `content=None`. Bản errata đầu tiên ghi
nguyên nhân là "chưa xác định". Sau khi kiểm tra lại (29/09/2026), có thêm căn cứ.

**Cập nhật.** Cấu hình cũ dùng `moonshotai/kimi-k3` làm model chính. Khi gọi trực tiếp model này qua
NVIDIA NIM, API trả **HTTP 404** (`Function id '...' Not Found`) — tài khoản **không có quyền truy
cập** model đó (model có tên trong danh sách catalog `/v1/models` nhưng không gọi được). Vì vậy
**rất có thể** các lần `content=None` trước đây là do gọi nhầm một model không dùng được, chứ không
phải lỗi định tuyến (routing) không xác định như bản đầu ghi.

**Mức độ chắc chắn.** Đây là **suy luận có căn cứ**, KHÔNG phải bằng chứng tuyệt đối cho *mọi* lần
lỗi `content=None` trước đó: log cũ không lưu mã lỗi HTTP của từng lần, nên không loại trừ được các
nguyên nhân khác (timeout, provider quá tải, `response_format` không hỗ trợ). Kết luận chắc chắn duy
nhất: **kimi-k3 không dùng được trên tài khoản NIM hiện tại (404)**.

**Hành động.** Đã bỏ `moonshotai/kimi-k3` khỏi cấu hình. Model chính = `nvidia/nemotron-3-ultra-550b-a55b`
(đo 1,4s), fallback = `nvidia/nemotron-3-super-120b-a12b` (đo 2,7s) — cả hai đều gọi được thật trên
NVIDIA NIM. Cơ chế retry 3 bước trong `app/services/scoring.py` giữ nguyên (xử lý triệu chứng).

## E3 — Các con số đã đính chính (tham chiếu FACT_AUDIT)

Các sai số liệu dưới đây đã được sửa trong commit cùng ngày; chi tiết nguồn xác minh xem
`docs/FACT_AUDIT.md`:

| # | Nội dung sai (cũ) | Nội dung đúng (mới) | Nguồn |
|---|---|---|---|
| E3.1 | "LLM 320/450 (72,2%)" | **325/450 (72,2%)** | DB `parsed->skills_info->method` |
| E3.2 | "99% JD (446/450) có ≥1 skill; TB 8,6 skill/JD" | **450/450 (100%); TB 11,7 skill/JD** | DB đếm lại 28/09 |
| E3.3 | "Truy xuất Top-20 ... dưới 0,05 giây (<50ms)" | **Top-30 ứng viên, ~60 ms warm** (lần đầu 441 ms) | đo pgvector 28/09 |
| E3.4 | "thực nghiệm đạt mức tăng điểm trung bình +12 đến +16 điểm" | **+21,4 đến +41,7 (trung vị +33,3)** — cận trên lý thuyết | `data/labeled/improve_delta_report.md` |
| E3.5 | "điểm số tăng từ 72 lên 88" | **33,4 → 66,8 (+33,4)** | đo thật 27/09 |
| E3.6 | "Khảo sát pilot: 100% người dùng đánh giá cao" | **bỏ** (chưa có khảo sát) | — |
| E3.7 | ">70% sinh viên hoang mang", "<10% phản hồi" | **bỏ số** hoặc dẫn nguồn công khai | — |
| E3.8 | "Human-in-the-loop ... chính xác 100%" | **mô tả cơ chế, bỏ số** | — |
