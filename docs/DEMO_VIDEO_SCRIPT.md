# Kịch Bản Quay Video Demo Sản Phẩm (Thời Lượng: 5 Phút)
**Dự án:** aitainang — Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam  
**Phiên bản:** Local Release (FastAPI Backend + React Frontend + 450 JD thật từ `tinixai`)  
**Mục tiêu video:** Minh chứng luồng sản phẩm 6 bước hoạt động thật 100%, nhấn mạnh tính **Giải thích được (Explainable Matching)** và **Đồng hành sửa CV đo được (Delta Score)**.

---

## 1. Phân Bổ Thời Gian Tổng Thể (300 Giây)

| Phân đoạn | Thời lượng | Bước sản phẩm | Nội dung chính & Thao tác | Điểm nhấn kỹ thuật / USP |
|---|---|---|---|---|
| **P1** | 0:00 – 0:35 (35s) | Giới thiệu & Bối cảnh | Nêu nỗi đau: Sinh viên nộp hàng chục CV không có hồi đáp vì không biết CV thiếu gì so với JD. Giới thiệu aitainang. | Định vị: Trợ lý nghề nghiệp AI, không phải chỉ chấm điểm CV. |
| **P2** | 0:35 – 1:15 (40s) | Bước 1: Onboarding | Thao tác trên `/onboarding`: Chọn mục tiêu nghề nghiệp (Backend / Data), địa điểm, kỳ vọng lương, số năm kinh nghiệm. Bấm tiếp tục. | Tạo Career Profile làm context lọc metadata Tầng 3. |
| **P3** | 1:15 – 2:05 (50s) | Bước 2: Upload & Parse CV | Thao tác trên `/upload-cv`: Tải lên file PDF thật. Hiện thanh tiến trình AI đọc CV. Xuất hiện màn hình **Human-in-the-loop**. | **Human-in-the-loop**: Người dùng xác nhận & sửa kỹ năng AI trích xuất (tránh hallucination). Tắt hoàn toàn Demo Badge. |
| **P4** | 2:05 – 2:50 (45s) | Bước 3: Matching CV–JD | Thao tác trên `/matching`: Hiển thị danh sách Top-K JD xếp hạng từ kho **450 JD thật**. Thử click tab lọc "🤖 Data / AI / ML" (75 job thật). | Truy xuất đa chiều: Cosine Similarity embedding + Metadata Filtering (Tầng 3). |
| **P5** | 2:50 – 4:00 (70s) | Bước 4: Kết quả & Giải thích | Thao tác trên `/results`: **TRỌNG TÂM VIDEO**. Xem điểm tổng quan (ví dụ 86%), phân rã 3 chiều Hybrid V2 (Kỹ năng cứng 50%, Ngữ nghĩa 40%, Kỹ năng mềm 10%), xem bảng đối chiếu Evidence trích dẫn từ CV và JD. | **USP #1 - Explainable Matching**: Công thức minh bạch, trích dẫn bằng chứng cụ thể, không hộp đen. |
| **P6** | 4:00 – 4:40 (40s) | Bước 5: Cải thiện CV | Thao tác trên `/improve`: Xem các Gap kỹ năng ưu tiên (ví dụ thiếu Docker, Redis). Xem gợi ý viết lại bullet point cụ thể. Nhấn nút "Chấm lại CV" -> **Hiển thị Delta Score thật (+33,4 điểm, đo thực tế backend: 33,4 → 66,8)**. | **USP #2 - Measurable Loop**: Đo lường sự tiến bộ trước khi nộp đơn. |
| **P7** | 4:40 – 5:00 (20s) | Bước 6: Dashboard & Kết | Thao tác trên `/dashboard`: Xem lịch sử các phiên chấm, tiến độ đóng gap và tổng kết thông điệp. | Đồng hành dài hạn cùng người trẻ Việt Nam. |

---

## 2. Kịch Bản Chi Tiết Từng Cảnh (Lời Thoại & Hành Động)

### Cảnh 1: Mở đầu & Nêu bài toán (0:00 – 0:35)
- **Hình ảnh:** Màn hình chính trang Onboarding `/onboarding`.
- **Lời thuyết minh:**  
  *"Chào Ban Giám Khảo và các bạn, đây là aitainang — nền tảng trợ lý nghề nghiệp cá nhân hóa dành cho sinh viên và fresh graduate Việt Nam. Một sinh viên sắp ra trường thường gặp 3 câu hỏi lớn: Mình hợp với vị trí nào? CV của mình thiếu gì so với JD? Và phải sửa CV như thế nào để được gọi phỏng vấn? Hiện nay, các bạn phải tự đọc hàng chục bản mô tả công việc và tự mò mẫm sửa CV. aitainang ra đời để giải quyết triệt để vấn đề này bằng một pipeline AI 5 tầng minh bạch và có thể kiểm chứng được."*

### Cảnh 2: Onboarding định hướng (0:35 – 1:15)
- **Hình ảnh:** Điền form tại `/onboarding`.
- **Thao tác:** Chọn vị trí mục tiêu là `Backend Developer`, chọn địa điểm `Hà Nội`, kinh nghiệm `Fresher / Junior (0-1 năm)`. Bấm nút *"Tiếp tục: Tải lên CV (Bước 2)"*.
- **Lời thuyết minh:**  
  *"Hành trình bắt đầu với bước Onboarding. Thay vì bắt người dùng tải CV ngay mà không rõ mục đích, aitainang ghi nhận Career Profile gồm vai trò mục tiêu, địa điểm và mức kinh nghiệm mong muốn. Đây là cơ sở để hệ thống lọc metadata ở tầng truy xuất tiếp theo."*

### Cảnh 3: Upload CV & Rà soát Human-in-the-loop (1:15 – 2:05)
- **Hình ảnh:** Màn hình `/upload-cv`.
- **Thao tác:** Tải lên CV kiểm thử (`cv_single_column.pdf`). Tiến trình hiển thị đọc nội dung thô và gọi API backend FastAPI. Ngay sau đó hiển thị màn hình xác nhận kết quả trích xuất cấu trúc. Chỉ chuột vào badge màu xanh lá: Backend API đã kết nối thật và Demo Badge tắt hoàn toàn.
- **Lời thuyết minh:**  
  *"Ở bước 2, khi người dùng tải file CV PDF, backend FastAPI sẽ thực hiện Structured Extraction để bóc tách thông tin thành JSON chuẩn hóa. Điểm mấu chốt ở đây là **cơ chế Human-in-the-loop**: AI không tự ý đưa ra quyết định mà hiển thị toàn bộ kỹ năng, kinh nghiệm và học vấn để người dùng rà soát, bổ sung các kỹ năng bị thiếu hoặc xóa bỏ nhận diện sai trước khi bắt đầu đối chiếu, ngăn chặn hoàn toàn hiện tượng hallucination."*

### Cảnh 4: Matching trên kho JD thật (2:05 – 2:50)
- **Hình ảnh:** Màn hình `/matching`.
- **Thao tác:** Lướt qua danh sách Top việc làm được xếp hạng. Bấm chọn tab `🤖 Data / AI / ML` (hiển thị 75 job thật), sau đó chọn tab `💻 Software Engineering`. Chọn một công việc có điểm khớp cao.
- **Lời thuyết minh:**  
  *"Sau khi xác nhận CV, hệ thống truy xuất và chấm điểm trên kho dữ liệu gồm **450 JD tuyển dụng thật** từ dataset tinixai CC BY-NC 4.0. Chúng tôi hoàn toàn không dùng tên công ty hay vị trí bịa đặt. Từng thẻ việc làm hiển thị mức lương thật, địa điểm thật và điểm số được tính toán từ backend theo thời gian thực."*

### Cảnh 5: Kết quả & Phân rã điểm Explainable (2:50 – 4:00) — **Trọng tâm USP**
- **Hình ảnh:** Màn hình `/results`.
- **Thao tác:**  
  - Chỉ chuột vào vòng tròn điểm số: **86 / 100 điểm**.
  - Rê chuột vào phần **Phân rã điểm (Breakdown)**: Giải thích thanh Kỹ năng cứng (50%), Ngữ nghĩa CV–JD (40%) và Kỹ năng mềm (10%).
  - Cuộn xuống phần **Bằng chứng đối chiếu (Evidence)**: Đọc trích dẫn trích từ CV và đoạn trích từ JD công ty tuyển dụng thật.
  - Chỉ vào danh sách Kỹ năng đáp ứng và Khoảng trống kỹ năng (Gaps).
- **Lời thuyết minh:**  
  *"Đây chính là điểm cốt lõi tạo nên sự khác biệt của aitainang: **Explainable AI Matching**. Thay vì trả về một con số hộp đen gây hoang mang, chúng tôi công khai phân rã điểm theo công thức Hybrid V2: 50% kỹ năng cứng, 40% độ tương đồng ngữ nghĩa bằng embedding đa ngôn ngữ, và 10% kỹ năng mềm.  
  Đặc biệt, hệ thống cung cấp **Evidence trích dẫn trực tiếp** từ cả bản CV của ứng viên lẫn yêu cầu thực tế trong JD, giải thích cặn kẽ tại sao ứng viên đạt điểm số đó và những khoảng trống kỹ năng cụ thể cần cải thiện."*

### Cảnh 6: Vòng lặp cải thiện CV & Đo lường Delta Score (4:00 – 4:40)
- **Hình ảnh:** Màn hình `/improve`.
- **Thao tác:** Bấm nút *"Tiếp tục: Cải thiện CV"*. Xem danh sách Gap ưu tiên, xem ví dụ viết lại bullet point hành động theo phương pháp STAR. Nhấn *"Chấm lại CV đã sửa"* để thấy điểm tăng từ **33,4 lên 66,8 (+33,4 điểm — số đo thật từ backend, cặp CV cv_member_01_backend × JD Kỹ Sư Quản Trị Hệ Thống)**.
- **Lời thuyết minh:**  
  *"Từ các khoảng trống kỹ năng vừa phát hiện, Bước 5 đồng hành cùng ứng viên sửa CV. AI đưa ra gợi ý viết lại từng gạch đầu dòng cụ thể, bám sát từ khóa và định dạng STAR. Sau khi chỉnh sửa, ứng viên bấm chấm lại ngay để thấy **Delta Score** — sự gia tăng điểm số đo lường được trước khi chính thức bấm gửi hồ sơ ứng tuyển."*

### Cảnh 7: Dashboard theo dõi & Kết luận (4:40 – 5:00)
- **Hình ảnh:** Màn hình `/dashboard`.
- **Thao tác:** Lướt xem lịch sử các phiên đối chiếu và tiến độ lấp đầy gap kỹ năng.
- **Lời thuyết minh:**  
  *"Toàn bộ quá trình được lưu lại trên Dashboard cá nhân, giúp người trẻ theo dõi sự tiến bộ nghề nghiệp theo thời gian. aitainang tự hào mang lại một giải pháp chạy được, kiểm chứng được và minh bạch cho cộng đồng sinh viên Việt Nam. Cảm ơn Ban Giám Khảo đã theo dõi!"*
