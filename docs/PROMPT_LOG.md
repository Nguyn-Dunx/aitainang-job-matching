# Prompt Log — aitainang (Bảng C, 2026)

Bắt buộc nộp theo Điều 5.7 / mục 13 Mẫu 3. Sau mỗi thay đổi đáng kể, thêm một dòng theo mẫu:

```
[PROMPT LOG] Việc: ... | AI tạo: ... | Người xác nhận/sửa: ... | Ghi chú: ...
```

## Nhật ký

[PROMPT LOG] Việc: T1 — khởi tạo repo, skeleton FastAPI, schema DB (CV/JD/MatchResult + pgvector), CI ruff+pytest | AI tạo: toàn bộ cấu trúc app/, requirements, docker-compose, CI, README | Người xác nhận/sửa: B (AI/Backend Lead) | Ghi chú: LLM SDK chưa chốt — chờ xác nhận API key provider
[PROMPT LOG] Việc: T2/T3 — Nạp 450 JD thật từ tinixai, lọc chuẩn 75 job Data/AI/ML, nối endpoint POST /api/cv/upload backend thật | AI tạo: apiService.js, tích hợp UploadCVPage/MatchingPage/ResultsPage với Hybrid V2 scoring | Người xác nhận/sửa: C (Product/Frontend Lead) | Ghi chú: Demo mode badge tắt tự động khi gọi API thật thành công, lưu toàn bộ minh chứng vào docs/evidence/
[PROMPT LOG] Việc: T3/T4 — Chuẩn hóa đường dẫn D2 tại data/cv_samples/, tạo 3 CV nội bộ ẩn danh, sửa ResultsPage hiển thị đúng 3 chiều Hybrid V2 (xóa bỏ số liệu kinh nghiệm/học vấn cũ), hoàn thiện toàn bộ mục 1, 2, 8, 11, 12 Mẫu 3 | AI tạo: Cập nhật ResultsPage.jsx, DEMO_VIDEO_SCRIPT.md, mau3_draft.md, tạo 3 file CV JSON và hướng dẫn gom Prompt Log | Người xác nhận/sửa: C (Product/Frontend Lead) | Ghi chú: Đồng bộ 100% công thức Hybrid V2 (50/40/10) trên toàn bộ hệ thống
[PROMPT LOG] Việc: T4 — Hiệu chỉnh mục 8 & 12 Mẫu 3 (thay 92% bằng tỷ lệ LLM/fallback 72,2%/27,8%, chuyển formal accuracy sang mục 12; cập nhật thời gian ~1,1-1,3s warm), thêm lưu ý warm-up vào kịch bản demo | AI tạo: Cập nhật docs/mau3_draft.md, docs/DEMO_VIDEO_SCRIPT.md | Người xác nhận/sửa: C (Product/Frontend Lead) | Ghi chú: Tạm dừng giữ nguyên phần Delta Score chờ B xác nhận Tầng 5


