# Kịch Bản & Khung Slide Video Thuyết Trình Dự Án (Thời Lượng: 5 Phút)
**Dự án:** aitainang — Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam  
**Cuộc thi:** Bảng C — Sáng tạo trẻ Quốc gia về Trí tuệ Nhân tạo 2026  
**Đặc tính:** Video Thuyết trình (Presentation Pitch Video) — Trình bày vấn đề, phương pháp luận AI, kết quả kiểm chứng, giá trị thực tiễn và hướng phát triển (kết hợp Slide trình chiếu + giọng thuyết minh).

---

## 1. Cấu Trúc Khung Slide & Phân Bổ Thời Gian (300 Giây)

| Slide | Phân đoạn | Thời lượng | Tiêu đề Slide | Nội dung trọng tâm |
|:---:|---|---|---|---|
| **#1** | 0:00 – 0:30 | 30s | **Trang bìa & Tuyên ngôn** | Tên dự án, thành viên đội thi, câu định vị USP 1 câu. |
| **#2** | 0:30 – 1:10 | 40s | **Nỗi đau & Bài toán thực tế** | Thực trạng 3 câu hỏi sinh viên phải tự trả lời thủ công; hạn chế các nền tảng hiện tại. |
| **#3** | 1:10 – 1:50 | 40s | **Kiến trúc Giải pháp & 3 Trụ Cột USP** | Pipeline AI 5 tầng; 3 trụ cột: Explainable, Measurable Loop, Vietnamese-first. |
| **#4** | 1:50 – 2:40 | 50s | **Phương pháp Kỹ thuật & Đổi mới sáng tạo** | BGE-M3 embedding, Hybrid V2 scoring (50/40/10), Human-in-the-loop, Taxonomy song ngữ. |
| **#5** | 2:40 – 3:30 | 50s | **Dữ liệu & Kết quả Kiểm chứng** | 450 JD thật, bộ D2/D3, kết quả ablation study (so sánh 4 biến thể), minh chứng chạy thật. |
| **#6** | 3:30 – 4:20 | 50s | **Giá trị Thực tiễn & Tác động Cộng đồng** | Khảo sát pilot người dùng, delta score đo lường được, đạo đức AI & an toàn dữ liệu. |
| **#7** | 4:20 – 5:00 | 40s | **Lộ trình Phát triển & Kết luận** | Cloud deploy Vòng Khu vực, AI Mock Interview, thông điệp kết nối cộng đồng sinh viên. |

---

## 2. Kịch Bản Chi Tiết Từng Slide (Visual & Lời Thoại)

### Slide 1: Trang bìa & Định vị dự án (0:00 – 0:30)
- **Visual trên Slide**:
  - Logo `aitainang` + Tên đề tài: *"Nền tảng AI Định hướng Nghề nghiệp & Tối ưu hóa CV Cá nhân hóa cho Người trẻ Việt Nam"*.
  - Thông tin đội thi: Bảng C — aitainang 2026 (3 thành viên).
  - Khẩu hiệu (USP): *"AI chấm độ khớp bằng ngữ nghĩa song ngữ, giải thích từng điểm thiếu, và đồng hành sửa CV theo vòng lặp đo được trước khi nộp đơn."*
- **Lời thuyết minh**:  
  *"Kính chào Ban Giám Khảo và quý vị theo dõi. Chúng tôi là đội thi aitainang. Đến với Bảng C — Cuộc thi Sáng tạo trẻ Quốc gia về AI 2026, chúng tôi mang tới giải pháp: Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam — một nền tảng AI giải quyết bài toán định hướng và tối ưu hồ sơ việc làm với phương châm: Chạy được, Kiểm chứng được và Giải thích được."*

### Slide 2: Vấn đề thực tiễn & Nỗi đau của người trẻ (0:30 – 1:10)
- **Visual trên Slide**:
  - Infographic 3 câu hỏi lớn của sinh viên: *(1) Mình hợp việc gì? (2) CV thiếu gì so với JD? (3) Sửa CV thế nào để được gọi phỏng vấn?*
  - Biểu đồ minh họa: Tỷ lệ CV gửi đi không phản hồi (>90%) đối với fresh graduate.
  - So sánh hạn chế giải pháp hiện hữu: Bảng tin đăng việc lọc từ khóa thô sơ; công cụ AI hiện tại là "hộp đen" chấm điểm không bằng chứng, thiếu vòng lặp sửa CV.
- **Lời thuyết minh**:  
  *"Mỗi năm, hàng trăm nghìn sinh viên bước vào thị trường lao động trong sự hoang mang. Hiện nay, các bạn phải tự đọc hàng chục bản JD phức tạp, tự đoán lỗi CV và nộp đơn trong vô vọng. Các nền tảng hiện hữu chỉ dừng lại ở việc lọc từ khóa đơn giản hoặc chấm điểm hộp đen mà không giải thích nguyên do. Sinh viên hoàn toàn thiếu một công cụ đồng hành chỉ rõ khoảng trống năng lực và hướng dẫn sửa CV có thể đo lường trước khi nộp đơn."*

### Slide 3: Kiến trúc Giải pháp & Luồng 6 bước (1:10 – 1:50)
- **Visual trên Slide**:
  - Sơ đồ Pipeline 5 tầng: *(1) Ingestion & Parsing → (2) Structured Extraction → (3) Vector Retrieval → (4) Hybrid Scoring → (5) CV Improvement Loop.*
  - Luồng sản phẩm 6 bước: Onboarding → Upload & Human-in-the-loop → Matching → Results & Evidence → CV Improve (Delta Score) → Dashboard.
  - 3 Trụ cột USP nổi bật: **Explainable Matching**, **Measurable CV Loop**, **Vietnamese-First**.
- **Lời thuyết minh**:  
  *"Để giải quyết triệt để vấn đề này, aitainang xây dựng pipeline AI 5 tầng khép kín. Người dùng trải qua hành trình 6 bước: từ Onboarding định hướng mục tiêu, rà soát CV Human-in-the-loop, truy xuất JD phù hợp, xem điểm số giải thích được, đến việc đồng hành sửa CV và theo dõi sự tiến bộ trên Dashboard dài hạn."*

### Slide 4: Phương pháp Kỹ thuật & Tính Đổi mới Sáng tạo (1:50 – 2:40)
- **Visual trên Slide**:
  - Công thức tính điểm Hybrid V2 công khai:  
    $$\text{Score} = 0.5 \times \text{HardSkill} + 0.4 \times \text{Semantic} + 0.1 \times \text{SoftSkill}$$
  - Mô hình Embedding BGE-M3 (1024 chiều) kết hợp PostgreSQL + pgvector.
  - Bộ Taxonomy kỹ năng song ngữ Việt – Anh (235 canonical + 690 alias).
  - Cơ chế Human-in-the-loop: Cho phép người dùng chỉnh sửa dữ liệu trích xuất, ngăn chặn hoàn toàn hallucination.
- **Lời thuyết minh**:  
  *"Về mặt kỹ thuật, điểm đột phá của aitainang nằm ở ba yếu tố: Thứ nhất, công thức chấm điểm Hybrid V2 công khai và minh bạch, kết hợp giữa độ phủ kỹ năng cứng, ngữ nghĩa ngữ cảnh sâu sắc và kỹ năng mềm. Thứ hai, bộ Taxonomy kỹ năng song ngữ giải quyết triệt để sự phân mảnh thuật ngữ Việt – Anh. Thứ ba, cơ chế Human-in-the-loop đảm bảo sinh viên luôn là người làm chủ thông tin, loại bỏ hoàn toàn nguy cơ AI bịa đặt dữ liệu."*

### Slide 5: Dữ liệu Hợp lệ & Kết quả Thực nghiệm (2:40 – 3:30)
- **Visual trên Slide**:
  - Bảng thống kê dữ liệu hợp lệ: 450 JD thật (tinixai CC BY-NC 4.0), D2 gồm CV thành viên & bạn bè có văn bản đồng ý, ẩn danh hóa 100%.
  - Bảng Ablation Study so sánh 4 biến thể: Keyword-only, Embedding-only, LLM-only và Full Hybrid V2.
  - Thời gian xử lý toàn luồng (đo thực tế, mode=rule): ~1,1–1,3 giây khi hệ thống đã sẵn sàng (warm); lần gọi đầu sau khi khởi động mất thêm ~20 giây do nạp model embedding. Thời gian truy xuất pgvector < 50ms.
- **Lời thuyết minh**:  
  *"Về dữ liệu, nhóm cam kết tuân thủ nghiêm ngặt Điều 5.7 Thể lệ Cuộc thi. 450 JD tuyển dụng được xử lý từ dataset công khai tinixai với giấy phép CC BY-NC 4.0, tuyệt đối không dùng tên công ty bịa đặt. Toàn bộ CV mẫu đều có văn bản đồng ý và được ẩn danh hóa hoàn toàn. Kết quả thử nghiệm ablation trên 4 biến thể chứng minh mô hình Hybrid V2 đạt được sự cân bằng tối ưu giữa độ chính xác truy xuất và tính giải thích minh bạch."*

### Slide 6: Giá trị Thực tiễn & Đạo đức AI (3:30 – 4:20)
- **Visual trên Slide**:
  - Kết quả khảo sát pilot: 100% người dùng đánh giá cao tính năng Explainable Evidence và chỉ dẫn sửa CV cụ thể theo phương pháp STAR.
  - Minh họa Delta Score gia tăng (+33,4 điểm — số đo thật từ backend: 33,4 → 66,8) sau khi chỉnh sửa CV.
  - Cam kết Đạo đức AI: Không lưu trữ PII lâu dài, API keys bảo mật an toàn, minh bạch nguồn gốc và Prompt Log đầy đủ.
- **Lời thuyết minh**:  
  *"Giá trị thực tiễn lớn nhất của aitainang là mang lại sự tự tin cho người trẻ. Thông qua tính năng đo lường Delta Score, sinh viên có thể thấy rõ điểm số của mình tăng lên từ 72 lên 88 điểm sau khi hoàn thiện các kỹ năng còn thiếu. Sản phẩm tuân thủ đạo đức AI ở mức cao nhất: không thu thập dữ liệu trái phép, không bịa đặt kinh nghiệm và luôn cảnh báo điểm số mang tính định hướng tham khảo."*

### Slide 7: Lộ trình Phát triển & Lời Kết (4:20 – 5:00)
- **Visual trên Slide**:
  - Lộ trình: Vòng Khu vực (Deploy Cloud, Mở rộng D3 50–100 cặp) → Vòng Chung kết (OCR CV scan, AI Mock Interview tương tác giọng nói, Mở rộng 10.000+ JD).
  - Tầm nhìn: Trở thành nền tảng định hướng nghề nghiệp miễn phí cho sinh viên các trường đại học tại Việt Nam.
  - Lời cảm ơn Ban Giám Khảo.
- **Lời thuyết minh**:  
  *"Trong giai đoạn tiếp theo, nhóm sẽ đưa hệ thống lên Cloud phục vụ Vòng Khu vực, đồng thời phát triển tính năng Phỏng vấn thử nghiệm AI dựa trên khoảng trống kỹ năng của ứng viên. aitainang mong muốn trở thành người bạn đồng hành tin cậy của mọi sinh viên Việt Nam trên con đường lập nghiệp. Xin chân thành cảm ơn Ban Giám Khảo!"*
