"""
Bước 1: Đếm chính xác số JD Data Science/Engineering và AI/ML
trong pool 9,748 JD IT đã lọc (trước sampling).

Usage:
    python scripts/count_data_ai_pool.py
"""
import hashlib
import re
from collections import Counter

from datasets import load_dataset

# --- Cùng logic lọc IT thuần từ filter_and_sample_jds.py ---
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


# --- Phân loại nhóm ngành chi tiết ---
DATA_AI_KEYWORDS = [
    "Data Science", "Data Analyst", "Data Engineer", "Data",
    "Artificial Intelligence", "AI Engineer", "AI",
    "Machine Learning", "ML",
    "Deep Learning",
    "NLP", "Natural Language",
    "Computer Vision",
    "Big Data",
    "Business Intelligence",
    "Market Research and Analysis",
]


def classify_industry_group(industry):
    """Classify a job_industry value into a high-level group."""
    if not industry:
        return "Unknown"
    ind = industry

    # Data Science / AI / ML — check first (more specific)
    for kw in DATA_AI_KEYWORDS:
        if kw.lower() in ind.lower():
            return "Data/AI/ML"

    if "Software Engineering" in ind or "Software Engineer" in ind:
        return "Software Engineering"
    if "Software Testing" in ind or "Tester" in ind or "QA" in ind:
        return "Software Testing/QA"
    if "Infrastructure" in ind or "DevOps" in ind or "System" in ind:
        return "Infrastructure/DevOps"
    if "Product Management" in ind or "Project Management" in ind:
        return "Product/Project Management"
    if "Security" in ind or "Information Security" in ind:
        return "Security"
    if "Game" in ind:
        return "Game Development"
    if "IT Phần mềm" in ind or "IT phần mềm" in ind or "CNTT" in ind:
        return "IT Phần mềm (general)"
    if "IT Phần cứng" in ind or "IT phần cứng" in ind or "Mạng" in ind:
        return "IT Phần cứng/Mạng"
    if "Công nghệ thông tin" in ind.lower():
        return "IT khác"
    return "Other IT"


def main():
    print("=" * 70)
    print("Bước 1: Đếm Data/AI JD trong pool IT đã lọc")
    print("=" * 70)

    # Load dataset
    print("\n⏳ Đang tải dataset...")
    ds = load_dataset("tinixai/vietnamese-job-descriptions", split="train")
    print(f"✅ Đã tải: {len(ds):,} dòng")

    # Filter IT
    print("🔍 Lọc IT thuần...")
    it_jds = [ds[i] for i in range(len(ds)) if is_it_industry(ds[i]["job_industry"])]
    print(f"✅ IT thuần: {len(it_jds):,}")

    # Dedup
    print("🧹 Loại trùng lặp...")
    seen_fp = {}
    unique_jds = []
    for jd in it_jds:
        company = normalize_text(jd.get("company_name", ""))
        desc = jd.get("job_description", "") or ""
        req = jd.get("requirements", "") or ""
        fp = company + "|" + text_fingerprint(desc + " " + req)
        if fp not in seen_fp:
            seen_fp[fp] = True
            unique_jds.append(jd)
    print(f"   Sau dedup: {len(unique_jds):,}")

    # Remove empty
    valid_jds = []
    for jd in unique_jds:
        title = (jd.get("job_title") or "").strip()
        desc = (jd.get("job_description") or "").strip()
        req = (jd.get("requirements") or "").strip()
        if title and (desc or req) and len(desc + req) >= 100:
            valid_jds.append(jd)
    print(f"   Sau loại thiếu nội dung: {len(valid_jds):,}")

    # Classify each JD
    print("\n📊 Phân loại nhóm ngành trong pool:")
    group_counter = Counter()
    group_jds = {}
    for jd in valid_jds:
        group = classify_industry_group(jd.get("job_industry", ""))
        group_counter[group] += 1
        if group not in group_jds:
            group_jds[group] = []
        group_jds[group].append(jd)

    print(f"\n{'Nhóm ngành':<35} {'Số JD':>8} {'%':>6}")
    print("-" * 55)
    for group, count in group_counter.most_common():
        pct = count * 100 / len(valid_jds)
        marker = " <<<" if group == "Data/AI/ML" else ""
        print(f"  {group:<33} {count:>8,} {pct:>5.1f}%{marker}")
    print(f"  {'TỔNG':<33} {len(valid_jds):>8,}")

    # Detail Data/AI/ML
    data_ai_jds = group_jds.get("Data/AI/ML", [])
    print(f"\n{'='*70}")
    print(f"CHI TIẾT Data/AI/ML: {len(data_ai_jds)} JD")
    print(f"{'='*70}")

    if data_ai_jds:
        # Sub-categories
        sub_counter = Counter()
        for jd in data_ai_jds:
            ind = jd.get("job_industry", "")
            sub_counter[ind] += 1

        print("\nPhân bố job_industry cụ thể:")
        for ind, cnt in sub_counter.most_common():
            print(f"  [{cnt:>3}] {ind}")

        # Sample titles
        print("\nMẫu job_title (20 JD đầu):")
        for i, jd in enumerate(data_ai_jds[:20]):
            print(f"  {i+1:>2}. {jd['job_title']} | {jd.get('company_name','')[:40]}")

    # Also check: JDs with Data/AI keywords in title/description but NOT in industry
    print(f"\n{'='*70}")
    print("KIỂM TRA BỔ SUNG: JD có keyword Data/AI trong title/description")
    print("nhưng KHÔNG nằm trong nhóm Data/AI/ML theo job_industry")
    print(f"{'='*70}")

    title_keywords = ["data scientist", "data analyst", "data engineer",
                       "machine learning", "ai engineer", "deep learning",
                       "nlp", "computer vision", "big data", "business intelligence",
                       "bi developer", "bi analyst", "data architect",
                       "ml engineer", "mle", "mlops"]

    extra_data_ai = []
    for jd in valid_jds:
        group = classify_industry_group(jd.get("job_industry", ""))
        if group == "Data/AI/ML":
            continue  # Already counted
        title = (jd.get("job_title") or "").lower()
        if any(kw in title for kw in title_keywords):
            extra_data_ai.append(jd)

    print(f"\nTìm thấy thêm {len(extra_data_ai)} JD Data/AI theo title:")
    for i, jd in enumerate(extra_data_ai[:20]):
        print(f"  {i+1:>2}. {jd['job_title']} | industry: {jd.get('job_industry','')[:50]}")

    total_data_ai = len(data_ai_jds) + len(extra_data_ai)
    print(f"\n{'='*70}")
    print("TỔNG KẾT:")
    print(f"  - Data/AI theo job_industry: {len(data_ai_jds)}")
    print(f"  - Data/AI theo title (bổ sung): {len(extra_data_ai)}")
    print(f"  - TỔNG Data/AI tiềm năng: {total_data_ai}")
    print(f"  - Pool IT tổng: {len(valid_jds):,}")
    print(f"  - Tỷ lệ Data/AI: {total_data_ai*100/len(valid_jds):.1f}%")
    print(f"{'='*70}")

    if total_data_ai >= 60:
        print("→ ĐỦ ≥60 JD → Có thể resample với quota sàn 12-15%")
    elif total_data_ai >= 30:
        print("→ Có 30-59 JD → Lấy gần hết, nhưng sẽ dưới 12%")
    else:
        print("→ DƯỚI 30 JD → Cần báo user quyết định")


if __name__ == "__main__":
    main()
