# Kịch bản kỹ thuật cho video demo (C quay)

> Mô tả ĐÚNG những gì code thực sự làm khi 1 CV được upload — đọc nguyên văn hoặc
> diễn giải tự do đều được, miễn giữ đúng các con số và tên thành phần.

## Luồng xử lý 1 CV upload (4 tầng)

- **Tầng 1 — Đọc CV**: hệ thống dùng thư viện `pymupdf` tách text và các mục
  (kinh nghiệm, kỹ năng, học vấn) từ file PDF. Nếu CV là ảnh scan, hệ thống phát hiện
  và cảnh báo thay vì đoán sai.
- **Tầng 2 — Hiểu kỹ năng**: một LLM (Kimi-K3 qua OpenRouter) đọc CV và trích kỹ năng
  về **tên chuẩn** trong taxonomy song ngữ 235 kỹ năng / 690 alias do nhóm tự xây —
  ví dụ "py", "Python3" đều quy về `Python`. Nếu LLM lỗi, hệ thống tự chuyển sang
  chế độ rule (regex trên alias) nên pipeline không bao giờ chết — thực tế 27,8% JD
  đang chạy bằng rule.
- **Tầng 3 — Biểu diễn ngữ nghĩa**: CV được embed bằng model **BGE-M3** (vector 1024
  chiều, hỗ trợ tiếng Việt tốt). 450 JD thật trong hệ thống cũng đã được embed sẵn
  và lưu trong PostgreSQL + pgvector.
- **Tầng 4 — Lọc & chấm điểm**:
  1. Lọc cứng theo lựa chọn của người dùng (địa điểm / cấp bậc / nhóm ngành).
  2. Vector search lấy top JD gần nhất về ngữ nghĩa.
  3. Chấm điểm bằng **công thức công khai**:
     `điểm = 0,5 × khớp kỹ năng cứng + 0,1 × kỹ năng mềm + 0,4 × độ tương đồng ngữ nghĩa`
  4. Mỗi điểm đều kèm **breakdown 3 chiều + bằng chứng** (skill nào khớp, skill nào
     còn thiếu, trích đoạn JD) — không phải hộp đen.

## Thông điệp chốt cho video

- "Điểm số minh bạch": mọi điểm đều giải thích được từng phần, có trích dẫn JD gốc.
- "Dữ liệu thật": 450 JD thật từ dataset công khai (CC BY-NC), 369 công ty.
- "Đánh giá nghiêm túc": hệ thống được đo bằng 4 biến thể ablation
  (keyword-only / embedding-only / LLM-only / hybrid) trên bộ nhãn chấm tay 3 người,
  kèm chỉ số đồng thuận Fleiss' kappa — không tự khoe điểm.
- "Sẵn sàng mở rộng": kiến trúc module theo tầng, thay model embedding hay LLM chỉ
  cần đổi config.

## Số liệu được phép nói trong video (đã kiểm chứng)

| Con số | Giá trị |
|--------|---------|
| JD thật trong hệ thống | 450 (369 công ty) |
| Taxonomy kỹ năng | 235 skill, 690 alias, song ngữ |
| Tỷ lệ trích xuất LLM / rule | 72,2% / 27,8% |
| Embedding | BGE-M3, 1024 chiều |
| Thời gian xử lý 1 CV upload (E2E) | ~25 giây (gồm LLM); nhanh hơn nhiều ở mode rule |
| Công thức chấm | 0,5 hard skill + 0,1 soft skill + 0,4 semantic |

## KHÔNG được nói trong video

- Không trích số liệu pilot (Precision@5, Spearman...) — đó là nhãn cơ chế để kiểm
  chứng pipeline, chưa phải kết quả đánh giá chính thức.
- Không hứa tính năng OCR cho CV ảnh scan (ngoài phạm vi).
