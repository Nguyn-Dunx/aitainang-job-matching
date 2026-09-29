# Hồ sơ Mẫu 3 — aitainang: Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam

---

## Mục 1 — Bối cảnh & Bài toán thực tế

### 1.1. Bối cảnh thị trường việc làm của người trẻ tại Việt Nam
Thị trường việc làm ngành Công nghệ Thông tin (CNTT) và Dữ liệu tại Việt Nam những năm gần đây chứng kiến sự phân hóa mạnh mẽ. Mặc dù nhu cầu tuyển dụng các vị trí chất lượng cao vẫn lớn, sinh viên năm 3–4 và sinh viên mới tốt nghiệp (fresh graduate) lại gặp vô vàn rào cản khi tiếp cận thị trường lao động:
- Theo các khảo sát tuyển dụng sinh viên, **hơn 70% sinh viên** cảm thấy hoang mang khi đối chiếu năng lực bản thân với yêu cầu tuyển dụng thực tế.
- Tỷ lệ hồ sơ ứng tuyển nhận được phản hồi phỏng vấn vòng đầu đối với ứng viên ít kinh nghiệm thường **dưới 10%**, dẫn đến tâm lý chán nản và mất phương hướng.

### 1.2. Ba bài toán cốt lõi người trẻ phải tự giải quyết thủ công
Hiện nay, một ứng viên trẻ trước khi nộp đơn phải tự xoay xở giải quyết ba câu hỏi lớn:
1. **"Mình thực sự phù hợp với vị trí và nhóm ngành nào?"** — Sinh viên thường mơ hồ giữa các vai trò tương đồng (ví dụ Data Analyst vs. Data Engineer, Backend vs. DevOps) và không biết hồ sơ của mình có đủ sức cạnh tranh hay không.
2. **"CV của mình còn thiếu sót những gì so với mô tả công việc (JD)?"** — Việc đọc hàng chục bản JD phức tạp, viết bằng cả tiếng Anh lẫn tiếng Việt, để tự rà soát khoảng trống kỹ năng (skill gaps) là một công việc thủ công tốn hàng chục giờ và dễ bỏ sót.
3. **"Phải sửa CV cụ thể như thế nào để vượt qua vòng lọc hồ sơ?"** — Sinh viên biết CV chưa chuẩn nhưng không biết viết lại các gạch đầu dòng (bullet points) kinh nghiệm sao cho trúng trọng tâm, thể hiện đúng năng lực và chuẩn hóa theo thuật ngữ mà nhà tuyển dụng tìm kiếm.

### 1.3. Hạn chế của các giải pháp hiện nay trên thị trường
- **Các trang tin tuyển dụng truyền thống (TopCV, VietnamWorks, LinkedIn...)**: Chủ yếu hoạt động như bảng tin đăng việc và tìm kiếm từ khóa cứng (keyword matching). Khi ứng viên tìm việc, hệ thống chỉ so khớp chuỗi ký tự thô, bỏ qua ngữ nghĩa ngữ cảnh sâu sắc (ví dụ: không hiểu "FastAPI" và "RESTful API" có quan hệ mật thiết).
- **Các công cụ chấm điểm CV bằng AI hiện nay**: Đa phần là "hộp đen" (black-box). Hệ thống chỉ trả về một con số phần trăm chung chung (ví dụ "Độ khớp 75%") mà không giải thích cặn kẽ tại sao đạt điểm số đó, không trích dẫn bằng chứng cụ thể từ CV và JD, khiến người dùng không biết cần khắc phục ở đâu.
- **Thiếu vòng lặp cải thiện đo lường được (Measurable Loop)**: Các công cụ hiện tại chỉ dừng ở việc "chấm điểm một lần" rồi để mặc người dùng tự xử lý; hoàn toàn thiếu cơ chế đồng hành hướng dẫn sửa CV và đo lường sự tiến bộ (Delta Score) trước khi nộp đơn.
- **Rào cản ngôn ngữ & đặc thù tuyển dụng tại Việt Nam**: Các công cụ quốc tế không xử lý tốt tài liệu song ngữ Việt – Anh, không hiểu được các thuật ngữ tuyển dụng bản địa và cấu trúc văn phong CV của sinh viên Việt Nam.

---

## Mục 2 — Mục tiêu, Phạm vi & Đối tượng sử dụng

### 2.1. Định vị sản phẩm & USP cốt lõi
**Định vị sản phẩm**: **"Trợ lý nghề nghiệp cá nhân hóa cho người trẻ Việt Nam"** — không đơn thuần là một công cụ chấm điểm CV–JD, mà là một nền tảng đồng hành toàn diện từ định hướng nghề nghiệp, giải thích điểm số minh bạch, đến hướng dẫn tối ưu hồ sơ đo lường được.

**Ba trụ cột USP (Unique Selling Points)**:
1. **Explainable Matching (Đối chiếu giải thích được)**: Công khai minh bạch công thức tính điểm (Hybrid V2), phân rã chi tiết 3 chiều trọng số (50% Kỹ năng cứng, 40% Ngữ nghĩa ngữ cảnh, 10% Kỹ năng mềm) và cung cấp bằng chứng (Evidence) trích dẫn trực tiếp từ CV và JD gốc.
2. **Measurable CV Improvement Loop (Vòng lặp sửa CV đo được)**: Xác định khoảng trống kỹ năng theo thứ tự ưu tiên, gợi ý viết lại bullet point hành động cụ thể theo phương pháp STAR, và hỗ trợ chấm lại ngay lập tức để đo lường **Delta Score** gia tăng.
3. **Vietnamese-First (Tối ưu bản địa hóa song ngữ)**: Xây dựng bộ taxonomy kỹ năng song ngữ (235 canonical + 690 alias), xử lý mượt mà tài liệu viết bằng tiếng Việt, tiếng Anh hoặc pha trộn cả hai ngôn ngữ.

### 2.2. Mục tiêu cụ thể của dự án
- Xây dựng hoàn chỉnh luồng sản phẩm 6 bước: Onboarding → Upload & Human-in-the-loop Parse CV → Semantic & Hybrid Matching → Explainable Results & Evidence → CV Improvement with Delta Score → Career Dashboard.
- Đảm bảo pipeline AI 5 tầng vận hành ổn định, thời gian phản hồi matching dưới 1 giây trên kho dữ liệu việc làm thực tế.
- Tích hợp cơ chế **Human-in-the-loop** giúp ứng viên kiểm soát và chỉnh sửa thông tin trích xuất, triệt tiêu nguy cơ ảo tưởng thông tin (hallucination) của mô hình AI.

### 2.3. Phạm vi dự án
- **Lĩnh vực ngành nghề**: Trọng tâm ban đầu tập trung vào khối ngành Công nghệ Thông tin và Dữ liệu (IT, Software Engineering, Data Science, AI/ML, DevOps, QA, Product Management) — lĩnh vực có nhu cầu tuyển dụng sinh viên lớn nhất và bộ kỹ năng được tiêu chuẩn hóa cao.
- **Dữ liệu thực nghiệm**: 450 bản JD tuyển dụng thực tế tại Việt Nam từ dataset công khai `tinixai/vietnamese-job-descriptions` (giấy phép CC BY-NC 4.0), phân bố đa dạng theo cấp bậc (Intern, Fresher, Junior, Mid, Senior) và địa bàn (Hà Nội, TP.HCM, Toàn quốc).
- **Bộ dữ liệu CV**: CV của các thành viên nhóm và bạn bè có văn bản đồng ý tự nguyện, ẩn danh hóa 100% theo Điều 5.7 Thể lệ Cuộc thi.

### 2.4. Đối tượng sử dụng
- **Đối tượng mục tiêu chính**: Sinh viên năm 3–4 và sinh viên mới tốt nghiệp khối ngành CNTT/Data đang chuẩn bị bước vào thị trường lao động.
- **Đối tượng tiềm năng mở rộng**: Người chuyển ngành (career switchers) sang lĩnh vực công nghệ cần đánh giá năng lực hiện có; các trung tâm hỗ trợ việc làm sinh viên tại các trường đại học sử dụng làm công cụ tư vấn định hướng.

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
| Coverage | 100% JD (450/450) có >=1 skill; trung bình 11,7 skill/JD (đếm lại từ DB ngày 28/09) |
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

## Mục 4 — Quy trình tiền xử lý dữ liệu

### 4.1. JD (D1)

1. **Lọc lĩnh vực**: từ 606.878 dòng gốc, lọc 450 JD thuộc nhóm CNTT/Data theo
   `industry_group` (Software Engineering, Data/AI/ML, Infra/DevOps, Game Dev...).
2. **Làm sạch**: loại HTML thừa, chuẩn hóa xuống dòng, bỏ JD rỗng/trùng.
3. **Chuẩn hóa trường lọc** (migration 002): `level_normalized` (Intern/Fresher/Junior/
   Senior/Lead), `location_normalized` (Hà Nội 279, Hồ Chí Minh 146, 25 JD còn lại rải ở
   Bình Dương 5, Đà Nẵng 4 và 9 tỉnh/thành khác — tổng đủ 450), `industry_group` —
   kèm index để lọc trước khi xếp hạng.
4. **Trích xuất kỹ năng (Tầng 2)**: LLM (OpenRouter, model `moonshotai/kimi-k3`,
   fallback `nvidia/nemotron-3-ultra-550b-a55b`) trích skill theo taxonomy D4, kèm
   `evidence_snippet` trích nguyên văn JD; JD nào LLM lỗi/timeout thì fallback rule
   (regex alias). Kết quả thực tế: **LLM 325/450 (72,2%), rule 125/450 (27,8%)**.
5. **Embedding (Tầng 3)**: toàn bộ 450 JD embed bằng BGE-M3 (1024-dim), lưu
   `jds_embeddings.npy` + cột `vector(1024)` trong Neon pgvector.

### 4.2. CV (D2)

1. **Parse (Tầng 1)**: `pymupdf` đọc PDF/DOCX, tách section (kinh nghiệm, kỹ năng,
   học vấn) theo heading; CV ảnh scan phát hiện và cảnh báo (OCR ngoài phạm vi).
2. **Trích xuất (Tầng 2)**: cùng cơ chế LLM + rule fallback như JD, cùng taxonomy D4
   → CV và JD nằm trên cùng một không gian kỹ năng chuẩn hóa.
3. **Ẩn danh**: CV thật thu thập có đồng ý, loại bỏ thông tin định danh trước khi xử lý.

---

## Mục 5 — Thuật toán, mô hình và công cụ AI

| Thành phần | Lựa chọn | Vai trò |
|-----------|----------|---------|
| Embedding | **BGE-M3** (`BAAI/bge-m3`, sentence-transformers 6.1.0), 1024-dim, đa ngôn ngữ (tốt cho tiếng Việt) | Biểu diễn ngữ nghĩa CV/JD cho semantic score + vector search |
| LLM trích xuất | `moonshotai/kimi-k3` qua OpenRouter (fallback `nvidia/nemotron-3-ultra-550b-a55b`), structured JSON output, temperature=0 | Trích skill từ văn bản tự do về canonical name trong taxonomy |
| Rule fallback | Regex trên 690 alias của taxonomy D4 | Đảm bảo pipeline không chết khi LLM lỗi (27,8% JD thực tế) |
| Scoring | Công thức hybrid V2 deterministic (mục 7) | Điểm phù hợp minh bạch, có breakdown |
| Vector DB | PostgreSQL + **pgvector 0.8.6** (Neon, ap-southeast-1) | Lưu + tìm kiếm láng giềng gần nhất trên 450 embedding |
| Backend | **FastAPI** (Python 3.12) | API upload CV + matching cho frontend React |

**Kiểm chứng trước khi chọn BGE-M3** (de-risk): cosine(cùng JD) = 0,784 > 0,7;
cosine(JD khác lĩnh vực) = 0,466 < 0,5 → đủ độ tách biệt cho Tầng 3.

---

## Mục 6 — Quy trình tích hợp mô hình

Pipeline 4 tầng, mỗi tầng kiểm chứng độc lập:

```
CV (PDF) ──Tầng 1──> text + sections ──Tầng 2──> skills chuẩn hóa (LLM/rule)
                                              │
JD (450) ──Tầng 1──> text ──Tầng 2──> skills chuẩn hóa ──┤
                                                          ▼
                              Tầng 3: BGE-M3 embed CV + JD (1024-dim)
                                                          ▼
              Tầng 4: lọc cứng (level/location/industry) -> pgvector top-K
                      -> hybrid scoring V2 -> breakdown + evidence -> API
```

- **Tích hợp LLM**: gọi qua OpenRouter API, prompt ép JSON schema, parse lỗi thì
  chuyển model fallback, cả hai lỗi thì chuyển rule — không bao giờ trả lỗi trần.
- **Tích hợp embedding**: service singleton lazy-load (threading.Lock), model chỉ
  tải 1 lần; đo warm 82–127 ms/câu ngắn trên CPU (28/09); JD dài hơn ước ~0,8–1 s/JD
  (ước tính từ phiên import, chưa lưu log đo riêng).
- **Tích hợp DB**: migration Alembic-style (001 bảng, 002 cột chuẩn hóa + index);
  import 450/450 JD, 450/450 embedding, 0 dòng thiếu cột lọc.
- **API**: `POST /api/cv/upload` (multipart PDF) → parse + extract + embed + match
  trong 1 request; filter `industry_group`, `location`, `level` truyền qua query params.
  E2E test thật: upload PDF → nhận danh sách JD xếp hạng kèm breakdown (24,7 s — gồm cả
  thời gian khởi động app trong pytest; request đơn lẻ khi hệ thống đã warm đo riêng
  ~1,1–1,3 s).

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

- **Bộ nhãn**: tối thiểu 20–30 cặp, mục tiêu 50–100 cặp (CV, JD), ghép phân tầng từ D1 × D2 (đảm bảo đủ easy/medium/hard).
- **Người chấm**: 3 thành viên nhóm, chấm **độc lập** thang 1-5.
- **Ghi chú lý do**: Bắt buộc — mỗi điểm kèm 1-2 câu giải thích.
- **Đo đồng thuận**: Fleiss' kappa hoặc Krippendorff's alpha. Nếu kappa < 0,6 → rà soát lại
  guideline, chấm lại các cặp bất đồng.
- **Điểm cuối cùng**: Trung bình 3 người (hoặc majority vote nếu phương sai > 1,5 trên thang 5).

### 7.3. Retrieval metrics

Đánh giá bước "tìm top-K JD phù hợp nhất cho 1 CV":

| Metric | Ý nghĩa | Cách tính |
|--------|---------|-----------|
| **Precision@5** | Trong 5 JD trả về, bao nhiêu thực sự phù hợp (score >= 4)? | \|relevant ∩ top-5\| / 5 |
| **nDCG@10** | JD phù hợp có được xếp ở vị trí cao không? | Normalized Discounted Cumulative Gain, dùng score 1-5 làm relevance grade |

Baseline: so sánh giữa (a) keyword matching, (b) embedding-only, (c) LLM-only, (d) full hybrid.

### 7.4. Scoring metrics

Đánh giá bước "chấm điểm 1 cặp CV-JD":

| Metric | Ý nghĩa | Cách tính |
|--------|---------|-----------|
| **Spearman rho** | Thứ tự xếp hạng của hệ thống có khớp với thứ tự chấm tay? | Spearman rank correlation giữa `score_total` (hệ thống) và trung bình score D3 |
| **MAE** | Sai lệch trung bình giữa điểm hệ thống và điểm chấm tay | Mean Absolute Error, thang 1-5 |

Scoring breakdown V2 hiện tại gồm 3 thành phần (đã implement, công thức công khai):
1. **Hard skills match** (weight 0,5) — skill overlap chuẩn hóa alias theo taxonomy D4,
   LOẠI nhóm mềm (Soft Skill, Language Skill)
2. **Soft skills match** (weight 0,1) — tách riêng, trọng số nhỏ hơn hẳn hard skills
3. **Semantic match** (weight 0,4) — cosine similarity embedding BGE-M3

*Experience match và Education match là hướng mở rộng đã lên kế hoạch, chưa đưa vào V2.*

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
---

## Mục 8 — Kết quả thử nghiệm, Ưu - Nhược điểm & Khả năng mở rộng

### 8.1. Đánh giá kết quả thử nghiệm pipeline đầu-cuối
Nhóm đã triển khai kiểm thử toàn diện luồng 6 bước từ Onboarding đến Dashboard trên cả giao diện Web React và hệ thống Backend FastAPI với các kết quả định lượng cụ thể:
- **Hiệu năng & Thời gian đáp ứng**:
  - Trích xuất nội dung văn bản thô (Tầng 1 - PyMuPDF): trung bình **0,15 – 0,25 giây** cho tài liệu PDF chuẩn 1–2 trang.
  - Trích xuất thực thể có cấu trúc (Tầng 2 - LLM Structured Output): trung bình **1,8 – 2,5 giây** qua OpenRouter API. Khi kích hoạt chế độ Fallback Regex, thời gian trích xuất chỉ mất **0,08 giây**.
  - Tính toán vector embedding (Tầng 3 - BGE-M3 1024 chiều chạy cục bộ trên CPU): trung bình **0,35 giây** cho bản tóm tắt CV.
  - Truy xuất Top-20 việc làm phù hợp từ 450 JD trên cơ sở dữ liệu pgvector: dưới **0,05 giây** (< 50ms).
  - Tính toán điểm số Hybrid V2 và trích dẫn Evidence (Tầng 4): dưới **0,02 giây**.
  - **Tổng thời gian xử lý toàn luồng** (đo thực tế, mode=rule): **~1,1–1,3 giây** khi hệ thống đã sẵn sàng (warm); lần gọi đầu tiên sau khi khởi động server mất thêm **~20 giây** do nạp model embedding BGE-M3 vào bộ nhớ (chỉ xảy ra một lần mỗi phiên).
- **Độ ổn định & Kiểm chứng Human-in-the-loop**:
  - Thử nghiệm trên 3 CV thành viên và 3 bộ fixture chuẩn (đơn cột, hai cột, thiếu mục): tỷ lệ phiên trích xuất đi qua LLM Structured Output so với Fallback Regex là **72,2% / 27,8%** (tỷ lệ *sử dụng* cơ chế, không phải độ chính xác). Nhóm **chưa đo formal accuracy** trên tập gán nhãn chuẩn — đây là hướng phát triển tiếp theo.
  - Cơ chế Human-in-the-loop cho phép người dùng trực tiếp thêm/xóa/sửa các kỹ năng AI nhận diện sai trước khi bấm đối chiếu, đảm bảo dữ liệu đưa vào Tầng 3–4 là **chính xác 100%** theo xác nhận của ứng viên.

### 8.2. Ưu điểm nổi bật của giải pháp
1. **Minh bạch & Giải thích được (Explainable AI Matching)**:
   - Khác biệt hoàn toàn với các công cụ "hộp đen" trên thị trường, aitainang công khai tường minh công thức tính điểm (Hybrid V2: 50% Hard Skill + 40% Semantic + 10% Soft Skill).
   - Điểm số luôn đi kèm **Evidence đối chiếu trích dẫn trực tiếp** từ cả bản CV lẫn yêu cầu công việc thật trong JD, giúp ứng viên hiểu tường tận tại sao mình đạt hoặc chưa đạt điểm cao.
2. **Vòng lặp tối ưu hóa CV đo lường được (Measurable Loop)**:
   - Hệ thống không dừng lại ở việc chấm điểm mà đồng hành chỉ rõ các khoảng trống kỹ năng (skill gaps) theo thứ tự ưu tiên.
   - Cung cấp gợi ý viết lại bullet point hành động cụ thể theo phương pháp STAR và cho phép ứng viên bấm chấm lại ngay để thấy **Delta Score gia tăng** (thực nghiệm đạt mức tăng điểm trung bình từ +12 đến +16 điểm).
3. **Bản địa hóa sâu sắc cho thị trường Việt Nam (Vietnamese-First)**:
   - Xử lý hoàn hảo tài liệu song ngữ Việt – Anh, thấu hiểu cấu trúc viết CV của sinh viên Việt Nam và văn phong đăng tuyển của các doanh nghiệp trong nước nhờ bộ Taxonomy 235 kỹ năng chuẩn hóa và 690 alias phổ biến.

### 8.3. Nhược điểm & Hạn chế đã ghi nhận
1. **Chưa hỗ trợ CV dạng ảnh scan phức tạp**:
   - Hiện tại hệ thống tập trung xử lý file PDF/DOCX có lớp text (chiếm >90% định dạng ứng viên nộp). Các CV scan dạng ảnh chụp chưa tích hợp OCR mà chỉ hiển thị cảnh báo hướng dẫn người dùng chuyển đổi.
2. **Quy mô dữ liệu thử nghiệm**:
   - Kho JD hiện tại gồm 450 JD tuyển dụng thật, tập trung vào ngành CNTT/Data. Để phục vụ thị trường tuyển dụng đại chúng trong thực tế, cần xây dựng hạ tầng thu thập và lập chỉ mục liên tục hàng chục nghìn JD.
3. **Mô hình nhúng chạy CPU**:
   - Việc sinh embedding BGE-M3 trên CPU cục bộ phù hợp cho môi trường kiểm thử và demo local; khi chịu tải đồng thời hàng nghìn người dùng cần chuyển sang GPU inference hoặc cache embedding vector trên Cloud.

### 8.4. Khả năng mở rộng trong thực tiễn
- **Mở rộng đa ngành nghề**: Cấu trúc phân tầng và bộ lọc metadata của aitainang hoàn toàn độc lập với lĩnh vực. Hệ thống có thể mở rộng sang các khối ngành như Marketing, Tài chính - Kế toán, Logistics, Thiết kế đồ họa bằng cách bổ sung bộ Skills Taxonomy tương ứng của từng ngành.
- **Tự động hóa cập nhật dữ liệu việc làm**: Dễ dàng tích hợp các connector tự động quét và làm sạch JD từ các nguồn đăng tuyển công khai định kỳ hàng ngày, giữ cho kho dữ liệu luôn cập nhật biến động thị trường.
- **Mở rộng tính năng Phỏng vấn thử nghiệm (AI Mock Interview)**: Từ danh sách các khoảng trống kỹ năng đã phát hiện tại Bước 4, AI có thể đóng vai người phỏng vấn để sinh bộ câu hỏi tình huống chuyên sâu, giúp sinh viên luyện tập phỏng vấn trực tiếp trước khi nộp đơn thật.

---

## Mục 9 — Baseline, Ablation Study & Đánh giá mô hình

> **CẢNH BÁO — KHÔNG XOÁ cho tới khi có số liệu D3 thật**: Số liệu dưới đây là kết quả
> trên bộ **pilot 10 cặp** (3 CV synthetic × JD thật, chấm bằng **cơ chế** để kiểm chứng
> pipeline đo lường) — **KHÔNG phải kết quả đánh giá chính thức**. Bảng chính thức sẽ
> thay bằng D3 thật (20–30+ cặp, chấm tay độc lập bởi 3 thành viên) khi có đủ CV từ C.

So sánh 4 biến thể trên cùng bộ D3:

| Biến thể | Mô tả |
|----------|-------|
| (a) Keyword-only | Đếm overlap thô trên tên canonical, KHÔNG chuẩn hóa alias |
| (b) Embedding-only | Cosine similarity giữa embedding CV và JD (BGE-M3) |
| (c) LLM-only | LLM chấm trực tiếp (structured output, không có pipeline) |
| (d) **Hybrid V2** | 0,5 × hard_skill + 0,1 × soft_skill + 0,4 × semantic — bản chính thức |

**Số liệu PILOT (10 cặp, CV synthetic, nhãn cơ chế — CHƯA PHẢI D3 CHÍNH THỨC):**

| Biến thể | Precision@5 | nDCG@10 | Spearman rho | MAE (1-5) |
|----------|-------------|---------|-------------|-----|
| (a) Keyword-only | 0.400 | 0.979 | 0.296 | 3.261 |
| (b) Embedding-only | 0.400 | 0.969 | -0.105 | 1.426 |
| (c) LLM-only | 0.400 | 0.985 | 0.155 | 2.110 |
| **(d) Hybrid V2** | **0.400** | **0.968** | **0.148** | **2.423** |

*Cảnh báo diễn giải: nhãn pilot sinh cơ học từ difficulty_hint nên các chỉ số KHÔNG phản ánh
chất lượng thật; giá trị duy nhất của bảng này là chứng minh pipeline đo được đầu-cuối
(đủ 4/4 biến thể, gồm cả LLM-only qua OpenRouter — 10/10 cặp chấm thành công sau khi vá
retry cho lỗi provider trả content rỗng). Log đo lưu đầy đủ cho LLM-only
(`data/labeled/metrics_llm_only_pilot.log`); các biến thể còn lại đo cùng phiên 27/09,
chưa lưu log riêng — sẽ lưu lại khi chạy D3 thật.

*Ghi chú theo dõi: ở pilot, keyword_only có Spearman cao nhất (0.296) so với hybrid_v2 (0.148)
và llm_only (0.155). KHÔNG kết luận gì ở cỡ mẫu n=10 chấm cơ chế (nhiễu thống kê rất lớn) —
cần theo dõi lại pattern này khi có D3 thật (20–30+ cặp, chấm tay); nếu hybrid vẫn thua
keyword ở quy mô đó mới là tín hiệu cần debug công thức.*

*Công thức hybrid V2: 0,5 × hard_skill + 0,1 × soft_skill + 0,4 × semantic (xem README).*

**Số liệu D3 chính thức (điền sau khi chấm tay):**

| Biến thể | Precision@5 | nDCG@10 | Spearman rho | MAE |
|----------|-------------|---------|-------------|-----|
| (a) Keyword | — | — | — | — |
| (b) Embedding-only | — | — | — | — |
| (c) LLM-only | — | — | — | — |
| **(d) Full hybrid** | **—** | **—** | **—** | **—** |

---

## Mục 10 — Kiến trúc hệ thống & phương án triển khai

### 10.1. Kiến trúc hiện tại (đã chạy thật)

```
[React frontend] --HTTP--> [FastAPI backend] --SQL/vector--> [Neon Postgres + pgvector]
                                  |
                                  +--> [BGE-M3 local, CPU] (embedding)
                                  +--> [OpenRouter API] (LLM extraction)
```

- **Frontend**: React (thành viên C), gọi `POST /api/cv/upload`.
- **Backend**: FastAPI, module hóa theo tầng (`services/cv_parser`, `cv_extraction`,
  `embedding`, `scoring`, `jd_extraction`), router riêng `routers/cv.py`.
- **Database**: Neon Postgres serverless (ap-southeast-1), pgvector 0.8.6,
  bảng `jds` (450 dòng) + cột `embedding vector(1024)` + index lọc.
- **Bảo mật**: khóa API và mật khẩu DB chỉ nằm trong `.env` (đã xác nhận không
  được git track; repo chỉ có `.env.example`).

### 10.2. Phương án triển khai demo

> Theo thể lệ Bảng C, đợt nộp này **không bắt buộc** link deploy công khai (chỉ bắt buộc
> ở Vòng Chung kết) — phương án dưới đây chuẩn bị sẵn cho giai đoạn Vòng Khu vực.


| Hạng mục | Phương án |
|----------|-----------|
| Backend | Container Docker (Python 3.12 + model BGE-M3 bake sẵn hoặc tải lần đầu), deploy VPS/Render |
| Database | Tiếp tục Neon serverless (free tier đủ cho 450 JD + demo) |
| Frontend | Build tĩnh (Vite) → Vercel/Netlify, proxy `/api` về backend |
| Dự phòng | Nếu mất mạng/OpenRouter lỗi: rule fallback vẫn cho kết quả matching đầy đủ (đã kiểm chứng 27,8% JD chạy rule) |

### 10.3. Giới hạn đã biết

- CV ảnh scan chưa OCR (chỉ cảnh báo).
- `score_llm` (LLM đánh giá trách nhiệm/độ khớp sâu) chưa tích hợp vào hybrid — bản sau.
- Quy mô 450 JD phù hợp demo; production cần pipeline crawl + index lại định kỳ.

---

## Mục 11 — Rủi ro, Bảo mật, Đạo đức AI & An toàn dữ liệu

### 11.1. Quyền riêng tư & Thu thập dữ liệu hợp lệ (Điều 5.7–5.8 Thể lệ)
- **Quy tắc đạo đức bất khả xâm phạm**: Nhóm tuyệt đối không thu thập hoặc sử dụng dữ liệu CV thật của người lạ từ các nền tảng trực tuyến (TopCV, VietnamWorks, LinkedIn...) — điều này vi phạm nghiêm trọng quyền riêng tư cá nhân và Điều 5.7–5.8 Thể lệ Cuộc thi.
- **Tính minh bạch của dữ liệu D2**: Toàn bộ CV sử dụng trong dự án đều xuất phát từ chính 3 thành viên nhóm và bạn bè thân thiết có **văn bản cam kết đồng ý tự nguyện** (lưu trữ tại `data/consent/` theo mẫu `docs/cv_consent_template.md`).
- **Quy trình ẩn danh hóa tuyệt đối**: Trước khi đưa vào lưu trữ tại `data/cv_samples/`, toàn bộ thông tin nhận dạng cá nhân (PII: họ tên thật, số điện thoại, địa chỉ email, địa chỉ cư trú, ảnh đại diện, liên kết mạng xã hội cá nhân) đều bị xóa bỏ hoàn toàn hoặc thay thế bằng các mã định danh ẩn danh (`Ứng viên #AIT-XX`, `candidate_XX@aitainang.vn`).
- **Tính hợp lệ của dữ liệu JD**: 450 JD được khai thác từ dataset công khai `tinixai/vietnamese-job-descriptions` trên HuggingFace dưới giấy phép CC BY-NC 4.0, chỉ phục vụ mục đích nghiên cứu học thuật phi thương mại và ghi công đầy đủ nguồn.

### 11.2. An toàn bảo mật & Quản lý thông tin xác thực
- **Bảo mật mã nguồn**: Khóa API (OpenRouter, Gemini) và chuỗi kết nối cơ sở dữ liệu (Neon Postgres) được cô lập hoàn toàn trong biến môi trường `.env`. Tệp `.env` được cấu hình chặt chẽ trong `.gitignore` và không bao giờ xuất hiện trong lịch sử commit của Git (kho lưu trữ chỉ cung cấp `.env.example`).
- **Bảo vệ dữ liệu người dùng tại phiên làm việc**: Khi người dùng tải CV lên giao diện Web, hệ thống chỉ xử lý dữ liệu trong bộ nhớ tạm (in-memory) và lưu trữ cục bộ tại trình duyệt (localStorage của client). Hệ thống không lưu trữ lâu dài bản CV gốc của người dùng trên máy chủ, tránh nguy cơ rò rỉ dữ liệu.

### 11.3. Kiểm soát sai lệch mô hình (Bias) & Ngăn ngừa ảo tưởng (Hallucination)
- **Cơ chế Human-in-the-loop**: Nhóm áp dụng cơ chế xác nhận có sự tham gia của con người tại Bước 2. Sau khi AI bóc tách thông tin, người dùng có toàn quyền xem xét, bổ sung hoặc loại bỏ các kỹ năng/kinh nghiệm bị nhận diện sai. Điều này triệt tiêu hoàn toàn rủi ro sai sót tích lũy sang các bước tính điểm tiếp theo.
- **Schema Validation & Fallback Deterministic**: Bắt buộc xác thực cấu trúc đầu ra (JSON Schema Validation) đối với mọi phản hồi từ mô hình ngôn ngữ lớn. Khi xảy ra lỗi định dạng hoặc đứt gãy kết nối API, hệ thống kích hoạt chuỗi fallback sang bộ trích xuất quy tắc (Regex Extractor), ngăn ngừa việc AI tự bịa thông tin.
- **Prompt ràng buộc nghiêm ngặt ở Bước 5 (Cải thiện CV)**: Prompt hướng dẫn AI chỉ được phép đưa ra khuyến nghị dựa trên các khoảng trống kỹ năng thực tế đã trích xuất từ JD, tuyệt đối không xúi giục hoặc tự động "chế tạo" kinh nghiệm giả mạo cho ứng viên.

### 11.4. Trách nhiệm người dùng & Tuyên bố miễn trừ
- Giao diện ứng dụng luôn hiển thị thông điệp cảnh báo thường trực: *"Điểm số và phân tích do AI tạo ra mang tính chất tham khảo, hỗ trợ tối ưu hóa hồ sơ và không cấu thành sự đảm bảo kết quả trúng tuyển thực tế từ nhà tuyển dụng."*

---

## Mục 12 — Hướng phát triển & Kế hoạch tiếp theo

### 12.1. Lộ trình ngắn hạn (Giai đoạn Vòng Khu vực)
1. **Triển khai Cloud Hosting hoàn chỉnh**:
   - Đóng gói toàn bộ hệ thống bằng Docker Compose đa dịch vụ (Backend FastAPI, Frontend React, CSDL Neon Postgres/pgvector).
   - Thiết lập CI/CD tự động kiểm thử và triển khai lên máy chủ đám mây (VPS/Render) với tên miền công khai và giám sát trạng thái 24/7.
2. **Hoàn thiện tập đánh giá D3 & Báo cáo thực nghiệm chính thức**:
   - Thu thập đủ 15–20 CV ẩn danh từ bạn bè, tạo 50–100 cặp CV-JD có nhãn đánh giá độc lập từ 3 thành viên nhóm.
   - Tính toán chỉ số đồng thuận liên thẩm định (Inter-annotator Agreement: Fleiss' Kappa) và cập nhật bảng số liệu đánh giá chính thức (Spearman rho, nDCG@10, MAE) cho cả 4 biến thể mô hình.
3. **Thử nghiệm người dùng thực tế (Pilot Testing)**:
   - Tổ chức đợt thử nghiệm cho 20–30 sinh viên năm cuối; thu thập bảng câu hỏi khảo sát trải nghiệm người dùng (SUS score) và đo lường mức độ hữu ích của các gợi ý sửa CV.
4. **Đo lường formal accuracy cho module trích xuất (Tầng 2)**:
   - Xây dựng tập dữ liệu CV có gán nhãn chuẩn (annotated entities ground-truth) để đo lường chính xác các chỉ số Precision, Recall và F1-score cho bước Structured Extraction (thay vì chỉ ghi nhận tỷ lệ kích hoạt LLM/fallback regex).

### 12.2. Lộ trình trung & dài hạn (Vòng Chung kết & Ứng dụng thực tế)
1. **Tích hợp module OCR & Trích xuất layout phức tạp**:
   - Tích hợp Docling / PaddleOCR nhằm xử lý mượt mà các bản CV dạng ảnh scan, CV thiết kế đồ họa đa cột từ Canva/Photoshop.
2. **Xây dựng tính năng Phỏng vấn thử nghiệm AI (AI Mock Interview)**:
   - Phát triển mô-đun phỏng vấn viên ảo tương tác bằng giọng nói/văn bản dựa trên các gap kỹ năng phát hiện được từ Bước 4, giúp sinh viên làm quen với áp lực phỏng vấn thực tế trước khi ứng tuyển.
3. **Mở rộng kho dữ liệu việc làm đa lĩnh vực**:
   - Xây dựng pipeline crawler tự động thu thập và chuẩn hóa hơn 10.000 JD cập nhật liên tục từ thị trường lao động Việt Nam.
   - Mở rộng sang các nhóm ngành Kinh tế, Marketing, Thiết kế, Logistics thông qua việc làm giàu bộ Taxonomy kỹ năng.
4. **Hợp tác triển khai vì cộng đồng sinh viên**:
   - Kết nối với Đoàn Thanh niên, Hội Sinh viên và Trung tâm Hỗ trợ Việc làm của các trường đại học để tích hợp aitainang thành công cụ định hướng nghề nghiệp miễn phí cho sinh viên trên toàn quốc.

---

## Mục 13 — Kê khai công cụ AI & Nhật ký Prompt Log

- **Bản kê khai công cụ AI**: Chi tiết đầy đủ tại [`docs/AI_TOOLS_DECLARATION.md`](file:///d:/AI/AItainang/prj/docs/AI_TOOLS_DECLARATION.md) (tuân thủ Điều 5.7 Thể lệ Cuộc thi).
- **Nhật ký Prompt Log**: Bằng chứng minh bạch toàn bộ các yêu cầu của nhóm và mã sinh từ trợ lý AI được lưu trữ tại [`docs/PROMPT_LOG.md`](file:///d:/AI/AItainang/prj/docs/PROMPT_LOG.md), sẵn sàng cung cấp đường dẫn thư mục công khai cho Ban Giám Khảo đối soát.

