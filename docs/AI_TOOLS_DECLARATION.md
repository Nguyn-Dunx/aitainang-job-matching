# Kê khai công cụ AI & nguồn mở sử dụng trong dự án

> Mục đích: minh bạch phần nào đội tự viết, phần nào có AI hỗ trợ, phần nào kế thừa
> nguồn mở/dữ liệu công khai — phục vụ tính trung thực học thuật của hồ sơ dự thi.

## 1. Công cụ AI hỗ trợ phát triển (development-time)

| Công cụ | Dùng cho | Phạm vi |
|---------|----------|---------|
| Antigravity IDE + mô hình AI trong terminal (coding agent) | Hỗ trợ viết/review code backend, script xử lý dữ liệu, test, tài liệu nháp | Code do AI sinh đều được thành viên phụ trách chạy kiểm chứng (pytest, truy vấn DB thật) trước khi commit; mọi quyết định thiết kế (công thức chấm, taxonomy, tiêu chí đánh giá) do đội chốt |
| LLM qua API (xem mục 2) | Sinh CV synthetic phục vụ test (nhân vật hư cấu), hỗ trợ trích xuất kỹ năng | CV synthetic chỉ dùng nội bộ kiểm thử, không phải dữ liệu đánh giá chính thức |

## 2. Mô hình AI dùng TRONG sản phẩm (runtime)

| Thành phần | Mô hình / dịch vụ | Vai trò trong hệ thống |
|-----------|-------------------|------------------------|
| LLM trích xuất kỹ năng | `moonshotai/kimi-k3` qua **OpenRouter** (fallback `nvidia/nemotron-3-ultra-550b-a55b`), temperature=0, structured JSON | Tầng 2: trích skill từ CV/JD về canonical name trong taxonomy; lỗi thì fallback rule (regex alias) |
| Embedding | **BGE-M3** (`BAAI/bge-m3`, sentence-transformers 6.1.0), 1024 chiều, chạy local CPU | Tầng 3: biểu diễn ngữ nghĩa CV/JD cho semantic score + vector search |
| Chấm điểm | **Công thức deterministic do đội tự thiết kế** (0,5 hard_skill + 0,1 soft_skill + 0,4 semantic) | Tầng 4 — KHÔNG dùng LLM trong công thức chính, đảm bảo minh bạch/tái lập |

## 3. Framework & hạ tầng nguồn mở

| Hạng mục | Công nghệ | Giấy phép |
|----------|-----------|-----------|
| Backend | FastAPI (Python 3.12) | MIT |
| Frontend | React + Vite | MIT |
| Database | PostgreSQL + pgvector 0.8.6, host serverless qua **Neon** (ap-southeast-1) | PostgreSQL License / Apache-2.0 |
| PDF parsing | PyMuPDF | AGPL (dùng cho mục đích phi thương mại, mã nguồn dự án công khai) |
| Embedding runtime | sentence-transformers | Apache-2.0 |

## 4. Dữ liệu

| Tập | Nguồn | Giấy phép / cam kết |
|-----|-------|---------------------|
| D1 — 450 JD thật | Dataset công khai `tinixai/vietnamese-job-descriptions` (HuggingFace) | **CC BY-NC 4.0** — phi thương mại, đã ghi công trong README + hồ sơ |
| D2 — CV mẫu | CV thành viên + bạn bè có **đồng ý bằng văn bản** (`data/consent/`), ẩn danh hoàn toàn; CV synthetic do LLM sinh (nhân vật hư cấu) | Không thu thập CV người lạ từ bất kỳ nguồn nào |
| D3 — Bộ nhãn | 3 thành viên tự chấm tay độc lập (AI không chấm hộ) | Guideline tại `data/labeled/ANNOTATION_GUIDE.md` |
| D4 — Taxonomy 235 skill / 690 alias | **Đội tự xây** (seed thủ công + mở rộng theo tần suất JD thật) | Tài sản của đội |

## 5. Phân định đóng góp

- **Đội tự viết/tự thiết kế**: taxonomy D4; công thức chấm V2 và quyết định tách
  hard/soft skill; pipeline 4 tầng; guideline chấm D3; toàn bộ quyết định kiến trúc
  và lựa chọn công nghệ; việc chấm nhãn ground truth.
- **AI hỗ trợ (có người kiểm chứng)**: một phần code backend/script/test được sinh
  với sự hỗ trợ của coding agent, sau đó chạy kiểm chứng thật (24 test, truy vấn DB,
  curl API) trước khi merge; CV synthetic; nháp tài liệu (con người duyệt lần cuối).
- **Kế thừa nguồn mở/dữ liệu công khai**: như bảng mục 3 và 4 — tất cả đều ghi rõ
  nguồn và giấy phép.
