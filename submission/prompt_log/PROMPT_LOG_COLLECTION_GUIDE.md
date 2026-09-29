# Hướng Dẫn Thu Thập & Gộp Prompt Log Toàn Dự Án
**Quy định:** Bắt buộc nộp minh chứng theo Điều 5.7 Thể lệ Cuộc thi & Mục 13 Hồ sơ Mẫu 3.

---

## 1. Cấu Trúc Thư Mục Google Drive (Dùng để nộp BGK)
Tạo 1 thư mục trên Google Drive của nhóm với tên:  
📁 `aitainang_2026_BangC_Prompt_Logs`  
Cấu hình quyền truy cập: **"Bất kỳ ai có đường liên kết đều có thể xem (Viewer)"**.

Bên trong thư mục gồm các tệp/thư mục con:
```
aitainang_2026_BangC_Prompt_Logs/
├── README_PROMPT_LOG.pdf               <- Giới thiệu tổng quan quy trình làm việc với AI
├── 01_ChienLuoc_Va_KienTruc_Chung.md   <- Toàn bộ trao đổi chiến lược định hướng ban đầu
├── 02_ThanhVien_A_Data_Va_Retrieval/   <- Toàn bộ log của Thành viên A (Data, Taxonomy, pgvector)
│   ├── conversation_session_01.md
│   └── conversation_session_02.md
├── 03_ThanhVien_B_Backend_Va_Scoring/  <- Toàn bộ log của Thành viên B (FastAPI, Hybrid V2, Tests)
│   ├── conversation_session_01.md
│   └── conversation_session_02.md
├── 04_ThanhVien_C_Product_Va_Frontend/ <- Toàn bộ log của Thành viên C (UI 6 bước, E2E, Video demo)
│   ├── conversation_session_01.md
│   └── conversation_session_02.md
└── 05_TongHop_NhatKy_PROMPT_LOG.md     <- Tệp đồng bộ từ docs/PROMPT_LOG.md trong repo Git
```

---

## 2. Cách Xuất (Export) Lịch Sử Hội Thoại Antigravity

Mỗi thành viên chạy công cụ Antigravity có thể lấy toàn bộ lịch sử phiên làm việc từ đường dẫn lưu trữ cục bộ:
- **Đường dẫn trên Windows**:  
  `C:\Users\<Tên_User>\.gemini\antigravity-ide\brain\<conversation-id>\.system_generated\logs\transcript_full.jsonl`
- **Cách chuyển sang Markdown dễ đọc**:
  - Có thể dùng tính năng Export Chat / Share Chat trên thanh công cụ của Antigravity IDE (nếu có).
  - Hoặc copy các khối văn bản trao đổi chiến lược và mã lệnh chính lưu thành file `.md` hoặc `.txt`.
  - Giữ nguyên nội dung gốc: câu lệnh của người dùng (User Prompt) và phản hồi của AI (Assistant Response).

---

## 3. Checklist Kiểm Tra Trước Khi Gửi Link
- [ ] Đã gom đủ log của cả 3 thành viên (A, B, C) và log chỉ đạo chiến lược chung.
- [ ] Đã loại bỏ/che mờ các API key bí mật (`nvapi-...`, `sk-or-v1-...`) trong file log nếu lỡ xuất hiện.
- [ ] Đã mở quyền truy cập Google Drive sang chế độ công khai: **"Anyone with the link can view"**.
- [ ] Đã dán đường link Google Drive vào Mục 13 của `docs/mau3_draft.md` và `docs/PROMPT_LOG.md`.
