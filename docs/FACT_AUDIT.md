# FACT AUDIT — Hồ sơ & Kịch bản video (ngày 28/09/2026)

> Mỗi dòng: vị trí | khẳng định | nguồn xác minh | kết luận | xử lý.
> Nguồn xác minh = file code / lệnh đo chạy ngày 28/09 / báo cáo cụ thể. "KHÔNG CÓ NGUỒN" = không tìm thấy đo lường hay trích dẫn nào trong repo.
> Phân công: "Neko đã sửa" = commit này; "C sửa" = mục 1, 2, 8, 11, 12 của mau3_draft.md (tránh xung đột commit).

## A. docs/mau3_draft.md

### Mục 1 (C sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 1.1 | ">70% sinh viên cảm thấy hoang mang khi đối chiếu năng lực với yêu cầu tuyển dụng" | KHÔNG CÓ NGUỒN — không có khảo sát/trích dẫn nào trong repo | CHƯA CÓ NGUỒN | C sửa: trích dẫn khảo sát thật (NACENFCT, TopDev...) hoặc bỏ con số |
| 1.1 | "Tỷ lệ hồ sơ nhận phản hồi phỏng vấn vòng đầu... dưới 10%" | KHÔNG CÓ NGUỒN | CHƯA CÓ NGUỒN | C sửa: như trên |

### Mục 2 (C sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 2.2 | "thời gian phản hồi matching dưới 1 giây" | Đo thật 27/09 (curl): toàn luồng upload warm 1,1–1,3 s; riêng retrieval pgvector ~60 ms + scoring <20 ms thì đúng dưới 1 s | THIẾU NGỮ CẢNH — dễ bị hiểu sai | C sửa: tách rõ "truy xuất+chấm điểm <1 s; toàn luồng 1,1–1,3 s warm" |

### Mục 3 (đã xác minh — không cần sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận |
|---|---|---|---|
| 3.1 D1 | "450 JD, 369 công ty" | DB `COUNT(*) jds`=450; `data/raw/hf_it_jds_filtered.json` distinct company=369 | ĐÚNG |
| 3.2 | Funnel 606.878 → 10.572 → 9.768 → 9.748 → 450 | `data/DATA_SOURCES.md` (bảng lọc từng bước) | ĐÚNG |

### Mục 4 (Neko đã sửa trong commit này)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 4.1 | "LLM 320/450 (72,2%)" | DB: `parsed->skills_info->method` = llm **325**/450 (72,2%), rule 125/450 (27,8%) | SAI SỐ (320→325) | Neko đã sửa |
| 4.1 | "99% JD (446/450) có ≥1 skill; TB 8,6 skill/JD" | DB đếm lại 28/09: **450/450 (100%)**, TB **11,7** skill/JD (số cũ từ taxonomy v1.0 trước khi trích xuất lại) | SAI (số cũ) | Neko đã sửa |
| 4.1 | Taxonomy 235 mục + 690 alias, active 211/235 (89,8%) | `data/taxonomy/skills_taxonomy.json` metadata (v1.1.0) | ĐÚNG | — |
| 4.1 | Communication 48,7% / Report Writing 42,9% / English 40,2% | `data/taxonomy/skills_summary.txt` (rank 1-3) | ĐÚNG | — |

### Mục 5 (đã xác minh — không cần sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận |
|---|---|---|---|
| 5 | cosine cùng ý 0,784 > 0,7; khác ý 0,466 < 0,5 | `scripts/de_risk_embedding.py` chạy lại 28/09 ra đúng 0.784 / 0.466 | ĐÚNG |

### Mục 6 (Neko đã sửa trong commit này)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 6 | "~0,8–1,0 s/JD trên CPU" (import embedding) | KHÔNG CÓ LOG LƯU; đo warm 28/09: 82–127 ms/câu ngắn → JD dài ~0,8–1 s là hợp lý nhưng vẫn là ước tính | ƯỚC TÍNH | Neko đã thêm caveat "ước tính, chưa lưu log đo riêng" |
| 6 | "E2E test thật: ... (24,7 s)" | Đo pytest phiên 27/09 — gồm cả thời gian khởi động app trong test; request đơn lẻ warm đo riêng 1,1–1,3 s | THIẾU NGỮ CẢNH | Neko đã làm rõ ngữ cảnh trong ngoặc |
| 6 | "import 450/450 JD, 450/450 embedding, 0 dòng thiếu cột lọc" | DB verify 28/09: 450 dòng, 0 embedding NULL, 0 dòng thiếu cột lọc | ĐÚNG | — |

### Mục 8 (C sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 8.1 | "72,2%/27,8%" gán cho "thử nghiệm trên 3 CV thành viên và 3 bộ fixture" | Nguồn thật: DB method trên **450 JD** (llm 325 / rule 125) — KHÔNG phải số đo trên 3 CV + 3 fixture | SAI GÁN NGUỒN | C sửa: chuyển câu này về mục 4.1 (450 JD) hoặc đo riêng trên 3 CV + 3 fixture rồi báo số mới |
| 8.1 | "Truy xuất Top-20 việc làm... dưới 0,05 giây" | Code `app/routers/cv.py`: truy xuất top_k×3 = **30** ứng viên (mặc định top_k=10); đo pgvector 28/09: warm 55–72 ms, lần đầu 441 ms | SAI (cả Top-20 lẫn <50ms) | C sửa: "truy xuất Top-30 ứng viên ~60 ms warm" |
| 8.1 | "0,15–0,25 s parse / 1,8–2,5 s LLM / 0,08 s rule / 0,35 s embedding / <0,02 s scoring" | KHÔNG CÓ LOG LƯU cho từng tầng. Đo lại 28/09: embedding warm 82–127 ms (khớp thứ tự độ lớn, nhưng số 0,35 s không đúng); các tầng còn lại chưa đo lại | KHÔNG CÓ NGUỒN LƯU | C sửa: đo lại từng tầng rồi thay, hoặc bỏ con số chi tiết |
| 8.1 | "Human-in-the-loop... chính xác 100% theo xác nhận của ứng viên" | KHÔNG CÓ NGUỒN — chưa có phiên xác nhận nào được ghi lại | CHƯA CÓ NGUỒN | C sửa: bỏ "100%" hoặc làm phiên xác nhận thật (3 CV nội bộ) và ghi log |
| 8.2 | "thực nghiệm đạt mức tăng điểm trung bình từ +12 đến +16 điểm" | KHÔNG CÓ NGUỒN. Số đo thật hiện có: +33,4 (1 cặp, cv_member_01_backend × JD sysadmin, commit 595bf4d); bảng 9 cặp (scripts/eval_improve_delta.py, cùng commit này) sẽ cho min/median/max thật | SAI (số bịa) | C sửa: thay bằng min/median/max từ `data/labeled/improve_delta_report.md` |
| 8.1 | "92% độ chính xác trích xuất" | Đã xoá và thay bằng mô tả đúng (LLM/rule 72,2/27,8 + "chưa đo formal accuracy") | ĐÃ SỬA (commit 595bf4d) | — |
| 8.1 | "Tổng thời gian toàn luồng dưới 3,5 giây" | Đã thay bằng số đo thật: warm 1,1–1,3 s; cold +~20 s nạp model | ĐÃ SỬA (commit 595bf4d) | — |

### Mục 9 (Neko đã bổ sung ghi chú)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 9 | Bảng pilot 4 biến thể (P@5, nDCG@10, Spearman, MAE) | Đo phiên 27/09 qua `scripts/compute_metrics.py`; log lưu đầy đủ chỉ cho llm_only (`data/labeled/metrics_llm_only_pilot.log`); 3 biến thể còn lại đo cùng phiên, chưa lưu log riêng | ĐÚNG (đã gắn nhãn pilot rõ) | Neko đã thêm ghi chú nguồn log vào cảnh báo diễn giải |

### Mục 10 (đã xác minh — không cần sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận |
|---|---|---|---|
| 10.1 | "bảng jds (450 dòng)", pgvector 0.8.6, Neon ap-southeast-1 | DB verify 28/09: 450 dòng, extversion 0.8.6, host `.ap-southeast-1.aws.neon.tech` | ĐÚNG |

### Mục 11, 12 (C sửa)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| 11/12 | (kiểm tra khi đọc: các cam kết lộ trình, deploy cloud, mock interview) | Đây là kế hoạch tương lai — không cần nguồn đo, nhưng KHÔNG được trình bày như tính năng đã có | LƯU Ý | C rà soát khi viết: mọi tính năng tương lai phải ở thời tương lai |

## B. docs/DEMO_VIDEO_SCRIPT.md (Neko đã sửa trong commit này)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| P3 + Cảnh 3 | "ngăn chặn hoàn toàn hiện tượng hallucination" | Human-in-the-loop giảm thiểu nhưng không "hoàn toàn" | OVERCLAIM | Neko đã sửa → "giảm thiểu" |
| P4 | "75 job thật" (tab Data/AI/ML) | DB: industry_group='Data/AI/ML' = 75 | ĐÚNG | — |
| P5 | "ví dụ 86%" | Minh hoạ — điểm thật do backend trả lúc quay | GIỮ (đã ghi "ví dụ") | Khi quay phải dùng điểm backend thật |
| P6 + Cảnh 6 | "ví dụ thiếu Docker, Redis" | Cặp đo thật thiếu Firewall, Load Balancer, Networking, Windows Server | SAI VÍ DỤ | Neko đã sửa theo cặp đo thật |
| P6 + Cảnh 6 | "gợi ý viết lại bullet point cụ thể / theo phương pháp STAR" | Thực tế: gợi ý **dạng điều kiện** ("Nếu bạn đã từng..."), không phải STAR | SAI MÔ TẢ TÍNH NĂNG | Neko đã sửa thành mô tả đúng |
| P6 | "+33,4 điểm (33,4 → 66,8)" | Đo thật 27/09, endpoint `/api/cv/suggest-improvement` | ĐÚNG | — |

## C. docs/PRESENTATION_VIDEO_SCRIPT.md (Neko đã sửa trong commit này)

| Vị trí | Khẳng định | Nguồn | Kết luận | Xử lý |
|---|---|---|---|---|
| Slide 2 | "Tỷ lệ CV gửi đi không phản hồi (>90%)" | KHÔNG CÓ NGUỒN | CHƯA CÓ NGUỒN | Neko đã sửa → bỏ con số, ghi chú cần trích dẫn thật |
| Slide 4 | "ngăn chặn hoàn toàn hallucination" | Overclaim | OVERCLAIM | Neko đã sửa → "giảm thiểu" |
| Slide 5 | "Bảng Ablation Study so sánh 4 biến thể" | Chỉ có số pilot 10 cặp, nhãn tự sinh (đã gắn nhãn ở mục 9 mau3) | THIẾU NHÃN PILOT | Neko đã thêm "(kết quả pilot 10 cặp, nhãn tự sinh — chưa phải D3 chính thức)" |
| Slide 5 | "Thời gian truy xuất pgvector < 50ms" | Đo thật 28/09: warm 55–72 ms (TB ~60 ms), lần đầu 441 ms | SAI | Neko đã sửa → "~60 ms warm (đo thật 5 lần: 55–72 ms; lần đầu 441 ms)" |
| Slide 6 | "Khảo sát pilot: 100% người dùng đánh giá cao" | KHÔNG CÓ NGUỒN — chưa có khảo sát nào | SAI (số bịa) | Neko đã bỏ dòng này; C quyết nội dung thay (làm khảo sát thật hoặc thay bằng minh chứng khác) |
| Slide 6 | "điểm số tăng từ 72 lên 88" | Số bịa cũ; đo thật: 33,4 → 66,8 (+33,4) | SAI | Neko đã sửa theo số đo thật |

## D. Xác minh kiến trúc (trả lời câu hỏi audit)

- **Retrieval dùng pgvector query thật, KHÔNG phải numpy in-memory**: `app/routers/cv.py` dòng 90-99 — SQL `ORDER BY embedding <=> CAST(:q AS vector) LIMIT :k` chạy trên bảng `jds` (Neon Postgres, pgvector 0.8.6). File `data/processed/jds_embeddings.npy` tồn tại nhưng KHÔNG được dùng trong luồng `/api/cv/upload`.
- **Latency pgvector đo thật (28/09, top-30 trên 450 JD)**: lần đầu 441 ms (cold connection), sau đó 55/64/62/72 ms — warm TB ~60 ms.
- **Embedding CV đo thật (28/09)**: cold 20,3 s (nạp BGE-M3, 1 lần mỗi phiên), warm 82–127 ms/câu.
- **Latency LLM Tầng 5 đo thật qua endpoint `/api/cv/suggest-improvement` (29/09/2026, cấu hình `.env` mới — model chính `nvidia/nemotron-3-super-120b-a12b`, fallback `nvidia/nemotron-3-ultra-550b-a55b`, CV `cv_member_01_backend.json` × top-1 match thật, JD "Backend Developer (Node.JS/PHP)")**:
  - **Super (model chính, budget 45 s)**: 3/3 lần OK — min 21,3 s / median 24,0 s / max 42,8 s. Lần max 42,8 s đã sát ngưỡng 45 s.
  - **Ultra (fallback, budget 15 s trong code)**: đo qua đường fallback thật của endpoint — 3/3 lần THẤT BẠI (2 lần 503 "Service temporarily overloaded" từ NVIDIA sau 1–4 s, 1 lần timeout đúng 15 s). Khi tạm nâng cap lên 120 s để lấy số thật: 64,7 s và 90,3 s (median 77,5 s) — ultra KHÔNG THỂ thành công trong budget 15 s hiện tại, thậm chí vượt cả 45 s của model chính.
  - Kết luận: fallback hiện tại chỉ là "cứ thử rồi báo timeout" — không mang lại gợi ý thật. Cần quyết định của người dùng (xem SUBMISSION_CHECKLIST / báo cáo BƯỚC 0).
