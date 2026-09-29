"""
Bước 2: Resample 450 JD với quota sàn cho Data/AI/ML (12-15%).
Lấy gần hết JD Data/AI có sẵn, phần còn lại phân tầng từ các nhóm khác.

Đồng thời:
- Bước 4a: Chuẩn hóa location → tỉnh/thành
- Bước 4b: Chuẩn hóa experience_level → 5 nhóm

Usage:
    python scripts/resample_with_quota.py
"""
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from datasets import load_dataset

# ========== Lọc IT (giữ nguyên logic cũ) ==========
IT_EXACT_INDUSTRIES = {
    "IT Phần mềm", "IT phần mềm", "IT Phần cứng - Mạng", "IT phần cứng/mạng",
    "CNTT - Phần mềm", "CNTT - Phần mềm , CNTT - Phần cứng / Mạng",
    "IT Phần cứng - Mạng / IT Phần mềm", "IT Phần mềm / IT Phần cứng - Mạng",
    "Công nghệ thông tin",
}
IT_KEYWORDS_IN_INDUSTRY = ["Công nghệ thông tin,", "Công nghệ Thông tin,"]


def is_it_industry(val):
    if not val:
        return False
    if val in IT_EXACT_INDUSTRIES:
        return True
    return any(kw in val for kw in IT_KEYWORDS_IN_INDUSTRY)


def normalize_text(text):
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[^\w\s]', '', t)
    return t


def text_fingerprint(text):
    normalized = normalize_text(text)
    if len(normalized) < 50:
        return hashlib.md5(normalized.encode()).hexdigest()
    chunk = normalized[:200] + normalized[-200:]
    return hashlib.md5(chunk.encode()).hexdigest()


# ========== Phân loại nhóm ngành ==========
DATA_AI_KEYWORDS = [
    "Data Science", "Data Analyst", "Data Engineer", "Data Labeling",
    "Data Scientist", "Database Administrator",
    "Artificial Intelligence", "AI Engineer", "AI Researcher",
    "Machine Learning", "Deep Learning", "NLP", "Natural Language",
    "Computer Vision", "Big Data", "Business Intelligence",
    "Market Research and Analysis", "Blockchain",
]

DATA_AI_TITLE_KEYWORDS = [
    "data scientist", "data analyst", "data engineer", "data architect",
    "machine learning", "ai engineer", "deep learning", "nlp",
    "computer vision", "big data", "business intelligence",
    "bi developer", "bi analyst", "ml engineer", "mlops",
    "data labeling", "dba", "database", "blockchain",
]


def classify_industry_group(industry):
    if not industry:
        return "IT General"
    ind = industry
    for kw in DATA_AI_KEYWORDS:
        if kw.lower() in ind.lower():
            return "Data/AI/ML"
    if "Software Engineering" in ind or "Software Engineer" in ind:
        return "Software Engineering"
    if "Software Testing" in ind or "Tester" in ind or "QA" in ind:
        return "Testing/QA"
    if "Infrastructure" in ind or "DevOps" in ind or "System" in ind:
        return "Infra/DevOps"
    if "Product Management" in ind or "Project Management" in ind:
        return "Product/Project Mgmt"
    if "Security" in ind or "Information Security" in ind:
        return "Security"
    if "Game" in ind:
        return "Game Dev"
    return "IT General"


def is_data_ai_by_title(title):
    """Check if a JD is Data/AI based on job title."""
    if not title:
        return False
    t = title.lower()
    return any(kw in t for kw in DATA_AI_TITLE_KEYWORDS)


# ========== Chuẩn hóa location ==========
PROVINCE_PATTERNS = [
    (r"(?:TP\.?\s*)?Hồ Chí Minh|HCM|Sài Gòn|Saigon|TPHCM|Thành phố Hồ Chí Minh|Thủ Đức", "Hồ Chí Minh"),
    (r"Hà Nội|Ha Noi|Hanoi", "Hà Nội"),
    (r"Đà Nẵng|Da Nang|Danang", "Đà Nẵng"),
    (r"Hải Phòng|Hai Phong", "Hải Phòng"),
    (r"Cần Thơ|Can Tho", "Cần Thơ"),
    (r"Bình Dương|Binh Duong|Thuận An|Dĩ An|Thủ Dầu Một", "Bình Dương"),
    (r"Đồng Nai|Dong Nai|Biên Hòa", "Đồng Nai"),
    (r"Long An", "Long An"),
    (r"Bắc Ninh|Bac Ninh", "Bắc Ninh"),
    (r"Hưng Yên|Hung Yen", "Hưng Yên"),
    (r"Vĩnh Phúc|Vinh Phuc", "Vĩnh Phúc"),
    (r"Bắc Giang|Bac Giang", "Bắc Giang"),
    (r"Thái Nguyên|Thai Nguyen", "Thái Nguyên"),
    (r"Nghệ An|Nghe An", "Nghệ An"),
    (r"Thanh Hóa|Thanh Hoa", "Thanh Hóa"),
    (r"Quảng Ninh|Quang Ninh", "Quảng Ninh"),
    (r"Khánh Hòa|Khanh Hoa|Nha Trang", "Khánh Hòa"),
    (r"Lâm Đồng|Lam Dong|Đà Lạt|Da Lat", "Lâm Đồng"),
    (r"Bà Rịa.*Vũng Tàu|BR-VT|Vũng Tàu|Vung Tau", "Bà Rịa - Vũng Tàu"),
    (r"Thừa Thiên.*Huế|Hue|Huế", "Thừa Thiên Huế"),
    (r"Bình Định|Binh Dinh|Quy Nhon|Quy Nhơn", "Bình Định"),
    (r"Quảng Nam|Quang Nam|Hội An", "Quảng Nam"),
    (r"Phú Thọ|Phu Tho", "Phú Thọ"),
    (r"Hà Nam|Ha Nam", "Hà Nam"),
    (r"Nam Định|Nam Dinh", "Nam Định"),
    (r"Ninh Bình|Ninh Binh", "Ninh Bình"),
    (r"Hải Dương|Hai Duong", "Hải Dương"),
    (r"Tây Ninh|Tay Ninh", "Tây Ninh"),
    (r"Bình Phước|Binh Phuoc", "Bình Phước"),
    (r"Tiền Giang|Tien Giang", "Tiền Giang"),
    (r"Kiên Giang|Kien Giang|Phú Quốc", "Kiên Giang"),
    (r"Đắk Lắk|Dak Lak|Buôn Ma Thuột", "Đắk Lắk"),
    (r"Gia Lai", "Gia Lai"),
    (r"Lào Cai|Lao Cai", "Lào Cai"),
    (r"Quảng Bình|Quang Binh", "Quảng Bình"),
    (r"Quảng Trị|Quang Tri", "Quảng Trị"),
    (r"Phú Yên|Phu Yen", "Phú Yên"),
    (r"Sóc Trăng|Soc Trang", "Sóc Trăng"),
    (r"Bến Tre|Ben Tre", "Bến Tre"),
    (r"Vĩnh Long|Vinh Long", "Vĩnh Long"),
    (r"An Giang", "An Giang"),
    (r"Đồng Tháp|Dong Thap", "Đồng Tháp"),
    (r"Trà Vinh|Tra Vinh", "Trà Vinh"),
    (r"Hậu Giang|Hau Giang", "Hậu Giang"),
    (r"Bạc Liêu|Bac Lieu", "Bạc Liêu"),
    (r"Cà Mau|Ca Mau", "Cà Mau"),
    (r"Remote|Từ xa|Làm việc từ xa", "Remote"),
    (r"Toàn quốc|All provinces|Tất cả", "Toàn quốc"),
]


def normalize_location(raw_location):
    """Normalize raw location to province/city level."""
    if not raw_location:
        return "Không rõ"
    for pattern, province in PROVINCE_PATTERNS:
        if re.search(pattern, raw_location, re.IGNORECASE):
            return province
    return "Khác"


# ========== Chuẩn hóa experience_level ==========
def normalize_experience(exp):
    """Normalize experience_level text to 5 standard groups."""
    if not exp:
        return "Không rõ"
    e = exp.lower().strip()

    # Intern/Fresher
    if any(k in e for k in ["thực tập", "intern", "fresher", "mới tốt nghiệp"]):
        return "Intern/Fresher"

    # Try to extract numeric years
    # Patterns: "3 năm", "1 - 2 năm", "2-5 năm", "dưới 1", "< 1", "0,5"
    match_range = re.search(r'(\d+(?:,\d+)?)\s*[-–—]\s*(\d+(?:,\d+)?)', e)
    match_single = re.search(r'(\d+(?:,\d+)?)\s*(?:năm|year)', e)
    match_below = re.search(r'(?:dưới|<|lên đến|từ 0)\s*(\d)', e)

    min_years = None
    if match_range:
        low = float(match_range.group(1).replace(',', '.'))
        high = float(match_range.group(2).replace(',', '.'))
        min_years = low
    elif match_single:
        min_years = float(match_single.group(1).replace(',', '.'))
    elif match_below:
        min_years = 0

    if "không" in e and "kinh nghiệm" not in e:
        # "Không" alone often means "no requirement"
        if min_years is None:
            return "Entry (0-1 năm)"

    if min_years is not None:
        if min_years < 1:
            return "Entry (0-1 năm)"
        elif min_years < 3:
            return "Junior (1-3 năm)"
        elif min_years < 5:
            return "Mid (3-5 năm)"
        else:
            return "Senior (5+ năm)"

    # Keyword fallback
    if any(k in e for k in ["trên 5", "hơn 5", "trên 3"]):
        return "Senior (5+ năm)"
    if any(k in e for k in ["trên 2", "trên 1"]):
        return "Junior (1-3 năm)"
    if "yêu cầu" in e and "kinh nghiệm" in e:
        return "Junior (1-3 năm)"

    return "Không rõ"


# ========== Map sang schema nội bộ ==========
def map_to_schema(jd, industry_group):
    """Map raw JD to internal schema with normalized fields."""
    return {
        "title": jd.get("job_title") or "",
        "requirements": jd.get("requirements") or "",
        "responsibilities": jd.get("job_description") or "",
        "level": jd.get("experience_level") or "",
        "level_normalized": normalize_experience(jd.get("experience_level")),
        "location": jd.get("location") or "",
        "location_normalized": normalize_location(jd.get("location")),
        "industry_group": industry_group,
        "metadata": {
            "company_name": jd.get("company_name") or "",
            "salary": jd.get("salary") or "",
            "benefits": jd.get("benefits") or "",
            "job_type": jd.get("job_type") or "",
            "education_level": jd.get("education_level") or "",
            "job_position": jd.get("job_position") or "",
            "job_industry": jd.get("job_industry") or "",
            "year": jd.get("year"),
            "source_dataset": "tinixai/vietnamese-job-descriptions",
            "source_id": jd.get("id"),
        },
    }


def main():
    random.seed(42)
    TARGET_TOTAL = 450
    DATA_AI_QUOTA_MIN = 60  # ~13% of 450

    print("=" * 70)
    print("Bước 2: Resample với quota Data/AI")
    print(f"  Mục tiêu: {TARGET_TOTAL} JD, Data/AI tối thiểu {DATA_AI_QUOTA_MIN}")
    print("=" * 70)

    # === Load & filter ===
    print("\n⏳ Đang tải dataset...")
    ds = load_dataset("tinixai/vietnamese-job-descriptions", split="train")
    print(f"✅ Đã tải: {len(ds):,} dòng")

    print("🔍 Lọc IT thuần...")
    it_jds = [ds[i] for i in range(len(ds)) if is_it_industry(ds[i]["job_industry"])]
    print(f"   IT thuần: {len(it_jds):,}")

    # Dedup
    seen_fp = {}
    unique_jds = []
    for jd in it_jds:
        company = normalize_text(jd.get("company_name") or "")
        desc = (jd.get("job_description") or "") + " " + (jd.get("requirements") or "")
        fp = company + "|" + text_fingerprint(desc)
        if fp not in seen_fp:
            seen_fp[fp] = True
            unique_jds.append(jd)

    # Remove empty
    valid_jds = []
    for jd in unique_jds:
        title = (jd.get("job_title") or "").strip()
        desc = (jd.get("job_description") or "").strip()
        req = (jd.get("requirements") or "").strip()
        if title and (desc or req) and len(desc + req) >= 100:
            valid_jds.append(jd)
    print(f"   Pool valid: {len(valid_jds):,}")

    # === Classify ===
    data_ai_pool = []
    other_pool = []

    for jd in valid_jds:
        group = classify_industry_group(jd.get("job_industry", ""))
        if group == "Data/AI/ML":
            data_ai_pool.append((jd, group))
        elif is_data_ai_by_title(jd.get("job_title")):
            # JD has Data/AI title but generic industry → count as Data/AI
            data_ai_pool.append((jd, "Data/AI/ML"))
        else:
            other_pool.append((jd, group))

    print("\n📊 Pool phân loại:")
    print(f"   Data/AI/ML: {len(data_ai_pool)}")
    print(f"   Other IT: {len(other_pool)}")

    # === Sample Data/AI ===
    # Take as many Data/AI as possible, up to quota
    random.shuffle(data_ai_pool)

    # Dedup by company within Data/AI (max 2 per company)
    data_ai_by_company = defaultdict(list)
    for jd, group in data_ai_pool:
        company = (jd.get("company_name") or "Unknown").strip()
        data_ai_by_company[company].append((jd, group))

    data_ai_sampled = []
    for company, jds_list in data_ai_by_company.items():
        for jd, group in jds_list[:3]:  # Max 3 per company for Data/AI
            data_ai_sampled.append((jd, group))

    # Cap at reasonable number
    data_ai_target = min(len(data_ai_sampled), 75)
    if len(data_ai_sampled) > data_ai_target:
        random.shuffle(data_ai_sampled)
        data_ai_sampled = data_ai_sampled[:data_ai_target]

    print(f"\n🎯 Data/AI sampled: {len(data_ai_sampled)}")

    # === Sample other groups ===
    other_target = TARGET_TOTAL - len(data_ai_sampled)
    print(f"🎯 Other IT target: {other_target}")

    # Group other by (group, experience_category)
    other_groups = defaultdict(list)
    for jd, group in other_pool:
        exp_cat = normalize_experience(jd.get("experience_level"))
        other_groups[(group, exp_cat)].append((jd, group))

    # Round-robin sampling
    other_sampled = []
    other_ids = set()
    group_keys = list(other_groups.keys())
    random.shuffle(group_keys)

    round_num = 0
    while len(other_sampled) < other_target:
        added = 0
        for key in group_keys:
            if len(other_sampled) >= other_target:
                break
            candidates = other_groups[key]
            if round_num < len(candidates):
                jd, group = candidates[round_num]
                jd_id = jd.get("id", id(jd))
                if jd_id not in other_ids:
                    other_sampled.append((jd, group))
                    other_ids.add(jd_id)
                    added += 1
        round_num += 1
        if added == 0:
            break

    print(f"   Other IT sampled: {len(other_sampled)}")

    # === Combine ===
    all_sampled = data_ai_sampled + other_sampled
    random.shuffle(all_sampled)
    print(f"\n✅ TỔNG: {len(all_sampled)} JD")

    # === Stats ===
    print("\n📊 Phân bố mẫu mới:")

    group_counts = Counter(group for _, group in all_sampled)
    print("\n  Nhóm ngành:")
    for group, count in group_counts.most_common():
        pct = count * 100 / len(all_sampled)
        print(f"    {group:<30} {count:>4} ({pct:.1f}%)")

    exp_counts = Counter(normalize_experience(jd.get("experience_level"))
                          for jd, _ in all_sampled)
    print("\n  Experience:")
    for cat, count in sorted(exp_counts.items()):
        pct = count * 100 / len(all_sampled)
        print(f"    {cat:<25} {count:>4} ({pct:.1f}%)")

    loc_counts = Counter(normalize_location(jd.get("location"))
                          for jd, _ in all_sampled)
    print("\n  Location (top 10):")
    for loc, count in loc_counts.most_common(10):
        pct = count * 100 / len(all_sampled)
        print(f"    {loc:<25} {count:>4} ({pct:.1f}%)")

    company_counts = Counter((jd.get("company_name") or "").strip()
                              for jd, _ in all_sampled)
    print(f"\n  Số công ty unique: {len(company_counts)}")
    print(f"  Max JD/công ty: {max(company_counts.values())}")

    # === Map schema + save ===
    print("\n" + "=" * 70)
    print("Map schema + chuẩn hóa + lưu file")
    print("=" * 70)

    output_jds = [map_to_schema(jd, group) for jd, group in all_sampled]

    # Save processed
    out_path = Path("data/processed/jds.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output_jds, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Đã lưu {len(output_jds)} JD tại: {out_path}")

    # Save raw
    raw_path = Path("data/raw/hf_it_jds_filtered.json")
    raw_data = [{k: v for k, v in jd.items()} for jd, _ in all_sampled]
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu raw tại: {raw_path}")

    # Verify Data/AI percentage
    data_ai_count = sum(1 for j in output_jds if j["industry_group"] == "Data/AI/ML")
    data_ai_pct = data_ai_count * 100 / len(output_jds)
    print(f"\n✅ Data/AI/ML: {data_ai_count}/{len(output_jds)} = {data_ai_pct:.1f}%")
    if data_ai_pct >= 12:
        print("   → ĐẠT quota sàn 12%!")
    else:
        print(f"   → CHƯA ĐẠT 12% (có {data_ai_pct:.1f}%)")

    # Sample Data/AI titles for verification
    print("\n--- Mẫu 10 JD Data/AI/ML ---")
    data_ai_jds = [j for j in output_jds if j["industry_group"] == "Data/AI/ML"]
    for i, jd in enumerate(data_ai_jds[:10]):
        print(f"  {i+1:>2}. {jd['title']}")
        print(f"      level: {jd['level_normalized']} | loc: {jd['location_normalized']}")

    print("\n✅ Hoàn tất bước 2! Sẵn sàng báo B commit.")


if __name__ == "__main__":
    main()
