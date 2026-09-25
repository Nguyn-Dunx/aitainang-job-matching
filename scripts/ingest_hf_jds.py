#!/usr/bin/env python3
"""
ingest_hf_jds.py — Tải dataset tinixai/vietnamese-job-descriptions từ HuggingFace,
lọc ngành CNTT/Data, chuyển đổi sang schema dự án, lưu JSON.

Cách dùng:
    python scripts/ingest_hf_jds.py                        # Tải & lọc CNTT/Data
    python scripts/ingest_hf_jds.py --all-industries       # Giữ tất cả ngành (debug)
    python scripts/ingest_hf_jds.py --max-records 500      # Giới hạn số JD
    python scripts/ingest_hf_jds.py --stats-only           # Chỉ in thống kê, không lưu

Schema đầu ra (mỗi JD):
{
    "id": "JD-0001",
    "title": "...",
    "company": "...",
    "requirements": ["..."],
    "responsibilities": ["..."],
    "level": "...",
    "location": "...",
    "salary": "...",
    "posted_date": null,
    "source_url": "https://huggingface.co/datasets/tinixai/vietnamese-job-descriptions",
    "source_dataset": "tinixai/vietnamese-job-descriptions",
    "source_id": 12345,                    # ID gốc trong dataset HF
    "collected_date": "2026-09-25",
    "job_type": "...",
    "job_industry": "...",
    "education_level": "...",
    "job_position": "...",
    "benefits": "...",
    "year": 2024,
    "raw_text": "...",                     # Ghép toàn bộ nội dung gốc để audit
    "needs_review": false,
    "review_notes": []
}
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATASET_NAME = "tinixai/vietnamese-job-descriptions"
DATASET_URL = f"https://huggingface.co/datasets/{DATASET_NAME}"
DATASET_LICENSE = "CC-BY-NC-4.0"

# Keywords to filter IT/Data industries (case-insensitive, partial match)
IT_DATA_INDUSTRY_KEYWORDS = [
    # English
    "it", "information technology", "software", "computer",
    "data", "technology", "tech", "digital",
    "internet", "telecom", "telecommunication",
    "ai", "artificial intelligence", "machine learning",
    "cybersecurity", "security", "cloud",
    "e-commerce", "ecommerce", "fintech",
    "game", "gaming",
    # Vietnamese
    "công nghệ thông tin", "phần mềm", "công nghệ",
    "dữ liệu", "viễn thông", "tin học",
    "thương mại điện tử", "kỹ thuật số",
    "trí tuệ nhân tạo", "máy tính",
    "điện tử", "lập trình",
]

# Keywords to match IT/Data job titles (fallback when industry is vague)
IT_DATA_TITLE_KEYWORDS = [
    "developer", "engineer", "lập trình", "programmer",
    "data", "analyst", "devops", "sre",
    "qa", "tester", "testing",
    "frontend", "backend", "fullstack", "full-stack", "full stack",
    "mobile", "ios", "android",
    "cloud", "aws", "azure", "gcp",
    "ai", "ml", "machine learning", "deep learning",
    "security", "infra", "infrastructure",
    "dba", "database", "admin", "sysadmin", "system",
    "product manager", "scrum", "agile", "project manager",
    "ui/ux", "ux", "designer",  # tech designer
    "blockchain", "web3",
    "network", "mạng",
    "it ", "cntt", "phần mềm",
    "business analyst", "ba ",
    "solution architect", "technical",
    "helpdesk", "support",
]

# Level mapping from HF dataset's experience_level to our schema
LEVEL_MAP = {
    "intern": "intern",
    "thực tập": "intern",
    "internship": "intern",
    "fresher": "fresher",
    "fresh": "fresher",
    "mới ra trường": "fresher",
    "junior": "junior",
    "nhân viên": "junior",
    "mid": "mid",
    "middle": "mid",
    "senior": "senior",
    "trưởng nhóm": "lead",
    "lead": "lead",
    "leader": "lead",
    "manager": "lead",
    "quản lý": "lead",
    "director": "lead",
    "giám đốc": "lead",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def is_it_data_industry(industry: str | None) -> bool:
    """Check if industry string matches IT/Data domain."""
    if not industry:
        return False
    industry_lower = industry.lower().strip()
    return any(kw in industry_lower for kw in IT_DATA_INDUSTRY_KEYWORDS)


def is_it_data_title(title: str | None) -> bool:
    """Check if job title matches IT/Data domain."""
    if not title:
        return False
    title_lower = title.lower().strip()
    return any(kw in title_lower for kw in IT_DATA_TITLE_KEYWORDS)


def parse_list_from_text(text: str | None) -> list[str]:
    """Parse a text block (possibly with bullets/newlines) into a list of items."""
    if not text or not text.strip():
        return []

    lines = text.strip().split("\n")
    items = []
    for line in lines:
        # Remove bullet / numbering prefix
        cleaned = re.sub(r"^\s*[-•●*·▪►]\s*", "", line)
        cleaned = re.sub(r"^\s*\d+[.)]\s*", "", cleaned)
        cleaned = cleaned.strip()
        # Remove trailing semicolons/periods
        cleaned = cleaned.rstrip(";").strip()
        if cleaned and len(cleaned) > 3:
            items.append(cleaned)
    return items


def map_level(experience_level: str | None, title: str | None) -> str | None:
    """Map experience_level from HF dataset to our level schema."""
    # Try from explicit experience_level field
    if experience_level:
        exp_lower = experience_level.lower().strip()
        for keyword, level in LEVEL_MAP.items():
            if keyword in exp_lower:
                return level

    # Fallback: detect from title
    if title:
        title_lower = title.lower()
        # Check in priority order
        for level_check in ["lead", "senior", "mid", "junior", "fresher", "intern"]:
            for keyword, mapped_level in LEVEL_MAP.items():
                if mapped_level == level_check and keyword in title_lower:
                    return level_check
    return None


def build_raw_text(row: dict) -> str:
    """Reconstruct raw text from HF dataset row for audit trail."""
    parts = []
    if row.get("job_title"):
        parts.append(f"Title: {row['job_title']}")
    if row.get("company_name"):
        parts.append(f"Company: {row['company_name']}")
    if row.get("location"):
        parts.append(f"Location: {row['location']}")
    if row.get("salary"):
        parts.append(f"Salary: {row['salary']}")
    if row.get("job_industry"):
        parts.append(f"Industry: {row['job_industry']}")
    if row.get("experience_level"):
        parts.append(f"Experience: {row['experience_level']}")
    if row.get("education_level"):
        parts.append(f"Education: {row['education_level']}")
    if row.get("job_description"):
        parts.append(f"\nJob Description:\n{row['job_description']}")
    if row.get("requirements"):
        parts.append(f"\nRequirements:\n{row['requirements']}")
    if row.get("benefits"):
        parts.append(f"\nBenefits:\n{row['benefits']}")
    return "\n".join(parts)


def convert_row(row: dict, jd_id: str, collected_date: str) -> dict:
    """Convert one HF dataset row to our project's JD schema."""
    review_notes = []

    title = row.get("job_title") or None
    if not title:
        review_notes.append("Thiếu title")

    requirements = parse_list_from_text(row.get("requirements"))
    if not requirements:
        review_notes.append("Thiếu requirements")

    # job_description in this dataset = responsibilities
    responsibilities = parse_list_from_text(row.get("job_description"))
    if not responsibilities:
        review_notes.append("Thiếu responsibilities/job_description")

    level = map_level(row.get("experience_level"), title)

    return {
        "id": jd_id,
        "title": title,
        "company": row.get("company_name") or None,
        "requirements": requirements,
        "responsibilities": responsibilities,
        "level": level,
        "location": row.get("location") or None,
        "salary": row.get("salary") or None,
        "posted_date": None,
        "source_url": DATASET_URL,
        "source_dataset": DATASET_NAME,
        "source_id": row.get("id"),
        "collected_date": collected_date,
        "job_type": row.get("job_type") or None,
        "job_industry": row.get("job_industry") or None,
        "education_level": row.get("education_level") or None,
        "job_position": row.get("job_position") or None,
        "benefits": row.get("benefits") or None,
        "year": row.get("year"),
        "raw_text": build_raw_text(row),
        "needs_review": len(review_notes) > 0,
        "review_notes": review_notes,
    }


def print_stats(dataset, filtered_rows: list, all_industries: bool):
    """Print statistics about the dataset and filtering."""
    print(f"\n{'='*60}")
    print(f"📊 Thống kê dataset: {DATASET_NAME}")
    print(f"{'='*60}")
    print(f"  Tổng records trong dataset  : {len(dataset):,}")
    print(f"  Records sau khi lọc CNTT/Data: {len(filtered_rows):,}")
    if not all_industries:
        print(f"  Tỉ lệ lọc                 : {len(filtered_rows)/len(dataset)*100:.1f}%")

    # Industry distribution (in filtered set)
    industries = Counter(
        row.get("job_industry", "N/A") for row in filtered_rows
    )
    print(f"\n  Top ngành nghề (sau lọc):")
    for ind, count in industries.most_common(15):
        print(f"    {ind:40s} : {count:,}")

    # Level distribution
    levels = Counter(
        row.get("experience_level", "N/A") for row in filtered_rows
    )
    print(f"\n  Phân bố experience_level:")
    for lv, count in levels.most_common(10):
        print(f"    {lv:30s} : {count:,}")

    # Location distribution
    locations = Counter(
        row.get("location", "N/A") for row in filtered_rows
    )
    print(f"\n  Top địa điểm:")
    for loc, count in locations.most_common(10):
        print(f"    {loc:40s} : {count:,}")

    # Year distribution
    years = Counter(row.get("year", "N/A") for row in filtered_rows)
    print(f"\n  Phân bố năm:")
    for yr, count in sorted(years.items()):
        print(f"    {yr} : {count:,}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description=f"Tải & lọc {DATASET_NAME} cho dự án AI Job Matching.",
        epilog="Ví dụ: python scripts/ingest_hf_jds.py --max-records 500",
    )
    parser.add_argument(
        "-o", "--output",
        default="data/processed/jds.json",
        help="Output JSON file (default: data/processed/jds.json)",
    )
    parser.add_argument(
        "--all-industries",
        action="store_true",
        help="Không lọc ngành — giữ tất cả industries (debug)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Giới hạn số JD tối đa trong output",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Chỉ in thống kê, không lưu file",
    )
    parser.add_argument(
        "-d", "--date",
        default=str(date.today()),
        help="Ngày thu thập (YYYY-MM-DD), mặc định = hôm nay",
    )

    args = parser.parse_args()

    # --- Load from HuggingFace ---
    print(f"⏳ Đang tải dataset {DATASET_NAME} từ HuggingFace...")
    try:
        from datasets import load_dataset
    except ImportError:
        print("❌ Cần cài thư viện: pip install datasets", file=sys.stderr)
        sys.exit(1)

    ds = load_dataset(DATASET_NAME, split="train")
    print(f"✅ Đã tải {len(ds):,} records")

    # --- Filter IT/Data ---
    if args.all_industries:
        filtered_rows = list(ds)
        print(f"⚠️  Giữ tất cả ngành: {len(filtered_rows):,} records")
    else:
        print("🔍 Đang lọc ngành CNTT/Data...")
        filtered_rows = []
        for row in ds:
            if is_it_data_industry(row.get("job_industry")) or \
               is_it_data_title(row.get("job_title")):
                filtered_rows.append(row)
        print(f"✅ Lọc được {len(filtered_rows):,} JD ngành CNTT/Data")

    # --- Stats ---
    print_stats(ds, filtered_rows, args.all_industries)

    if args.stats_only:
        print("📌 --stats-only: không lưu file.")
        return

    # --- Limit records ---
    if args.max_records and len(filtered_rows) > args.max_records:
        print(f"✂️  Giới hạn {args.max_records} records (từ {len(filtered_rows):,})")
        filtered_rows = filtered_rows[:args.max_records]

    # --- Convert to project schema ---
    print("🔄 Chuyển đổi sang schema dự án...")
    jds = []
    review_count = 0
    for i, row in enumerate(filtered_rows):
        jd_id = f"JD-{i+1:04d}"
        converted = convert_row(row, jd_id, args.date)
        jds.append(converted)
        if converted["needs_review"]:
            review_count += 1

    # --- Save ---
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(jds, f, ensure_ascii=False, indent=2)

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"📋 Kết quả")
    print(f"{'='*60}")
    print(f"  Tổng JD đã lưu  : {len(jds):,}")
    print(f"  Cần review       : {review_count:,}")
    print(f"  File output      : {output_path}")
    print(f"  Dataset source   : {DATASET_NAME}")
    print(f"  License          : {DATASET_LICENSE}")
    print()

    # Sample first 3
    print("📝 Mẫu 3 JD đầu tiên:")
    for jd in jds[:3]:
        print(f"  {jd['id']} | {jd.get('title', '???')[:60]:60s} | "
              f"level={jd.get('level', '?'):8s} | "
              f"req={len(jd['requirements'])} items | "
              f"{'⚠️  REVIEW' if jd['needs_review'] else '✅ OK'}")


if __name__ == "__main__":
    main()
