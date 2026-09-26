"""
Bước 3-4: Lọc JD ngành IT thuần từ dataset HuggingFace,
lấy mẫu 300-500 JD đa dạng, map sang schema nội bộ.

Usage:
    python scripts/filter_and_sample_jds.py
"""
import json
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

from datasets import load_dataset


# --- Bước 3a: Định nghĩa nhóm ngành IT thuần ---
# Phương án A: chỉ lấy nhóm IT/CNTT thuần túy
IT_EXACT_INDUSTRIES = {
    "IT Phần mềm",
    "IT phần mềm",
    "IT Phần cứng - Mạng",
    "IT phần cứng/mạng",
    "CNTT - Phần mềm",
    "CNTT - Phần mềm , CNTT - Phần cứng / Mạng",
    "IT Phần cứng - Mạng / IT Phần mềm",
    "IT Phần mềm / IT Phần cứng - Mạng",
    "Công nghệ thông tin",
}

IT_KEYWORDS_IN_INDUSTRY = [
    "Công nghệ thông tin,",  # catches all "Công nghệ thông tin, ..." compound values
    "Công nghệ Thông tin,",
]


def is_it_industry(val):
    """Check if a job_industry value belongs to IT/CNTT group (Phương án A)."""
    if not val:
        return False
    if val in IT_EXACT_INDUSTRIES:
        return True
    return any(kw in val for kw in IT_KEYWORDS_IN_INDUSTRY)


def normalize_text(text):
    """Normalize text for near-duplicate detection."""
    if not text:
        return ""
    # Lowercase, strip extra whitespace, remove special chars
    t = text.lower().strip()
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[^\w\s]', '', t)
    return t


def text_fingerprint(text, n=3):
    """Create a fingerprint from text for near-duplicate detection using n-gram hashing."""
    normalized = normalize_text(text)
    if len(normalized) < 50:
        return hashlib.md5(normalized.encode()).hexdigest()
    # Use first 200 + last 200 chars as fingerprint base
    chunk = normalized[:200] + normalized[-200:]
    return hashlib.md5(chunk.encode()).hexdigest()


def main():
    print("=" * 70)
    print("Bước 3: Lọc JD ngành IT thuần từ dataset HuggingFace")
    print("=" * 70)

    # Load dataset
    print("\n⏳ Đang tải dataset...")
    ds = load_dataset("tinixai/vietnamese-job-descriptions", split="train")
    print(f"✅ Đã tải: {len(ds):,} dòng")

    # --- Filter IT-only ---
    print("\n🔍 Lọc JD ngành IT thuần (Phương án A)...")
    it_indices = []
    for i in range(len(ds)):
        if is_it_industry(ds[i]["job_industry"]):
            it_indices.append(i)

    print(f"✅ Tìm thấy {len(it_indices):,} JD ngành IT thuần")

    # Collect IT JDs
    it_jds = [ds[i] for i in it_indices]

    # --- Stats before filtering ---
    print("\n📊 Phân bố trước khi lọc trùng lặp:")
    industry_counts = Counter(jd["job_industry"] for jd in it_jds)
    print(f"  - Số giá trị job_industry: {len(industry_counts)}")
    company_counts = Counter(jd["company_name"] for jd in it_jds)
    print(f"  - Số công ty: {len(company_counts)}")

    exp_counts = Counter(jd["experience_level"] for jd in it_jds)
    print(f"  - Số giá trị experience_level: {len(exp_counts)}")
    print("    Top 5:")
    for val, cnt in exp_counts.most_common(5):
        print(f"      {val}: {cnt}")

    # --- Remove near-duplicates ---
    print("\n🧹 Loại bỏ JD trùng lặp gần giống (cùng công ty, nội dung gần giống)...")
    seen_fingerprints = {}  # fingerprint -> index
    unique_jds = []
    duplicate_count = 0

    for jd in it_jds:
        company = normalize_text(jd.get("company_name", ""))
        desc = jd.get("job_description", "") or ""
        req = jd.get("requirements", "") or ""
        content = desc + " " + req

        # Fingerprint = company + content hash
        fp = company + "|" + text_fingerprint(content)
        if fp not in seen_fingerprints:
            seen_fingerprints[fp] = len(unique_jds)
            unique_jds.append(jd)
        else:
            duplicate_count += 1

    print(f"  - Removed {duplicate_count:,} near-duplicates")
    print(f"  - Remaining: {len(unique_jds):,} unique JDs")

    # --- Remove JDs with empty critical fields ---
    print("\n🧹 Loại bỏ JD thiếu nội dung chính...")
    valid_jds = []
    for jd in unique_jds:
        title = (jd.get("job_title") or "").strip()
        desc = (jd.get("job_description") or "").strip()
        req = (jd.get("requirements") or "").strip()
        if title and (desc or req) and len(desc + req) >= 100:
            valid_jds.append(jd)

    print(f"  - Removed {len(unique_jds) - len(valid_jds):,} JDs with missing/short content")
    print(f"  - Remaining: {len(valid_jds):,} valid JDs")

    # --- Stratified sampling: 400 JDs ---
    TARGET = 400
    print(f"\n🎯 Lấy mẫu phân tầng {TARGET} JD (đa dạng company, level, industry)...")

    # Normalize experience_level into categories
    def categorize_experience(exp):
        if not exp:
            return "Không rõ"
        exp_lower = exp.lower().strip()
        if any(k in exp_lower for k in ["không", "0 ", "dưới 1", "< 1", "thực tập",
                                          "mới tốt nghiệp", "fresher"]):
            return "Entry (0-1 năm)"
        if any(k in exp_lower for k in ["1 năm", "1 -", "1-", "0,5", "lên đến 1"]):
            if "10" not in exp_lower and "1 - 2" not in exp_lower and "1 - 3" not in exp_lower:
                return "Entry (0-1 năm)"
        if any(k in exp_lower for k in ["1 - 2", "1 - 3", "1-2", "1-3", "2 năm",
                                          "2 -", "2-", "từ 1", "trên 1"]):
            return "Junior (1-3 năm)"
        if any(k in exp_lower for k in ["3 năm", "3 -", "3-", "2 - 5", "từ 2", "trên 2",
                                          "4 năm", "4 -"]):
            return "Mid (3-5 năm)"
        if any(k in exp_lower for k in ["5 năm", "5 -", "5-", "trên 3", "trên 5",
                                          "6", "7", "8", "9", "10", "hơn 5"]):
            return "Senior (5+ năm)"
        return "Không rõ"

    # Group by (company, experience_category)
    groups = defaultdict(list)
    for jd in valid_jds:
        company = (jd.get("company_name") or "Unknown").strip()
        exp_cat = categorize_experience(jd.get("experience_level"))
        groups[(company, exp_cat)].append(jd)

    # Round-robin sampling: take 1 from each group, repeat until TARGET
    sampled = []
    sampled_ids = set()
    group_keys = list(groups.keys())

    # Shuffle groups for randomness (deterministic seed)
    import random
    random.seed(42)
    random.shuffle(group_keys)

    round_num = 0
    while len(sampled) < TARGET:
        added_this_round = 0
        for key in group_keys:
            if len(sampled) >= TARGET:
                break
            candidates = groups[key]
            if round_num < len(candidates):
                jd = candidates[round_num]
                jd_id = jd.get("id", id(jd))
                if jd_id not in sampled_ids:
                    sampled.append(jd)
                    sampled_ids.add(jd_id)
                    added_this_round += 1
        round_num += 1
        if added_this_round == 0:
            break  # No more candidates

    print(f"✅ Đã lấy mẫu: {len(sampled)} JD")

    # --- Stats of sample ---
    print("\n📊 Phân bố mẫu:")
    sample_companies = Counter(jd["company_name"] for jd in sampled)
    print(f"  - Số công ty: {len(sample_companies)}")
    print(f"  - Max JD/công ty: {max(sample_companies.values())}")

    sample_exp = Counter(categorize_experience(jd["experience_level"]) for jd in sampled)
    print("  - Experience distribution:")
    for cat, cnt in sorted(sample_exp.items()):
        print(f"      {cat}: {cnt} ({cnt*100//len(sampled)}%)")

    sample_industry_groups = Counter()
    for jd in sampled:
        ind = jd.get("job_industry", "")
        if "Software Engineering" in ind:
            sample_industry_groups["Software Engineering"] += 1
        elif "Software Testing" in ind:
            sample_industry_groups["Software Testing/QA"] += 1
        elif "Data Science" in ind or "Data" in ind:
            sample_industry_groups["Data Science/Engineering"] += 1
        elif "AI" in ind or "Artificial" in ind or "Machine" in ind:
            sample_industry_groups["AI/ML"] += 1
        elif "Infrastructure" in ind or "DevOps" in ind or "System" in ind:
            sample_industry_groups["Infrastructure/DevOps"] += 1
        elif "Product Management" in ind or "Project" in ind:
            sample_industry_groups["Product/Project Management"] += 1
        elif "IT Phần mềm" in ind or "IT phần mềm" in ind or "CNTT" in ind:
            sample_industry_groups["IT Phần mềm (general)"] += 1
        elif "Security" in ind or "Information Security" in ind:
            sample_industry_groups["Security"] += 1
        elif "Game" in ind:
            sample_industry_groups["Game Development"] += 1
        else:
            sample_industry_groups["Other IT"] += 1
    print("  - Industry groups:")
    for grp, cnt in sorted(sample_industry_groups.items(), key=lambda x: -x[1]):
        print(f"      {grp}: {cnt}")

    # --- Bước 4: Map sang schema nội bộ ---
    print("\n" + "=" * 70)
    print("Bước 4: Map sang schema JD nội bộ")
    print("=" * 70)

    output_jds = []
    for jd in sampled:
        mapped = {
            # Core fields (schema nội bộ)
            "title": jd.get("job_title", ""),
            "requirements": jd.get("requirements", ""),
            "responsibilities": jd.get("job_description", ""),
            "level": jd.get("experience_level", ""),
            "location": jd.get("location", ""),
            # Metadata phụ
            "metadata": {
                "company_name": jd.get("company_name", ""),
                "salary": jd.get("salary", ""),
                "benefits": jd.get("benefits", ""),
                "job_type": jd.get("job_type", ""),
                "education_level": jd.get("education_level", ""),
                "job_position": jd.get("job_position", ""),
                "job_industry": jd.get("job_industry", ""),
                "year": jd.get("year"),
                "source_dataset": "tinixai/vietnamese-job-descriptions",
                "source_id": jd.get("id"),
            },
        }
        output_jds.append(mapped)

    # Save
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "jds.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_jds, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Đã lưu {len(output_jds)} JD tại: {output_path}")

    # Also save raw filtered set for reference
    raw_output_path = Path("data/raw") / "hf_it_jds_filtered.json"
    raw_data = []
    for jd in sampled:
        raw_data.append({k: v for k, v in jd.items()})
    with open(raw_output_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu raw filtered tại: {raw_output_path}")

    # Show sample
    print("\n--- Mẫu 3 JD đầu tiên (đã map schema) ---")
    for i, jd in enumerate(output_jds[:3]):
        print(f"\n[{i}] title: {jd['title']}")
        print(f"    level: {jd['level']}")
        print(f"    location: {jd['location'][:80]}...")
        print(f"    company: {jd['metadata']['company_name']}")
        print(f"    industry: {jd['metadata']['job_industry'][:60]}...")
        print(f"    requirements (100 chars): {(jd['requirements'] or '')[:100]}...")
        print(f"    responsibilities (100 chars): {(jd['responsibilities'] or '')[:100]}...")

    print("\n✅ Hoàn tất bước 3-4!")


if __name__ == "__main__":
    main()
