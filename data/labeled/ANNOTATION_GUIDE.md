# Hướng dẫn gán nhãn D3 — Đánh giá cặp (CV, JD)

## Mục đích
Xây bộ ground truth 50–100 cặp (CV, JD) để đánh giá chất lượng pipeline matching.
Mỗi cặp được 3 người chấm độc lập → đo inter-annotator agreement → dùng cho Precision@5,
nDCG@10, Spearman correlation, MAE (mục 7, 9 hồ sơ Mẫu 3).

## Quy trình

### Bước 1: Ghép cặp (A làm)
- Script `scripts/generate_annotation_pairs.py` ghép CV × JD phân tầng:
  - Đảm bảo đủ 3 mức khó: easy (rõ ràng phù hợp/không phù hợp), medium, hard (khó phân biệt).
  - Mỗi CV ghép với 3–5 JD (mix ngành khác nhau).
- Output: `data/labeled/annotation_pairs.csv` (cv_id, jd_id).

### Bước 2: Chấm độc lập (3 người)
- Mỗi người nhận file riêng: `annotations_A.csv`, `annotations_B.csv`, `annotations_C.csv`.
- **KHÔNG** trao đổi điểm với nhau cho đến khi cả 3 hoàn thành.
- Mỗi dòng chấm: score 1–5 + lý do ngắn (1–2 câu).

### Bước 3: Đối chiếu (A tổng hợp)
- Script `scripts/compute_agreement.py` tính Fleiss' kappa / Krippendorff's alpha.
- Nếu kappa < 0,6 → rà soát guideline, chấm lại các cặp bất đồng (|max - min| ≥ 3).
- Điểm cuối cùng: trung bình 3 người.

## Thang điểm

| Score | Mức | Định nghĩa |
|-------|-----|-----------|
| 1 | Không liên quan | CV hoàn toàn không liên quan đến JD (khác ngành, khác level hoàn toàn) |
| 2 | Yếu | Có 1–2 điểm chung rất nhỏ, nhưng overall không phù hợp |
| 3 | Trung bình | Có overlap một số kỹ năng/kinh nghiệm, nhưng thiếu nhiều yêu cầu quan trọng |
| 4 | Khá | Phần lớn yêu cầu JD được CV đáp ứng, chỉ thiếu 1–2 điểm phụ |
| 5 | Rất phù hợp | CV đáp ứng gần như toàn bộ yêu cầu JD, có thể mời phỏng vấn ngay |

## Tiêu chí chấm chi tiết

Khi chấm, cân nhắc 4 chiều (nhưng chỉ cho **1 điểm tổng hợp** 1–5):

1. **Kỹ năng cứng (hard skills)**: CV có đáp ứng các kỹ năng kỹ thuật JD yêu cầu không?
   - Trọng số cao nhất. Thiếu skill cốt lõi → -2 điểm.
2. **Kỹ năng mềm (soft skills)**: Teamwork, communication, tiếng Anh…
   - Trọng số thấp hơn. Thiếu soft skill → -0,5 điểm.
3. **Kinh nghiệm (years)**: Số năm kinh nghiệm CV vs JD yêu cầu.
   - Thiếu ≥2 năm so với yêu cầu → -1 điểm.
4. **Học vấn (education)**: Bằng cấp, chuyên ngành.
   - Không đúng chuyên ngành yêu cầu → -0,5 điểm.

## Ghi chú lý do (bắt buộc)

Mỗi điểm **phải kèm** 1–2 câu giải thích, ví dụ:
- "Score 4: CV có 3/4 skill cứng JD yêu cầu (Python, SQL, Docker), thiếu Kubernetes. Kinh nghiệm đủ."
- "Score 2: CV là frontend (React), JD yêu cầu Data Engineer. Chỉ overlap Python."
- "Score 1: CV ngành Marketing, JD là Security Engineer. Không liên quan."

## File output

Cấu trúc `data/labeled/`:
```
data/labeled/
  annotation_pairs.csv       # Danh sách cặp (cv_id, jd_id) cần chấm
  annotations_A.csv          # Kết quả của người A
  annotations_B.csv          # Kết quả của người B
  annotations_C.csv          # Kết quả của người C
  annotations_merged.csv     # Tổng hợp + điểm cuối cùng
  agreement_report.md        # Kết quả đo inter-annotator agreement
```
