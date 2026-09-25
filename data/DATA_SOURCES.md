# DATA_SOURCES.md — Kê khai nguồn dữ liệu

> Tài liệu này là minh chứng cho **mục 3 — Hồ sơ Mẫu 3** (Dữ liệu & tính hợp lệ).
> Mọi thay đổi phải được commit kèm mô tả rõ ràng.

---

## D1 — JD thật, ngành CNTT / Data

| # | Nguồn | Loại nguồn | Ngày thu thập | Số lượng JD | Ghi chú / Điều khoản sử dụng |
|---|-------|-----------|--------------|------------|------------------------------|
| 1 | Nhóm Facebook "Tuyển dụng IT …" | Bài đăng công khai | 2026-09-xx | … | JD là thông tin tuyển dụng công khai; chỉ lấy phần mô tả công việc, không lấy thông tin cá nhân người đăng |
| 2 | TopDev — trang listing công khai | Trang tuyển dụng | 2026-09-xx | … | Dữ liệu listing công khai, không cần đăng nhập; tuân thủ robots.txt |
| 3 | ITviec — trang listing công khai | Trang tuyển dụng | 2026-09-xx | … | Như trên |

> **Lưu ý**: Chỉ thu thập phần **mô tả công việc** (title, requirements, responsibilities,
> level, location). Không lưu tên công ty nếu không cần thiết cho mục đích matching.
> Không thu thập thông tin cá nhân ứng viên/người đăng.

### Quy trình thu thập D1
1. Copy nội dung JD từ bài đăng/listing công khai.
2. Dán vào file `data/raw/jd_batch_<YYYYMMDD>.txt`, mỗi JD phân cách bằng dòng `===`.
3. Chạy script `scripts/parse_raw_jds.py` để chuẩn hóa thành JSON.
4. Review các JD có cờ `needs_review: true`, bổ sung trường thiếu.
5. JD đã duyệt lưu tại `data/processed/jds.json`.

---

## D2 — CV mẫu

| # | Nguồn | Đồng ý | Ẩn danh | Số lượng | Ghi chú |
|---|-------|--------|---------|---------|---------|
| 1 | CV thành viên nhóm (3 người) | Có — tự nguyện | Đã xóa: tên, SĐT, email, ảnh, địa chỉ | 3 | — |
| 2 | CV bạn bè (có xin phép văn bản) | Có — tin nhắn/email lưu lại | Như trên | … | Lưu bằng chứng đồng ý tại `data/consent/` |
| 3 | CV tổng hợp (synthetic) | N/A | N/A | … | Sinh bởi LLM từ template tự viết, không dựa trên CV thật của người lạ |

### Quy trình ẩn danh CV
- Xóa hoàn toàn: họ tên, SĐT, email, địa chỉ cụ thể, ảnh đại diện, link mạng xã hội cá nhân.
- Thay thế: tên → `Ứng viên A/B/C…`, email → `candidate_X@example.com`.
- File gốc **không** được commit vào repo; chỉ commit bản đã ẩn danh.

---

## D3 — Bộ đánh giá có nhãn (CV, JD)

| Hạng mục | Chi tiết |
|----------|---------|
| Quy mô | 50–100 cặp (CV, JD) |
| Cách ghép | Chọn ngẫu nhiên phân tầng từ D1 × D2 (đảm bảo đủ mức easy/medium/hard) |
| Người chấm | 3 thành viên, chấm độc lập thang 1–5 |
| Tiêu chí | Mức phù hợp tổng thể: 1 = không liên quan, 5 = rất phù hợp |
| Ghi chú lý do | Bắt buộc — mỗi điểm kèm 1–2 câu giải thích ngắn |
| Đo đồng thuận | Fleiss' kappa / Krippendorff's alpha — báo cáo trong mục 7, 9 |
| File kết quả | `data/labeled/annotations.csv` |

---

## D4 — Taxonomy kỹ năng song ngữ

| Hạng mục | Chi tiết |
|----------|---------|
| Quy mô mục tiêu | 200–500 mục + alias |
| Phương pháp xây | Thống kê tần suất kỹ năng trong D1, nhóm alias thủ công |
| Ngôn ngữ | Mỗi mục có tên tiếng Anh (canonical) + tên tiếng Việt + danh sách alias |
| Ví dụ | `{ "canonical": "Python", "vi": "Python", "aliases": ["python3", "python 3.x", "lập trình Python"] }` |
| File | `data/taxonomy/skills_taxonomy.json` |

---

## Cam kết đạo đức dữ liệu

- **Không** thu thập CV của người lạ từ bất kỳ nguồn nào (TopCV, LinkedIn, VietnamWorks…).
- **Không** lưu thông tin cá nhân (tên, SĐT, email, ảnh) vào repo.
- JD là thông tin tuyển dụng công khai — ghi rõ nguồn và ngày thu thập.
- Mọi CV đều có sự đồng ý rõ ràng bằng văn bản và đã ẩn danh hoàn toàn.
- Bằng chứng đồng ý lưu tại `data/consent/` (không commit lên GitHub public).
