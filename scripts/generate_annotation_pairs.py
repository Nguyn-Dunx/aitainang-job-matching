"""
Tạo danh sách cặp (CV, JD) cần gán nhãn cho D3.
Phân tầng: đảm bảo đủ easy/medium/hard, đa dạng industry_group.

Chạy sau khi có đủ CV (data/cv_samples/) và JD (data/processed/jds.json).

Usage:
    python scripts/generate_annotation_pairs.py \
        --cv-dir data/cv_samples/ \
        --jd-file data/processed/jds.json \
        --output data/labeled/annotation_pairs.csv \
        --n-pairs 80 \
        --jds-per-cv 5
"""
import argparse
import csv
import json
import random
from pathlib import Path


def load_cvs(cv_dir):
    """Load CV metadata (id + parsed skills nếu có)."""
    cv_dir = Path(cv_dir)
    cvs = []
    # Hỗ trợ cả JSON và thư mục chứa file riêng lẻ
    if (cv_dir / "cvs.json").exists():
        with open(cv_dir / "cvs.json", encoding="utf-8") as f:
            cvs = json.load(f)
    else:
        for fp in sorted(cv_dir.glob("*.json")):
            with open(fp, encoding="utf-8") as f:
                cv = json.load(f)
            if "id" not in cv:
                cv["id"] = fp.stem
            cvs.append(cv)
    return cvs


def load_jds(jd_file):
    """Load JDs."""
    with open(jd_file, encoding="utf-8") as f:
        jds = json.load(f)
    # Gán index-based ID nếu chưa có
    for i, jd in enumerate(jds):
        if "id" not in jd:
            jd["id"] = f"jd_{i:04d}"
        else:
            jd["id"] = str(jd.get("metadata", {}).get("source_id", f"jd_{i:04d}"))
    return jds


def classify_difficulty(cv, jd):
    """
    Heuristic phân loại mức khó dựa trên overlap industry_group.
    - Easy: cùng industry_group → likely match hoặc clearly not match
    - Hard: khác industry_group nhưng có overlap kỹ năng
    - Medium: else
    """
    # Placeholder — sẽ cải tiến khi có parsed skills
    cv_group = cv.get("industry_group", cv.get("target_industry", ""))
    jd_group = jd.get("industry_group", "")

    if cv_group and jd_group:
        if cv_group.lower() == jd_group.lower():
            return "easy"
        elif any(kw in jd_group.lower() for kw in ["data", "ai", "ml"]):
            return "hard"
    return "medium"


def generate_pairs(cvs, jds, n_pairs=80, jds_per_cv=5, seed=42):
    """
    Ghép cặp CV × JD phân tầng.
    Đảm bảo:
    - Mỗi CV ghép với jds_per_cv JD
    - Mix industry_group
    - Đủ 3 mức khó
    """
    random.seed(seed)

    # Group JDs by industry_group
    jds_by_group = {}
    for jd in jds:
        group = jd.get("industry_group", "Unknown")
        if group not in jds_by_group:
            jds_by_group[group] = []
        jds_by_group[group].append(jd)

    groups = list(jds_by_group.keys())
    pairs = []

    for cv in cvs:
        # Chọn JD từ nhiều nhóm khác nhau
        selected_jds = []

        # 2 JD cùng nhóm (nếu có) → easy
        cv_group = cv.get("industry_group", cv.get("target_industry", groups[0]))
        same_group = jds_by_group.get(cv_group, [])
        if same_group:
            selected_jds.extend(random.sample(same_group, min(2, len(same_group))))

        # 3 JD từ nhóm khác → medium/hard
        other_groups = [g for g in groups if g != cv_group]
        for g in random.sample(other_groups, min(3, len(other_groups))):
            candidates = jds_by_group[g]
            selected_jds.append(random.choice(candidates))

        # Cắt đúng jds_per_cv
        selected_jds = selected_jds[:jds_per_cv]

        for jd in selected_jds:
            difficulty = classify_difficulty(cv, jd)
            pairs.append({
                "cv_id": cv.get("id", "unknown"),
                "jd_id": jd["id"],
                "difficulty_hint": difficulty,
                "cv_industry": cv.get("industry_group",
                                       cv.get("target_industry", "")),
                "jd_industry": jd.get("industry_group", ""),
            })

        if len(pairs) >= n_pairs:
            break

    return pairs[:n_pairs]


def main():
    parser = argparse.ArgumentParser(description="Generate annotation pairs for D3")
    parser.add_argument("--cv-dir", default="data/cv_samples/",
                        help="Directory containing CV JSON files")
    parser.add_argument("--jd-file", default="data/processed/jds.json",
                        help="JD JSON file")
    parser.add_argument("--output", default="data/labeled/annotation_pairs.csv",
                        help="Output CSV file")
    parser.add_argument("--n-pairs", type=int, default=80,
                        help="Number of pairs to generate")
    parser.add_argument("--jds-per-cv", type=int, default=5,
                        help="JDs per CV")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cv_dir = Path(args.cv_dir)
    if not cv_dir.exists():
        print(f"⚠️  CV directory '{cv_dir}' chưa tồn tại.")
        print("   Tạo thư mục và thêm CV JSON files trước khi chạy script này.")
        print(f"   mkdir -p {cv_dir}")
        cv_dir.mkdir(parents=True, exist_ok=True)
        # Tạo file README
        readme = cv_dir / "README.md"
        readme.write_text(
            "# CV đã parse\n\n"
            "Đặt file CV đã parse (JSON) vào đây.\n"
            "Mỗi file cần có ít nhất: `id`, `skills`, `experience_years`, "
            "`education`, `target_industry`.\n",
            encoding="utf-8",
        )
        print(f"   Đã tạo {readme}")
        return

    cvs = load_cvs(cv_dir)
    if not cvs:
        print(f"⚠️  Không tìm thấy CV trong '{cv_dir}'. Thêm CV trước khi chạy.")
        return

    jds = load_jds(args.jd_file)
    print(f"✅ Đã load {len(cvs)} CV, {len(jds)} JD")

    pairs = generate_pairs(cvs, jds, args.n_pairs, args.jds_per_cv, args.seed)
    print(f"✅ Đã tạo {len(pairs)} cặp")

    # Thống kê mức khó
    from collections import Counter
    diff_counts = Counter(p["difficulty_hint"] for p in pairs)
    print(f"   Phân bố mức khó: {dict(diff_counts)}")

    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "cv_id", "jd_id", "difficulty_hint", "cv_industry", "jd_industry"
        ])
        writer.writeheader()
        writer.writerows(pairs)
    print(f"💾 Đã lưu tại: {output_path}")

    # Tạo 3 file annotation riêng cho 3 người
    for person in ["A", "B", "C"]:
        ann_path = output_path.parent / f"annotations_{person}.csv"
        if not ann_path.exists():
            with open(ann_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["cv_id", "jd_id", "score", "reason", "annotator"])
                for p in pairs:
                    writer.writerow([p["cv_id"], p["jd_id"], "", "", person])
            print(f"📝 Tạo file chấm: {ann_path}")

    print("\n✅ Hạ tầng gán nhãn D3 sẵn sàng!")
    print("   Bước tiếp: khi C có đủ CV → chạy lại script này → phát file cho 3 người chấm.")


if __name__ == "__main__":
    main()
