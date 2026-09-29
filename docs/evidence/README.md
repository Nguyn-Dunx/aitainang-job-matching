# Thư mục lưu trữ Minh chứng & Ảnh chụp màn hình hệ thống (Evidence)

> **Mục đích**: Lưu trữ toàn bộ ảnh chụp màn hình (screenshots) và video ghi hình (recordings)
> làm minh chứng cho **Mục 6 (Sản phẩm & Luồng người dùng)**, **Mục 8 (Kết quả thử nghiệm)** và
> **Mục 13 (Prompt Log & Minh chứng)** trong Hồ sơ Mẫu 3.
> 
> Các file này được commit trực tiếp vào repo `prj/docs/evidence/` thay vì lưu tạm trong cache IDE.

---

## Danh mục Minh chứng hiện có

| File | Mô tả | Minh chứng cho |
|------|-------|----------------|
| `step1_onboarding.png` | Form Career Profile (mục tiêu nghề, kinh nghiệm, địa điểm, mức lương, kỹ năng taxonomy) | Luồng Bước 1 |
| `step2_upload_cv_1790354928154.png` | Vùng tải lên CV (drag-drop, PDF/DOCX) | Luồng Bước 2 |
| `human_in_the_loop_review.png` | Màn hình rà soát Human-in-the-loop: thông tin, học vấn, kỹ năng AI trích xuất, trách nhiệm công việc | Cơ chế Human-in-the-loop (Tầng 2) |
| `step3_matching.png` | Danh sách Top-K JD xếp hạng theo độ khớp kèm thẻ thông tin chi tiết | Luồng Bước 3 |
| `step3_matching_real_jds.png` | Giao diện nạp 450 JD THẬT, tab Data/AI/ML hiển thị đúng 75 job, badge Demo Mode | Kiểm thử D1 thật & Tab Data/AI |
| `results_breakdown_evidence.png` | Kết quả chi tiết: Gauge điểm, phân rã 4 chiều, so khớp kỹ năng | Explainable AI (Tầng 4) |
| `step4_results_real_jds.png` | Kết quả chi tiết với công ty thật và trích dẫn yêu cầu thật từ tinixai | Minh chứng Explainability thật |
| `verify_real_jds.webp` | Video ghi hình kiểm thử nạp 450 JD thật và lọc 75 job Data/AI/ML | Demo kiểm thử dữ liệu thật |
| `step5_improve.png` | Đề xuất cải thiện CV theo thứ tự ưu tiên, ví dụ viết lại bullet point cụ thể, Delta Score | CV Improvement Loop (Tầng 5) |
| `step6_dashboard.png` | Dashboard theo dõi: tổng delta score, lịch sử các phiên chấm, tiến độ đóng gap kỹ năng | Luồng Bước 6 |
| `step1_step2_flow_1790419419298.webp` | Video ghi hình luồng kiểm thử thực tế từ Bước 1 đến Bước 6 trên trình duyệt | Demo tương tác |
| `verify_all_pages_1790354857431.webp` | Video ghi hình chuyển trang và điều hướng 6 bước | Điều hướng UI |

---

> [!NOTE]
> Mọi ảnh và video minh chứng mới khi tạo ra phải được lưu trực tiếp vào thư mục `docs/evidence/` này.
