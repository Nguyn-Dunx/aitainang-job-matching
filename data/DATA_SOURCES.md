# DATA_SOURCES.md — Kê khai nguồn dữ liệu

> Tài liệu này là minh chứng cho **mục 3 — Hồ sơ Mẫu 3** (Dữ liệu & tính hợp lệ).
> Mọi thay đổi phải được commit kèm mô tả rõ ràng.

---

## D1 — JD thật, ngành CNTT / Data

### Nguồn chính: Dataset công khai HuggingFace

| Hạng mục | Chi tiết |
|----------|---------|
| Dataset | [`tinixai/vietnamese-job-descriptions`](https://huggingface.co/datasets/tinixai/vietnamese-job-descriptions) |
| Giấy phép | **CC BY-NC 4.0** (phi thương mại, cần ghi công) — phù hợp mục đích dự thi |
| Quy mô gốc | 606,878 dòng |
| Ngày tải | 2026-09-26 |
| Cột | id, job_title, company_name, salary, location, job_type, job_industry, experience_level, education_level, job_position, job_description, benefits, requirements, year |

### Tiêu chí lọc đã dùng

1. **Lọc ngành (Phương án A — IT thuần)**: Chỉ lấy JD có `job_industry` thuộc nhóm:
   - `IT Phần mềm`, `IT phần mềm`, `IT Phần cứng - Mạng`, `IT phần cứng/mạng`
   - `CNTT - Phần mềm`, `Công nghệ thông tin`, và các giá trị ghép bắt đầu bằng
     `"Công nghệ thông tin, ..."` (Software Engineering, Data Science, AI, DevOps,
     Testing, Infrastructure, Product/Project Management, Security, Game Dev…)
   - → 10,572 JD IT thuần từ tổng 606,878
2. **Loại trùng lặp gần giống**: Cùng công ty + nội dung (job_description + requirements)
   có fingerprint giống nhau → loại 804 bản trùng → 9,768 JD unique
3. **Loại JD thiếu nội dung**: JD không có title hoặc (job_description + requirements)
   dưới 100 ký tự → loại 20 → 9,748 JD hợp lệ
4. **Lấy mẫu phân tầng có quota** (v2, `scripts/resample_with_quota.py`, seed=42) → **450 JD**
   - **Quota sàn Data/AI/ML ≥ 12%**: lấy 75/450 JD (16.7%) — phân loại theo cả
     `job_industry` và keyword trong `job_title` (data analyst, AI engineer, ML…)
   - Các nhóm khác: round-robin theo (industry_group, experience_category)
   - 369 công ty unique (max 6 JD/cty)
   - Phân bố nhóm ngành: Data/AI/ML 16.7%, IT General 15.8%, Software Eng 13.3%,
     Product/Project Mgmt 12.7%, Infra/DevOps 12.4%, Testing/QA 12.0%,
     Game Dev 8.7%, Security 8.4%
   - Phân bố experience: Entry 28.4%, Junior 34.2%, Mid 28.7%, Senior 8.7%
   - Phân bố location: Hà Nội 62%, HCM 32.4%, khác 5.6%

### Hạn chế của nguồn dữ liệu

- **Không có `source_url` hay `posted_date` theo từng dòng** — dẫn nguồn ở cấp dataset,
  không thể truy xuất về bài đăng gốc từng JD.
- Cột `location` rất chi tiết (địa chỉ cụ thể, 250k+ giá trị unique) — đã chuẩn hóa về
  tỉnh/thành trong trường `location_normalized` bằng regex matching 47 tỉnh/thành + Remote.
- Cột `experience_level` có 161 format khác nhau — đã chuẩn hóa thành 5 nhóm trong trường
  `level_normalized`: Intern/Fresher, Entry (0-1 năm), Junior (1-3 năm), Mid (3-5 năm),
  Senior (5+ năm).
- Cột `job_industry` rất "bẩn" — cùng một ngành có nhiều cách viết, nhiều giá trị ghép dài.
  Đã phân loại vào 8 nhóm trong trường `industry_group`.

### Mapping sang schema nội bộ

| Trường schema | ← Cột dataset | Ghi chú |
|---------------|---------------|---------|
| `title` | `job_title` | — |
| `requirements` | `requirements` | — |
| `responsibilities` | `job_description` | Dataset gọi là "job_description" |
| `level` | `experience_level` | Giữ nguyên giá trị gốc |
| `level_normalized` | *(derived)* | 5 nhóm: Intern/Fresher, Entry, Junior, Mid, Senior |
| `location` | `location` | Giữ nguyên giá trị gốc |
| `location_normalized` | *(derived)* | Tỉnh/thành hoặc Remote/Toàn quốc |
| `industry_group` | *(derived)* | 8 nhóm: Data/AI/ML, Software Eng, Testing/QA… |
| `metadata.company_name` | `company_name` | Metadata phụ |
| `metadata.salary` | `salary` | Metadata phụ |
| `metadata.benefits` | `benefits` | Metadata phụ |
| `metadata.job_type` | `job_type` | Metadata phụ |
| `metadata.education_level` | `education_level` | Metadata phụ |
| `metadata.job_position` | `job_position` | Metadata phụ |
| `metadata.job_industry` | `job_industry` | Metadata phụ |
| `metadata.year` | `year` | Metadata phụ |
| `metadata.source_dataset` | — | `"tinixai/vietnamese-job-descriptions"` |
| `metadata.source_id` | `id` | ID gốc trong dataset |

### File đầu ra

| File | Nội dung |
|------|---------|
| `data/processed/jds.json` | 450 JD đã map schema + chuẩn hóa, sẵn sàng dùng cho pipeline |
| `data/raw/hf_it_jds_filtered.json` | 450 JD raw (giữ cột gốc) |
| `data/raw/hf_dataset_exploration.json` | Thống kê unique values toàn dataset |

### Nguồn phụ: JD thu thập thủ công (tập đối chiếu chất lượng)

| # | Nguồn | Loại nguồn | Ngày thu thập | Số lượng JD | Ghi chú / Điều khoản sử dụng |
|---|-------|-----------|--------------|------------|------------------------------|
| 1 | Nhóm Facebook tuyển dụng IT | Bài đăng công khai | 2026-09-25 | 3 | JD thu thập thủ công, dùng làm tập đối chiếu chất lượng so với dataset HF |

> **Lưu ý**: JD thủ công lưu tại `data/raw/jd_batch_20260925_sample.txt`, giữ lại làm
> baseline so sánh chất lượng parsing, không tính vào 450 JD chính.

### Quy trình thu thập D1 (đã cập nhật)
1. Tải dataset từ HuggingFace bằng thư viện `datasets` (`scripts/explore_hf_dataset.py`).
2. Lọc ngành IT thuần + loại trùng lặp (`scripts/filter_and_sample_jds.py` — v1, lưu trữ).
3. Resample với quota Data/AI sàn 12% + chuẩn hóa location/experience
   (`scripts/resample_with_quota.py` — v2, bản chính thức).
4. Map sang schema nội bộ → `data/processed/jds.json`.
5. Review thủ công nếu cần (kiểm tra chất lượng mẫu).

---

## D2 — CV mẫu (Lưu trữ chuẩn tại `data/cv_samples/`)

| # | Nguồn | Đồng ý | Ẩn danh | Số lượng | Vị trí lưu trữ & Ghi chú |
|---|-------|--------|---------|---------|-------------------------|
| 1 | CV thành viên nhóm (3 người) | Có — tự nguyện bằng văn bản | Đã xóa 100%: tên thật, SĐT, email, ảnh, địa chỉ | 3 | `data/cv_samples/cv_member_01_backend.json`<br>`data/cv_samples/cv_member_02_data_ai.json`<br>`data/cv_samples/cv_member_03_frontend_product.json` |
| 2 | CV bạn bè (có xin phép văn bản) | Có — tin nhắn/email lưu lại theo `docs/cv_consent_template.md` | Như trên (loại bỏ toàn bộ PII) | 8/15-20 (đang tiếp nhận) | Đang ẩn danh hóa trước khi nạp vào `data/cv_samples/`; lưu bằng chứng đồng ý tại `data/consent/` |
| 3 | CV tổng hợp (synthetic) | N/A | N/A | 3 | `tests/fixtures/cv_{single_column,two_column,missing_sections}.pdf` — phục vụ test pipeline Tầng 1–2; pilot D3 tại `data/processed/cvs_pilot/` |

### Quy trình ẩn danh CV (Tuân thủ Điều 5.7 Thể lệ Cuộc thi)
- Xóa hoàn toàn: họ tên thật, SĐT, email, địa chỉ cụ thể, ảnh đại diện, link mạng xã hội cá nhân, tên trường/công ty nếu quá đặc thù.
- Thay thế: tên → `Ứng viên #AIT-01/02/03…`, email → `candidate_XX@aitainang.vn`.
- File CV gốc của người tham gia **tuyệt đối không** được commit vào repo; chỉ lưu bản đã ẩn danh tại `data/cv_samples/`.
- Cam kết đạo đức: Chỉ dùng dữ liệu cho mục đích nghiên cứu, học thuật của Cuộc thi Sáng tạo trẻ AI 2026.

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
| Quy mô đạt được | **235 mục + 690 alias** (mục tiêu 200–500 ✅) |
| Active trong D1 | 211/235 skills (89.8%) xuất hiện trong ≥1 JD |
| Coverage | 99% JD (446/450) có ≥1 skill; trung bình 8.6 skill/JD |
| Phương pháp xây | Seed taxonomy 143 skills (phân loại thủ công) + bổ sung 92 skills → regex matching trên D1 → đếm tần suất |
| Ngôn ngữ | Mỗi mục có tên tiếng Anh (canonical) + tên tiếng Việt + danh sách alias |
| Nhóm (categories) | 32 nhóm: Programming Language (24), Soft Skill (18), DevOps (19), Backend Framework (15), Database (17), AI & Data Science (12)… |
| Ví dụ | `{ "canonical": "Python", "vi": "Python", "aliases": ["python3", "python 3.x", "lập trình Python"], "frequency": { "jd_count": 114, "jd_percentage": 25.3 } }` |
| File | `data/taxonomy/skills_taxonomy.json` |
| Scripts | `scripts/build_taxonomy.py` (seed), `scripts/extend_taxonomy.py` (bổ sung) |

### Lưu ý quan trọng cho scoring (B cần biết — mục 7 hồ sơ)

> **Top skills phổ biến nhất phần lớn là kỹ năng mềm**, không phải kỹ năng cứng:
> Communication (48.7%), Report Writing (42.9%), English (40.2%), Independent Work
> (36.2%), Problem Solving (35.1%), Responsibility (31.1%), Teamwork (30.9%)…
>
> Khi scoring CV–JD, **B không nên cho trọng số ngang bằng** giữa soft skill và hard
> skill. Gợi ý: tách thành 2 chiều riêng (hard_skill_score, soft_skill_score), hoặc
> giảm weight soft skill xuống 0.3–0.5 so với hard skill trong công thức tổng hợp.
> Taxonomy đã phân loại sẵn `category` cho mỗi skill — dùng trường này để phân biệt.

---

## Cam kết đạo đức dữ liệu

- **Không** thu thập CV của người lạ từ bất kỳ nguồn nào (TopCV, LinkedIn, VietnamWorks…).
- **Không** lưu thông tin cá nhân (tên, SĐT, email, ảnh) vào repo.
- JD là thông tin tuyển dụng công khai — ghi rõ nguồn và ngày thu thập.
- Mọi CV đều có sự đồng ý rõ ràng bằng văn bản và đã ẩn danh hoàn toàn.
- Bằng chứng đồng ý lưu tại `data/consent/` (không commit lên GitHub public).
