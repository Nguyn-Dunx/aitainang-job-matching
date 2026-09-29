# Bảng delta Tầng 5 — 3 CV nội bộ × top-3 match thật (28/09/2026)

> **Bản chất số liệu:** điểm ƯỚC TÍNH theo giả định người dùng xác nhận thêm toàn bộ kỹ năng cứng còn thiếu (cận trên lý thuyết, không qua LLM sinh gợi ý, không tính gap soft-skill). Semantic giữ nguyên (không re-embed CV sau khi sửa).
> Top-3 match lấy từ đúng luồng matching thật (pgvector → score_pair → xếp hạng), không chọn tay.

| # | CV | JD | Số skill thiếu (hard) | Trước | Sau | Delta |
|---|---|---|---|---|---|---|
| 1 | cv_member_01_backend.json | Backend Developer (Node.JS/PHP) | Kinh Nghiệm 3 Năm | Đi Làm Ngay Tại Vạn Phúc City Thủ Đức Hồ Chí Minh | 9 | 50.8 | 80.8 | **+30.0** |
| 2 | cv_member_01_backend.json | BackEnd Engineer (Python And/Or Golang) | 19 | 48.3 | 83.5 | **+35.2** |
| 3 | cv_member_01_backend.json | Thực Tập Sinh Python / Django / Odoo | 10 | 46.4 | 79.7 | **+33.3** |
| 4 | cv_member_02_data_ai.json | Data Analyst (Middle, HCM) | 9 | 42.4 | 79.9 | **+37.5** |
| 5 | cv_member_02_data_ai.json | Business Intelligence Analyst | 5 | 40.6 | 82.3 | **+41.7** |
| 6 | cv_member_02_data_ai.json | Data Analyst | 7 | 39.3 | 78.2 | **+38.9** |
| 7 | cv_member_03_frontend_product.json | IT Frontend Developer (ReactJS) | 3 | 58.6 | 80.0 | **+21.4** |
| 8 | cv_member_03_frontend_product.json | Frontend Developer | 3 | 54.8 | 84.8 | **+30.0** |
| 9 | cv_member_03_frontend_product.json | Intern Frontend (ReactJS/ VueJS) | 6 | 53.8 | 83.8 | **+30.0** |

- Số cặp: 9
- Delta min: **+21.4**
- Delta median: **+33.3**
- Delta max: **+41.7**

_Ghi chú: đây là cận trên lý thuyết cho mục đích kiểm chứng cơ chế chấm lại điểm; delta thật khi người dùng chỉ xác nhận một phần gợi ý sẽ thấp hơn._