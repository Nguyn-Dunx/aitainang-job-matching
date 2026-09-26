"""Filter IT/Data-related values from HF dataset exploration results."""
import json

with open("data/raw/hf_dataset_exploration.json", encoding="utf-8") as f:
    data = json.load(f)

keywords = [
    "IT", "CNTT", "Công nghệ thông tin", "phần mềm", "Software", "Data",
    "Developer", "DevOps", "AI", "Machine Learning", "lập trình", "Tester",
    "QA", "Backend", "Frontend", "Fullstack", "Mobile", "Web", "Cloud",
    "Analyst", "Engineer", "Product Management", "Project Management",
    "System", "Database", "Mạng", "Infrastructure", "Security", "Cyber",
    "Artificial Intelligence", "Việc làm IT",
]


def matches(val):
    if not val:
        return False
    return any(kw.lower() in val.lower() for kw in keywords)


print("=" * 70)
print("JOB_INDUSTRY chứa từ khóa CNTT/Data/IT:")
print("=" * 70)
total_it = 0
for item in data["job_industry_unique"]:
    val = item["value"]
    if matches(val):
        print(f"  [{item['count']:>6,} JD] {val}")
        total_it += item["count"]
print(f"\n  >>> Tổng JD ngành IT/Data: {total_it:,}")

print()
print("=" * 70)
print("JOB_POSITION — TẤT CẢ giá trị (73 giá trị):")
print("=" * 70)
for i, item in enumerate(data["job_position_unique"], 1):
    marker = " <-- IT?" if matches(item["value"]) else ""
    print(f"  {i:3d}. [{item['count']:>6,} JD] {item['value']}{marker}")

print()
print("=" * 70)
print("JOB_INDUSTRY — TẤT CẢ giá trị (top 100):")
print("=" * 70)
for i, item in enumerate(data["job_industry_unique"][:100], 1):
    marker = " <-- IT?" if matches(item["value"]) else ""
    print(f"  {i:3d}. [{item['count']:>6,} JD] {item['value']}{marker}")
