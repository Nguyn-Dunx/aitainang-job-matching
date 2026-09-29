"""
Tính inter-annotator agreement cho D3.
Đo Fleiss' kappa và Krippendorff's alpha từ 3 file annotations.

Usage:
    python scripts/compute_agreement.py \
        --files data/labeled/annotations_A.csv data/labeled/annotations_B.csv data/labeled/annotations_C.csv \
        --output data/labeled/agreement_report.md
"""
import argparse
import csv
from pathlib import Path


def load_annotations(filepath):
    """Load annotations from CSV. Return dict: (cv_id, jd_id) -> score."""
    annotations = {}
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["cv_id"].strip(), row["jd_id"].strip())
            score_str = row.get("score", "").strip()
            if score_str and score_str.isdigit():
                annotations[key] = int(score_str)
    return annotations


def fleiss_kappa(ratings_matrix, n_categories=5):
    """
    Compute Fleiss' kappa for inter-rater agreement.
    ratings_matrix: list of lists, each inner list = counts of ratings per category for one item.
    """
    N = len(ratings_matrix)
    if N == 0:
        return 0.0

    n = sum(ratings_matrix[0])  # number of raters per item
    if n <= 1:
        return 0.0

    k = n_categories

    # P_i for each item
    P_items = []
    for row in ratings_matrix:
        sum_sq = sum(r * r for r in row)
        P_i = (sum_sq - n) / (n * (n - 1)) if n > 1 else 0
        P_items.append(P_i)

    P_bar = sum(P_items) / N

    # P_j for each category
    p_j = []
    for j in range(k):
        total = sum(row[j] for row in ratings_matrix)
        p_j.append(total / (N * n))

    P_e = sum(p * p for p in p_j)

    if P_e == 1:
        return 1.0

    kappa = (P_bar - P_e) / (1 - P_e)
    return kappa


def krippendorff_alpha(data, n_categories=5):
    """
    Simplified Krippendorff's alpha for ordinal data (3 raters).
    data: dict (cv_id, jd_id) -> list of scores from each rater (None if missing).
    """
    # Compute observed and expected disagreement
    pairs_observed = 0
    disagreement_observed = 0
    all_values = []

    for key, scores in data.items():  # noqa: PERF102
        valid = [s for s in scores if s is not None]
        if len(valid) < 2:
            continue
        all_values.extend(valid)
        n = len(valid)
        for i in range(n):
            for j in range(i + 1, n):
                pairs_observed += 1
                disagreement_observed += (valid[i] - valid[j]) ** 2

    if pairs_observed == 0:
        return 0.0

    Do = disagreement_observed / pairs_observed

    # Expected disagreement
    N = len(all_values)
    if N < 2:
        return 0.0

    pairs_expected = 0
    disagreement_expected = 0
    for i in range(N):
        for j in range(i + 1, N):
            pairs_expected += 1
            disagreement_expected += (all_values[i] - all_values[j]) ** 2

    De = disagreement_expected / pairs_expected

    if De == 0:
        return 1.0

    alpha = 1 - Do / De
    return alpha


def main():
    parser = argparse.ArgumentParser(description="Compute inter-annotator agreement")
    parser.add_argument("--files", nargs="+",
                        default=[
                            "data/labeled/annotations_A.csv",
                            "data/labeled/annotations_B.csv",
                            "data/labeled/annotations_C.csv",
                        ])
    parser.add_argument("--output", default="data/labeled/agreement_report.md")
    parser.add_argument("--merge-output", default="data/labeled/annotations_merged.csv")
    args = parser.parse_args()

    # Load all annotations
    all_anns = []
    annotator_names = []
    for fp in args.files:
        path = Path(fp)
        if not path.exists():
            print(f"⚠️  File {fp} chưa tồn tại — bỏ qua.")
            continue
        anns = load_annotations(path)
        if anns:
            all_anns.append(anns)
            annotator_names.append(path.stem.split("_")[-1])
            print(f"✅ Loaded {path.name}: {len(anns)} annotations")
        else:
            print(f"⚠️  File {fp} trống hoặc chưa có điểm.")

    if len(all_anns) < 2:
        print("\n⚠️  Cần ít nhất 2 người chấm để tính agreement. Chưa đủ dữ liệu.")
        return

    # Merge into aligned data
    all_keys = set()
    for anns in all_anns:
        all_keys.update(anns.keys())

    merged_data = {}
    for key in sorted(all_keys):
        scores = [anns.get(key) for anns in all_anns]
        merged_data[key] = scores

    # Items with all raters
    complete = {k: v for k, v in merged_data.items()
                if all(s is not None for s in v)}
    print("\n📊 Thống kê:")
    print(f"   Tổng cặp unique: {len(all_keys)}")
    print(f"   Cặp có đủ {len(all_anns)} người chấm: {len(complete)}")

    if not complete:
        print("⚠️  Chưa có cặp nào được cả 3 người chấm. Chưa tính agreement.")
        return

    # Build Fleiss matrix
    n_raters = len(all_anns)  # noqa: F841
    ratings_matrix = []
    for key, scores in complete.items():
        row = [0] * 5  # categories 1-5
        for s in scores:
            if 1 <= s <= 5:
                row[s - 1] += 1
        ratings_matrix.append(row)

    kappa = fleiss_kappa(ratings_matrix, n_categories=5)
    alpha = krippendorff_alpha(complete, n_categories=5)

    print("\n📏 Agreement:")
    print(f"   Fleiss' kappa: {kappa:.3f}")
    print(f"   Krippendorff's alpha: {alpha:.3f}")

    # Interpretation
    if kappa >= 0.8:
        interpretation = "Rất tốt (almost perfect agreement)"
    elif kappa >= 0.6:
        interpretation = "Tốt (substantial agreement)"
    elif kappa >= 0.4:
        interpretation = "Trung bình (moderate agreement)"
    elif kappa >= 0.2:
        interpretation = "Yếu (fair agreement) — cần rà soát guideline"
    else:
        interpretation = "Kém (poor/slight agreement) — cần chấm lại"

    print(f"   Đánh giá: {interpretation}")

    # Find disagreements
    disagreements = []
    for key, scores in complete.items():
        valid = [s for s in scores if s is not None]
        if max(valid) - min(valid) >= 3:
            disagreements.append((key, scores))

    print(f"\n⚠️  Cặp bất đồng lớn (|max-min| >= 3): {len(disagreements)}")

    # Save merged
    merge_path = Path(args.merge_output)
    merge_path.parent.mkdir(parents=True, exist_ok=True)
    with open(merge_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        headers = ["cv_id", "jd_id"]
        for name in annotator_names:
            headers.append(f"score_{name}")
        headers.extend(["score_mean", "score_std", "disagreement_flag"])
        writer.writerow(headers)

        for key in sorted(complete.keys()):
            scores = complete[key]
            valid = [s for s in scores if s is not None]
            mean = sum(valid) / len(valid)
            std = (sum((s - mean) ** 2 for s in valid) / len(valid)) ** 0.5
            flag = "⚠️" if max(valid) - min(valid) >= 3 else ""
            row = [key[0], key[1]] + scores + [f"{mean:.1f}", f"{std:.2f}", flag]
            writer.writerow(row)

    print(f"💾 Merged annotations: {merge_path}")

    # Save report
    report_path = Path(args.output)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# D3 — Inter-Annotator Agreement Report\n\n")
        f.write("## Thống kê\n\n")
        f.write(f"- Số người chấm: {len(all_anns)}\n")
        f.write(f"- Tổng cặp unique: {len(all_keys)}\n")
        f.write(f"- Cặp đủ {len(all_anns)} người: {len(complete)}\n\n")
        f.write("## Agreement\n\n")
        f.write("| Metric | Giá trị | Đánh giá |\n")
        f.write("|--------|---------|----------|\n")
        f.write(f"| Fleiss' kappa | {kappa:.3f} | {interpretation} |\n")
        f.write(f"| Krippendorff's alpha | {alpha:.3f} | — |\n\n")
        f.write("## Cặp bất đồng lớn (|max-min| >= 3)\n\n")
        if disagreements:
            f.write("| cv_id | jd_id | Scores |\n")
            f.write("|-------|-------|--------|\n")
            for key, scores in disagreements:
                f.write(f"| {key[0]} | {key[1]} | {scores} |\n")
        else:
            f.write("Không có cặp bất đồng lớn.\n")

    print(f"💾 Report: {report_path}")
    print("\n✅ Hoàn tất tính agreement!")


if __name__ == "__main__":
    main()
