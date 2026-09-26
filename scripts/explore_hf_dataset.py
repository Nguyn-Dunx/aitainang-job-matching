"""
Bước 1-2: Tải dataset tinixai/vietnamese-job-descriptions từ HuggingFace
và liệt kê giá trị duy nhất của job_industry, job_position để chọn nhóm ngành.

Usage:
    python scripts/explore_hf_dataset.py
"""
import json
from collections import Counter
from pathlib import Path

from datasets import load_dataset


def main():
    print("=" * 70)
    print("Bước 1: Tải dataset tinixai/vietnamese-job-descriptions từ HuggingFace")
    print("=" * 70)

    # Load dataset — streaming=False to download fully
    print("\n⏳ Đang tải dataset (607k dòng, có thể mất vài phút lần đầu)...\n")
    ds = load_dataset("tinixai/vietnamese-job-descriptions", split="train")
    print(f"✅ Đã tải xong: {len(ds):,} dòng")
    print(f"   Các cột: {ds.column_names}")

    # Show a few sample rows
    print("\n--- Mẫu 3 dòng đầu ---")
    for i in range(min(3, len(ds))):
        row = ds[i]
        print(f"\n[{i}] job_title: {row.get('job_title', 'N/A')}")
        print(f"    job_industry: {row.get('job_industry', 'N/A')}")
        print(f"    job_position: {row.get('job_position', 'N/A')}")
        print(f"    experience_level: {row.get('experience_level', 'N/A')}")
        print(f"    location: {row.get('location', 'N/A')}")
        desc = str(row.get('job_description', ''))[:200]
        print(f"    job_description (200 ký tự đầu): {desc}...")

    # ---- Bước 2: Liệt kê unique values ----
    print("\n" + "=" * 70)
    print("Bước 2: Liệt kê giá trị duy nhất của job_industry và job_position")
    print("=" * 70)

    # job_industry
    industry_counter = Counter(ds["job_industry"])
    print(f"\n📊 job_industry — {len(industry_counter)} giá trị duy nhất:")
    print("-" * 50)
    for idx, (val, count) in enumerate(industry_counter.most_common(), 1):
        print(f"  {idx:3d}. [{count:>6,} JD] {val}")

    # job_position
    position_counter = Counter(ds["job_position"])
    print(f"\n📊 job_position — {len(position_counter)} giá trị duy nhất:")
    print("-" * 50)
    for idx, (val, count) in enumerate(position_counter.most_common(), 1):
        print(f"  {idx:3d}. [{count:>6,} JD] {val}")

    # Save to JSON for reference
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "dataset_name": "tinixai/vietnamese-job-descriptions",
        "total_rows": len(ds),
        "columns": ds.column_names,
        "job_industry_unique": [
            {"value": val, "count": count}
            for val, count in industry_counter.most_common()
        ],
        "job_position_unique": [
            {"value": val, "count": count}
            for val, count in position_counter.most_common()
        ],
    }

    out_path = output_dir / "hf_dataset_exploration.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Đã lưu summary tại: {out_path}")

    # Also show experience_level and location for context
    print("\n" + "=" * 70)
    print("Thông tin bổ sung: experience_level và location")
    print("=" * 70)

    level_counter = Counter(ds["experience_level"])
    print(f"\n📊 experience_level — {len(level_counter)} giá trị:")
    for idx, (val, count) in enumerate(level_counter.most_common(), 1):
        print(f"  {idx:3d}. [{count:>6,} JD] {val}")

    location_counter = Counter(ds["location"])
    print(f"\n📊 location — {len(location_counter)} giá trị (top 20):")
    for idx, (val, count) in enumerate(location_counter.most_common(20), 1):
        print(f"  {idx:3d}. [{count:>6,} JD] {val}")

    print("\n✅ Hoàn tất bước 1-2. Hãy xem kết quả trên để chọn nhóm ngành phù hợp.")


if __name__ == "__main__":
    main()
