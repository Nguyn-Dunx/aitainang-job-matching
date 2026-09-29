#!/usr/bin/env python3
"""
parse_raw_jds.py — Chuẩn hóa JD thô (copy-paste) thành JSON theo schema dự án.

Cách dùng:
    python scripts/parse_raw_jds.py data/raw/jd_batch_20260925.txt

File đầu vào: file .txt chứa nhiều JD, phân tách bằng dòng '===' (ít nhất 3 dấu =).
File đầu ra : data/processed/jds.json (append, không ghi đè JD cũ).

Schema mỗi JD:
{
    "id": "JD-0001",
    "title": "...",
    "company": "...",           # optional, có thể để null
    "requirements": ["..."],    # list các yêu cầu
    "responsibilities": ["..."],# list trách nhiệm
    "level": "...",             # junior | mid | senior | lead | intern | null
    "location": "...",
    "salary": "...",            # raw string, null nếu không có
    "posted_date": "...",       # YYYY-MM-DD hoặc raw string
    "source_url": "...",        # URL gốc hoặc mô tả nguồn
    "collected_date": "...",    # ngày thu thập (auto = hôm nay)
    "raw_text": "...",          # giữ nguyên bản gốc để audit
    "needs_review": false,      # true nếu thiếu trường quan trọng
    "review_notes": []          # ghi chú trường nào thiếu
}
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SEPARATOR_PATTERN = re.compile(r"^={3,}\s*$", re.MULTILINE)

LEVEL_KEYWORDS = {
    "intern": ["intern", "thực tập", "internship"],
    "fresher": ["fresher", "fresh graduate", "mới ra trường", "fresh grad"],
    "junior": ["junior", "jr", "1-2 năm", "1-3 năm", "dưới 2 năm"],
    "mid": ["mid", "middle", "2-4 năm", "3-5 năm", "2-5 năm"],
    "senior": ["senior", "sr", "5+ năm", "trên 5 năm", "4-6 năm", "5-7 năm"],
    "lead": ["lead", "leader", "trưởng nhóm", "team lead", "tech lead", "manager"],
}

# ---------------------------------------------------------------------------
# Section header patterns — used to split JD text into sections
# ---------------------------------------------------------------------------
# Each tuple: (section_key, compiled regex matching a section header line)
SECTION_HEADER_PATTERNS = [
    (
        "requirements",
        re.compile(
            r"^\s*(?:yêu\s*cầu|requirements?|qualifications?|kỹ\s*năng\s*(?:yêu\s*cầu)?|"
            r"skills?\s*(?:required)?|điều\s*kiện)\s*[:\-–]?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "responsibilities",
        re.compile(
            r"^\s*(?:mô\s*tả\s*(?:công\s*việc)?|responsibilities|job\s*description|"
            r"nhiệm\s*vụ|công\s*việc\s*(?:chính)?)\s*[:\-–]?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "benefits",
        re.compile(
            r"^\s*(?:quyền\s*lợi|benefits?|phúc\s*lợi|chế\s*độ)\s*[:\-–]?\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "contact",
        re.compile(
            r"^\s*(?:liên\s*hệ|contact|cách\s*ứng\s*tuyển|hạn\s*nộp|deadline|"
            r"apply|ứng\s*tuyển)\s*[:\-–]?\s*$",
            re.IGNORECASE,
        ),
    ),
]

# Single-line metadata patterns (key: value on one line)
METADATA_PATTERNS = {
    "title": re.compile(
        r"^\s*(?:vị\s*trí|chức\s*danh|position|job\s*title|tuyển\s*dụng)\s*[:\-–]\s*(.+)",
        re.IGNORECASE,
    ),
    "location": re.compile(
        r"^\s*(?:địa\s*điểm|location|nơi\s*làm\s*việc|địa\s*chỉ)\s*[:\-–]\s*(.+)",
        re.IGNORECASE,
    ),
    "salary": re.compile(
        r"^\s*(?:mức\s*lương|lương|salary|thu\s*nhập|income)\s*[:\-–]\s*(.+)",
        re.IGNORECASE,
    ),
    "company": re.compile(
        r"^\s*(?:công\s*ty|company|nhà\s*tuyển\s*dụng|employer)\s*[:\-–]\s*(.+)",
        re.IGNORECASE,
    ),
    "posted_date": re.compile(
        r"^\s*(?:ngày\s*đăng|posted|date|thời\s*gian)\s*[:\-–]\s*(.+)",
        re.IGNORECASE,
    ),
    "source_url": re.compile(
        r"^\s*(?:nguồn|source|link|url)\s*[:\-–]\s*(https?://\S+|.+)",
        re.IGNORECASE,
    ),
}

# Fallback: grab the very first non-empty line as title if no explicit header
FIRST_LINE_TITLE = re.compile(r"^\s*(.{5,120})\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def split_jds(raw_text: str) -> list[str]:
    """Split raw text by === separator, return list of JD blocks."""
    blocks = SEPARATOR_PATTERN.split(raw_text)
    return [b.strip() for b in blocks if b.strip()]


def extract_list_items(text: str) -> list[str]:
    """Extract list items from a block of text (bulleted, numbered, or line-based)."""
    lines = text.strip().split("\n")
    items = []
    for line in lines:
        # Remove bullet / numbering prefix
        cleaned = re.sub(r"^\s*[-•●*]\s*", "", line)
        cleaned = re.sub(r"^\s*\d+[.)]\s*", "", cleaned)
        cleaned = cleaned.strip()
        if cleaned and len(cleaned) > 3:  # skip very short noise
            items.append(cleaned)
    return items


def detect_level(title: str | None, full_text: str) -> str | None:
    """Detect job level. Prioritize title match over body text to avoid
    false positives (e.g. 'Mentor junior developers' in a Senior JD)."""
    # Check title first (most reliable signal)
    if title:
        title_lower = title.lower()
        # Check in priority order: most specific first
        for level in ["lead", "senior", "mid", "junior", "fresher", "intern"]:
            for kw in LEVEL_KEYWORDS[level]:
                if kw in title_lower:
                    return level

    # Fallback: scan first few metadata lines (not bullet content)
    text_lower = full_text.lower()
    for level in ["lead", "senior", "mid", "junior", "fresher", "intern"]:
        for kw in LEVEL_KEYWORDS[level]:
            if kw in text_lower:
                return level
    return None


def split_into_sections(text: str) -> tuple[list[str], dict[str, str]]:
    """Split JD text into a header block (metadata lines before any section)
    and named sections (requirements, responsibilities, etc.).

    Returns:
        header_lines: lines before the first section header
        sections: dict mapping section_key -> section body text
    """
    lines = text.split("\n")
    header_lines = []
    sections: dict[str, str] = {}
    current_section = None
    current_lines: list[str] = []

    for line in lines:
        # Check if this line is a section header
        matched_section = None
        for key, pattern in SECTION_HEADER_PATTERNS:
            if pattern.match(line):
                matched_section = key
                break

        if matched_section:
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_lines)
            current_section = matched_section
            current_lines = []
        elif current_section:
            current_lines.append(line)
        else:
            header_lines.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_lines)

    return header_lines, sections


def parse_one_jd(raw_text: str, jd_id: str, collected_date: str) -> dict:
    """Parse a single JD block into structured JSON."""
    review_notes = []

    # --- Split into header + sections ---
    header_lines, sections = split_into_sections(raw_text)
    header_text = "\n".join(header_lines)

    # --- Extract metadata from header lines ---
    metadata: dict[str, str | None] = {}
    for key, pattern in METADATA_PATTERNS.items():
        for line in header_lines:
            m = pattern.match(line)
            if m:
                metadata[key] = m.group(1).strip()
                break

    # --- Title ---
    title = metadata.get("title")
    if not title:
        # Fallback: first non-empty line of the header
        for line in header_lines:
            stripped = line.strip()
            if stripped and len(stripped) >= 5:
                # Skip lines that look like metadata (key: value)
                is_meta = any(p.match(stripped) for p in METADATA_PATTERNS.values())
                if not is_meta:
                    title = stripped
                    break
        if not title:
            review_notes.append("Không tìm thấy title — cần bổ sung tay")

    # --- Requirements ---
    requirements = []
    if "requirements" in sections:
        requirements = extract_list_items(sections["requirements"])
    if not requirements:
        review_notes.append("Không trích được requirements — cần bổ sung tay")

    # --- Responsibilities ---
    responsibilities = []
    if "responsibilities" in sections:
        responsibilities = extract_list_items(sections["responsibilities"])
    if not responsibilities:
        review_notes.append("Không trích được responsibilities — cần bổ sung tay")

    # --- Level (prioritize title) ---
    level = detect_level(title, raw_text)
    if not level:
        review_notes.append("Không xác định được level — cần bổ sung tay")

    # --- Single-line fields ---
    location = metadata.get("location")
    salary = metadata.get("salary")
    company = metadata.get("company")
    posted_date = metadata.get("posted_date")
    source_url = metadata.get("source_url")

    if not source_url:
        review_notes.append("Thiếu source_url — cần bổ sung nguồn gốc JD")

    needs_review = len(review_notes) > 0

    return {
        "id": jd_id,
        "title": title,
        "company": company,
        "requirements": requirements if requirements else [],
        "responsibilities": responsibilities if responsibilities else [],
        "level": level,
        "location": location,
        "salary": salary,
        "posted_date": posted_date,
        "source_url": source_url,
        "collected_date": collected_date,
        "raw_text": raw_text,
        "needs_review": needs_review,
        "review_notes": review_notes,
    }


def load_existing_jds(output_path: Path) -> list[dict]:
    """Load existing JDs from output file if it exists."""
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_next_id(existing_jds: list[dict]) -> int:
    """Get the next JD ID number based on existing data."""
    if not existing_jds:
        return 1
    max_id = 0
    for jd in existing_jds:
        try:
            num = int(jd["id"].split("-")[1])
            max_id = max(max_id, num)
        except (IndexError, ValueError):
            pass
    return max_id + 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Parse raw JD text file into structured JSON.",
        epilog="Ví dụ: python scripts/parse_raw_jds.py data/raw/jd_batch_20260925.txt",
    )
    parser.add_argument(
        "input_file",
        help="Path to raw .txt file containing JDs separated by ===",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/processed/jds.json",
        help="Output JSON file (default: data/processed/jds.json)",
    )
    parser.add_argument(
        "-d",
        "--date",
        default=str(date.today()),
        help="Ngày thu thập (YYYY-MM-DD), mặc định = hôm nay",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ in ra stdout, không ghi file",
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Không tìm thấy file: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw_content = input_path.read_text(encoding="utf-8")
    jd_blocks = split_jds(raw_content)

    if not jd_blocks:
        print("⚠️  Không tìm thấy JD nào trong file. Kiểm tra dấu phân cách ===")
        sys.exit(0)

    # Load existing data
    output_path = Path(args.output)
    existing_jds = load_existing_jds(output_path)
    next_id = get_next_id(existing_jds)

    # Parse
    new_jds = []
    review_count = 0
    for i, block in enumerate(jd_blocks):
        jd_id = f"JD-{next_id + i:04d}"
        parsed = parse_one_jd(block, jd_id, args.date)
        new_jds.append(parsed)
        if parsed["needs_review"]:
            review_count += 1

    # Output
    if args.dry_run:
        print(json.dumps(new_jds, ensure_ascii=False, indent=2))
    else:
        # Merge with existing
        all_jds = existing_jds + new_jds
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_jds, f, ensure_ascii=False, indent=2)

    # Summary
    print(f"\n{'='*50}")
    print("📋 Tổng kết parse JD")
    print(f"{'='*50}")
    print(f"  File đầu vào : {input_path}")
    print(f"  Số JD mới    : {len(new_jds)}")
    print(f"  Cần review   : {review_count}")
    print(f"  Tổng JD (cũ + mới): {len(existing_jds) + len(new_jds)}")
    if not args.dry_run:
        print(f"  Đã ghi ra    : {output_path}")
    print()

    # Detail per JD
    for jd in new_jds:
        status = "⚠️  CẦN REVIEW" if jd["needs_review"] else "✅ OK"
        print(f"  {jd['id']} | {jd.get('title', '???')[:50]:50s} | {status}")
        if jd["review_notes"]:
            for note in jd["review_notes"]:
                print(f"         ↳ {note}")

    if review_count > 0:
        print(
            f"\n💡 Mở {output_path} để bổ sung {review_count} JD có cờ needs_review."
        )


if __name__ == "__main__":
    main()
