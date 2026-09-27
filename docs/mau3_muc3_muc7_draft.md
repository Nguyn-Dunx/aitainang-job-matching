# Hồ sơ Mẫu 3 — Nháp mục 3 & mục 7

> **Lưu ý**: Số liệu đã chốt (D1/D4). Mục 9 (baseline/ablation) viết sau khi có kết quả D3 + scoring.

---

## Mục 3 — Dữ liệu & tính hợp lệ

### 3.1. Tổng quan nguồn dữ liệu

Sản phẩm sử dụng 4 tập dữ liệu (D1–D4), phục vụ 3 mục đích: matching, đánh giá, và chuẩn hóa
kỹ năng. Toàn bộ dữ liệu được thu thập/xây dựng hợp pháp, ghi rõ nguồn gốc, và tuân thủ quyền
riêng tư.

| Ký hiệu | Dữ liệu | Quy mô | Vai trò |
|----------|---------|--------|---------|
| D1 | JD thật ngành CNTT/Data | 450 JD, 369 công ty | Corpus để matching CV–JD |
| D2 | CV mẫu (có đồng ý + ẩn danh) | 30–50 CV *(đang thu thập)* | Đầu vào để test pipeline |
| D3 | Bộ nhãn chấm điểm (CV, JD) | 50–100 cặp *(chưa gán)* | Ground truth cho evaluation |
| D4 | Taxonomy kỹ năng song ngữ | 235 mục + 690 alias | Chuẩn hóa kỹ năng khi scoring |

### 3.2. D1 — JD thật

**Nguồn**: Dataset công khai `tinixai/vietnamese-job-descriptions` trên HuggingFace
(https://huggingface.co/datasets/tinixai/vietnamese-job-descriptions).

| Hạng mục | Chi tiết |
|----------|---------|
| Giấy phép | CC BY-NC 4.0 (phi thương mại, cần ghi công) |
| Quy mô gốc | 606.878 dòng |
| Ngày tải về | 26/09/2026 |
| Các cột | id, job_title, company_name, salary, location, job_type, job_industry, experience_level, education_level, job_position, job_description, benefits, requirements, year |

**Tính hợp lệ**: Dataset được phát hành công khai trên HuggingFace dưới giấy phép CC BY-NC 4.0.
Sản phẩm dự thi là phi thương mại, phù hợp điều khoản giấy phép. Nhóm ghi công đầy đủ tên dataset
và link trong code, tài liệu, và hồ sơ.

**Quy trình lọc (4 bước)**:

1. **Lọc ngành IT thuần (Phương án A)**: Chỉ giữ JD có `job_industry` thuộc nhóm CNTT/IT — bao
   gồm "IT Phần mềm", "Công nghệ thông tin, Software Engineering, …", và các biến thể. Kết
   quả: 10.572 JD IT từ 606.878 tổng.
2. **Loại trùng lặp**: Cùng công ty + nội dung (job_description + requirements) có fingerprint
   MD5 giống nhau → loại 804 bản trùng → 9.768 JD unique.
3. **Loại JD thiếu nội dung**: JD không có title hoặc tổng (job_description + requirements) dưới
   100 ký tự → loại 20 → 9.748 JD hợp lệ.
4. **Lấy mẫu phân tầng có quota**: Round-robin theo (industry_group × experience_category),
   seed=42. **Quota sàn Data/AI/ML >= 12%** — phân loại JD theo cả `job_industry` và keyword
   trong `job_title` (data analyst, AI engineer, ML engineer…). Kết quả: **450 JD**.

**Phân bố mẫu cuối**:

| Nhóm ngành | JD | % |
|------------|----|----|
| Data/AI/ML | 75 | 16,7% |
| IT General | 71 | 15,8% |
| Software Engineering | 60 | 13,3% |
| Product/Project Mgmt | 57 | 12,7% |
| Infra/DevOps | 56 | 12,4% |
| Testing/QA | 54 | 12,0% |
| Game Dev | 39 | 8,7% |
| Security | 38 | 8,4% |

| Cấp kinh nghiệm | JD | % |
|-------------------|----|----|
| Entry (0-1 năm) | 128 | 28,4% |
| Junior (1-3 năm) | 154 | 34,2% |
| Mid (3-5 năm) | 129 | 28,7% |
| Senior (5+ năm) | 39 | 8,7% |

| Địa điểm | JD | % |
|-----------|----|----|
| Hà Nội | 279 | 62,0% |
| Hồ Chí Minh | 146 | 32,4% |
| Khác | 25 | 5,6% |

**Chuẩn hóa đã thực hiện**:
- `location` (250k+ giá trị unique) → `location_normalized` (47 tỉnh/thành + Remote), bằng regex.
- `experience_level` (161 format) → `level_normalized` (5 nhóm), bằng regex + keyword fallback.
- `job_industry` (đa dạng, "bẩn") → `industry_group` (8 nhóm), bằng keyword classification.

**Hạn chế**: Dataset không có `source_url` hay `posted_date` theo từng dòng — dẫn nguồn ở cấp
dataset, không thể truy xuất bài đăng gốc. Nhóm ghi nhận hạn chế này và bù bằng cách lưu
`source_id` (ID gốc trong dataset) cho mỗi JD.

### 3.3. D2 — CV mẫu

*(Chi tiết tại `data/DATA_SOURCES.md` mục D2 — đang thu thập, chưa chốt số lượng.)*

- CV thành viên nhóm (3 người, tự nguyện).
- CV bạn bè có xin phép bằng văn bản — bằng chứng lưu tại `data/consent/`.
- CV tổng hợp (synthetic) do LLM sinh từ template tự viết — nhân vật hoàn toàn hư cấu.
- **Ẩn danh hoàn toàn**: xóa tên, SĐT, email, ảnh, địa chỉ cụ thể trước khi vào repo.
- **Tuyệt đối không** thu thập CV người lạ từ TopCV/LinkedIn/VietnamWorks hay bất kỳ nguồn nào.

### 3.4. D4 — Taxonomy kỹ năng song ngữ

| Hạng mục | Kết quả |
|----------|---------|
| Quy mô | **235 mục** + **690 alias** |
| Active trong D1 | 211/235 (89,8%) xuất hiện trong >=1 JD |
| Coverage | 99% JD (446/450) có >=1 skill; trung bình 8,6 skill/JD |
| Số nhóm | 32 category (Programming Language, Soft Skill, DevOps, Database, AI…) |

**Phương pháp xây dựng**:
1. Xây seed taxonomy 143 kỹ năng, phân loại thủ công vào 32 nhóm, kèm tên tiếng Việt + danh
   sách alias (biến thể viết, viết tắt, song ngữ).
2. Bổ sung 92 kỹ năng từ domain-specific knowledge (tools phổ biến trong JD Việt Nam, soft
   skills, cloud services, testing tools, architecture patterns).
3. Regex matching trên toàn bộ 450 JD → đếm tần suất → gắn `frequency.jd_count` và
   `frequency.jd_percentage` cho mỗi mục.

**Lưu ý đã phát hiện**: Top skills phổ biến nhất là kỹ năng mềm (Communication 48,7%, Report
Writing 42,9%, English 40,2%…) chứ không phải kỹ năng cứng → scoring cần tách trọng số riêng
(xem mục 7).

### 3.5. Cam kết đạo đức dữ liệu

- **JD**: Thông tin tuyển dụng công khai, dataset có giấy phép rõ ràng (CC BY-NC 4.0).
- **CV**: Chỉ dùng CV có sự đồng ý rõ ràng bằng văn bản, đã ẩn danh hoàn toàn.
- **Không** thu thập dữ liệu cá nhân trái phép từ bất kỳ nguồn nào.
- **Không** dùng dữ liệu để mục đích thương mại.
- Mọi điểm số AI trả về đều kèm evidence và breakdown — không trả một con số hộp đen.
- UI ghi rõ: "Điểm số là tham khảo, không đảm bảo kết quả tuyển dụng."

---

## Mục 7 — Chỉ số đánh giá (phương pháp)

> **Lưu ý**: Mục này trình bày **phương pháp** đánh giá. Kết quả D3 chính thức sẽ điền sau
> khi có CV thật (đang chờ C) và 3 người chấm tay độc lập.
>
> **Kết quả PILOT (sơ bộ, KHÔNG phải D3 chính thức)**: đã kiểm chứng toàn bộ luồng
> ghép cặp → chấm → agreement → metric trên 10 cặp (3 CV synthetic × JD thật, nhãn cơ chế).
> Pipeline chạy đúng đầu-cuối: `generate_annotation_pairs.py` → 3 file chấm →
> `compute_agreement.py` (Fleiss' kappa + Krippendorff's alpha) → `compute_metrics.py`
> (Precision@5, nDCG@10, Spearman, MAE). Số liệu pilot ở bảng 7.6 chỉ mang tính kiểm chứng
> kỹ thuật, sẽ được THAY THẾ bằng số liệu D3 thật.

### 7.1. Tổng quan hệ thống đánh giá

Hệ thống đánh giá 3 tầng:

| Tầng | Đánh giá gì | Phương pháp | Ground truth |
|------|-------------|-------------|-------------|
| Retrieval | Top-K JD trả về có phù hợp không? | Precision@5, nDCG@10 | D3 (chấm tay) |
| Scoring | Điểm khớp CV-JD có đúng không? | Spearman correlation, MAE | D3 (chấm tay) |
| CV Improvement | Gợi ý sửa CV có hữu ích không? | Rubric chấm tay + pilot user | Rubric 3 tiêu chí |

### 7.2. Ground truth — D3

- **Bộ nhãn**: 50-100 cặp (CV, JD), ghép phân tầng từ D1 x D2 (đảm bảo đủ easy/medium/hard).
- **Người chấm**: 3 thành viên nhóm, chấm **độc lập** thang 1-5.
- **Ghi chú lý do**: Bắt buộc — mỗi điểm kèm 1-2 câu giải thích.
- **Đo đồng thuận**: Fleiss' kappa hoặc Krippendorff's alpha. Nếu kappa < 0,6 → rà soát lại
  guideline, chấm lại các cặp bất đồng.
- **Điểm cuối cùng**: Trung bình 3 người (hoặc majority vote nếu phương sai > 1,5 trên thang 5).

### 7.3. Retrieval metrics

Đánh giá bước "tìm top-K JD phù hợp nhất cho 1 CV":

| Metric | Ý nghĩa | Cách tính |
|--------|---------|-----------|
| **Precision@5** | Trong 5 JD trả về, bao nhiêu thực sự phù hợp (score >= 3)? | \|relevant ∩ top-5\| / 5 |
| **nDCG@10** | JD phù hợp có được xếp ở vị trí cao không? | Normalized Discounted Cumulative Gain, dùng score 1-5 làm relevance grade |

Baseline: so sánh giữa (a) keyword matching, (b) embedding-only, (c) LLM-only, (d) full hybrid.

### 7.4. Scoring metrics

Đánh giá bước "chấm điểm 1 cặp CV-JD":

| Metric | Ý nghĩa | Cách tính |
|--------|---------|-----------|
| **Spearman rho** | Thứ tự xếp hạng của hệ thống có khớp với thứ tự chấm tay? | Spearman rank correlation giữa `score_total` (hệ thống) và trung bình score D3 |
| **MAE** | Sai lệch trung bình giữa điểm hệ thống và điểm chấm tay | Mean Absolute Error, thang 1-5 |

Scoring breakdown theo 4 chiều (mỗi chiều có sub-score riêng):
1. **Hard skills match** — skill overlap chuẩn hóa alias theo taxonomy D4
2. **Soft skills match** — tách riêng, weight thấp hơn hard skills (0,3-0,5x)
3. **Experience match** — so sánh years of experience
4. **Education match** — so sánh education level

> **Phát hiện từ D4**: Top skills phổ biến nhất trong JD phần lớn là kỹ năng mềm (Communication
> 48,7%, Report Writing 42,9%…). Nếu cho trọng số ngang bằng, soft skills sẽ chi phối scoring
> → thiên lệch. Giải pháp: tách hard_skill_score và soft_skill_score, giảm weight soft skill
> trong công thức tổng hợp. Taxonomy phân loại sẵn `category` cho mỗi skill.

### 7.5. CV Improvement metrics

Đánh giá bước "gợi ý sửa CV":

| Tiêu chí | Thang | Định nghĩa |
|----------|-------|-----------|
| Tính cụ thể | 1-5 | Gợi ý có chỉ rõ **cần sửa gì**, ở đâu trong CV, và ví dụ viết lại? |
| Tính khả thi | 1-5 | Ứng viên có thể thực hiện gợi ý này không (không yêu cầu bịa kinh nghiệm)? |
| Không bịa | Binary | AI có "bịa" thông tin không có trong CV/JD gốc không? |

- Chấm tay trên 20-30 gợi ý (sample từ nhiều cặp CV-JD).
- Bổ sung phản hồi pilot người dùng (5-10 người thử nghiệm thực tế).
- **Delta score**: Sau khi sửa CV theo gợi ý → chạy lại scoring → đo delta = score_after - score_before.
  Kỳ vọng delta > 0 cho >=80% trường hợp.

### 7.6. Baseline / Ablation (mục 9 hồ sơ)

> *(Đã có số liệu PILOT kiểm chứng pipeline — xem bảng dưới; số D3 chính thức sẽ thay thế)*

So sánh 4 biến thể trên cùng bộ D3:

| Biến thể | Mô tả |
|----------|-------|
| (a) Keyword matching | Overlap từ khóa thuần túy (TF-IDF / Jaccard) |
| (b) Embedding-only | Cosine similarity giữa embedding CV và JD (BGE-M3) |
| (c) LLM-only | LLM chấm trực tiếp (structured output, không có pipeline) |
| (d) **Full hybrid** | Deterministic (skill/exp/edu) + semantic (embedding) + LLM — bản chính thức |

Bảng kết quả (template — chưa có số):

**Số liệu PILOT (10 cặp, CV synthetic, nhãn cơ chế — CHƯA PHẢI D3 CHÍNH THỨC):**

| Biến thể | Precision@5 | nDCG@10 | Spearman rho | MAE (1-5) |
|----------|-------------|---------|-------------|-----|
| (a) Keyword-only | 0.400 | 0.979 | 0.296 | 3.261 |
| (b) Embedding-only | 0.400 | 0.969 | -0.105 | 1.426 |
| (c) LLM-only | — (chờ chạy) | — | — | — |
| **(d) Hybrid V2** | **0.400** | **0.968** | **0.148** | **2.423** |

*Cảnh báo diễn giải: nhãn pilot sinh cơ học từ difficulty_hint nên các chỉ số KHÔNG phản ánh
chất lượng thật; giá trị duy nhất của bảng này là chứng minh pipeline đo được đầu-cuối.
Công thức hybrid V2: 0.5 × hard_skill + 0.1 × soft_skill + 0.4 × semantic (xem README).*

**Số liệu D3 chính thức (điền sau khi chấm tay):**

| Biến thể | Precision@5 | nDCG@10 | Spearman rho | MAE |
|----------|-------------|---------|-------------|-----|
| (a) Keyword | — | — | — | — |
| (b) Embedding-only | — | — | — | — |
| (c) LLM-only | — | — | — | — |
| **(d) Full hybrid** | **—** | **—** | **—** | **—** |
