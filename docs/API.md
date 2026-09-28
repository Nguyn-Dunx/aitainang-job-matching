# API tích hợp cho Frontend (C)

Backend: FastAPI. Chạy local:

```bash
# từ thư mục prj/ (đã activate venv)
uvicorn app.main:app --port 8000
```

## POST /api/cv/upload

Upload CV (PDF/DOCX) → parse → trích skill → embed → lọc + xếp hạng JD → trả điểm kèm breakdown.

**Request**: `multipart/form-data`, field `file` = file CV.

**Query params** (tất cả optional):

| Param | Kiểu | Mặc định | Mô tả |
|-------|------|----------|-------|
| `mode` | `llm` \| `rule` | `llm` | `llm`: trích skill bằng LLM (tự fallback rule nếu lỗi); `rule`: nhanh, deterministic |
| `top_k` | int 1–50 | `10` | Số JD trả về |
| `location` | string | — | Lọc cứng: `Hà Nội`, `Hồ Chí Minh`, `Bình Dương`, `Đà Nẵng`, `Khác` |
| `level` | string | — | Lọc cứng: `Intern`, `Fresher`, `Junior`, `Senior`, `Lead` |
| `industry_group` | string | — | Lọc cứng: `Software Engineering`, `Data/AI/ML`, `Infra/DevOps`, ... |

**Ví dụ curl (chạy thật được, dùng CV test có sẵn trong repo):**

```bash
curl -X POST "http://localhost:8000/api/cv/upload?mode=rule&top_k=3&location=H%C3%A0%20N%E1%BB%99i" \
  -F "file=@tests/fixtures/cv_single_column.pdf"
```

(`mode=rule` để test nhanh không cần LLM; bỏ `location` nếu muốn xem toàn bộ.)

**Response 200** — 4 key mức ngoài: `parsed_cv`, `matches`, `extraction_mode`, `parse_warnings`
(đã xác minh bằng curl thật với fixture trong repo):

```jsonc
{
  "extraction_mode": "rule",        // "llm" hoặc "rule" (rule = đã fallback)
  "parse_warnings": [],             // vd: cảnh báo CV ảnh scan

  // Phần 1: CV đã parse (shape khớp UploadCVPage)
  "parsed_cv": {
    "candidate_id": "Ứng viên (Ẩn danh)",
    "target_title": "Backend Developer",
    "years_of_experience": 2,
    "education": {"institution": "...", "degree": "...", "graduation_year": 2024, "gpa": null},
    "skills": ["Python", "Django", "PostgreSQL"],   // canonical name trong taxonomy
    "experience": [{"id": 1, "company": "...", "role": "...", "period": "...", "responsibilities": ["..."]}],
    "uploaded_filename": "cv_single_column.pdf"
  },

  // Phần 2: danh sách JD khớp, xếp hạng theo score giảm dần
  "matches": [
    {
      "id": "123",
      "title": "Back End Developer",
      "company": "Đơn vị tuyển dụng",
      "location": "Hà Nội",
      "level": "Junior",
      "industry_group": "Software Engineering",
      "salary": "Thỏa thuận",
      "job_type": "",
      "benefits": ["..."],
      "score": 50.8,                    // 0-100, công thức V2 công khai
      "breakdown": {
        "hard_skill": {"score": 29.0, "weight": 0.5, "matched": ["..."], "missing": ["..."]},
        "soft_skill": {"score": 50.0, "weight": 0.1, "matched": ["..."]},
        "semantic":   {"score": 64.0, "weight": 0.4}
      },
      "evidence": {
        "jd_snippet": "...",                       // trích nguyên văn JD
        "matched_skills_in_cv": ["..."]            // skill khớp xuất hiện thật trong CV
      }
    }
  ]
}
```

**Công thức điểm (công khai, không hộp đen):**
`score = 0.5 × hard_skill + 0.1 × soft_skill + 0.4 × semantic`
(hard/soft skill = overlap trên taxonomy 235 skill, tách riêng nhóm Soft Skill/Language Skill;
semantic = cosine BGE-M3 × 100)

**Lỗi**: 422 nếu query param sai pattern; 500 kèm message nếu file không parse được
(CV ảnh scan chỉ được cảnh báo, OCR ngoài phạm vi).

**Lưu ý tích hợp**: `MatchingPage.jsx` hiện có placeholder — chỉ cần thay bằng
`fetch('/api/cv/upload', {method: 'POST', body: formData})`. Response lồng 2 tầng:
CV nằm trong `data.parsed_cv`, danh sách JD trong `data.matches`. Kiểm tra
`data.extraction_mode === 'rule'` để hiển thị badge "chế độ dự phòng" nếu LLM lỗi. Nhớ gửi kèm query params
filter nếu UI có chọn location/level/industry.

---

## POST /api/cv/suggest-improvement — Tầng 5: gợi ý sửa CV + delta score

Input: CV **đã parse** (không cần upload lại file) + `job_id` của 1 JD trong danh sách match.

```json
{
  "job_id": "f356d908-...",            // UUID JD (trường id trong matches của /upload)
  "cv_skills": ["Python", "FastAPI", "..."],
  "cv_experience": ["Thiết kế RESTful API...", "..."],  // bullet kinh nghiệm hiện có
  "cv_text": "Backend Engineer | ... (bản tóm tắt CV)",   // optional: để tính cosine_sim thật
  "accepted_skills": null              // null = chấp nhận tất cả skill trong gợi ý
}
```

Response (đo thật, CV `cv_member_01_backend` × JD "Kỹ Sư Quản Trị Hệ Thống"):

```json
{
  "job_id": "...", "job_title": "Kỹ Sư Quản Trị Hệ Thống",
  "gap": {
    "matched_hard": ["Linux", "Docker"], "missing_hard": ["Firewall", "Load Balancer", "Networking", "Windows Server"],
    "matched_soft": ["Teamwork"], "missing_soft": ["Communication", "Time Management"]
  },
  "suggestions": [
    {"skill": "Networking", "text": "Nếu bạn đã cấu hình mạng cho container Docker (bridge network, port mapping)..."}
  ],
  "accepted_skills": ["Communication", "Firewall", "Load Balancer", "Networking"],
  "score_before": 13.3, "score_after": 46.7, "delta": 33.4,
  "breakdown_before": {"...": "..."}, "breakdown_after": {"...": "..."},
  "note": "delta chi den tu thanh phan skill overlap; semantic giu nguyen (khong re-embed CV sau khi sua). Goi y dang dieu kien, khong bia kinh nghiem."
}
```

**Ràng buộc chống bịa:**
- Gap lấy từ đúng hàm scoring hiện có (`split_hard_soft` + `_overlap_score`), không tính lại từ đầu.
- LLM chỉ được gợi ý cho skill nằm trong `missing_*`; gợi ý lệch danh sách bị loại bỏ phía server.
- Prompt bắt buộc viết gợi ý dạng điều kiện ("Nếu bạn đã từng...") — không bịa kinh nghiệm CV không có.
- `accepted_skills` từ client cũng bị lọc lại theo gap thật.
- Delta = `score_hybrid_v2(CV + accepted) − score_hybrid_v2(CV gốc)`, cùng cosine_sim → delta chỉ đến từ skill overlap; semantic giữ nguyên.

**Lỗi**: 404 nếu `job_id` không tồn tại; 200 với `suggestions: []` nếu LLM lỗi cả 3 lần thử
(model chính ×2 + fallback) — khi đó `delta` vẫn tính được nếu client gửi `accepted_skills` riêng.
