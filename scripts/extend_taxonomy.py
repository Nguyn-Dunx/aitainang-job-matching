"""
Bổ sung thêm skills vào seed taxonomy để đạt mục tiêu 200+ mục.
Tập trung: tools cụ thể phổ biến trong JD VN, kỹ năng domain IT VN,
soft skills VN, các công nghệ mới.

Chạy sau build_taxonomy.py — merge vào taxonomy có sẵn.

Usage:
    python scripts/extend_taxonomy.py
"""

import json
import re
from collections import Counter
from pathlib import Path

# ============================================================================
# BỔ SUNG SKILLS (60+ mục mới)
# ============================================================================

EXTRA_SKILLS = {
    # === Programming Languages (bổ sung) ===
    "Solidity": {
        "vi": "Solidity",
        "category": "Programming Language",
        "aliases": ["solidity"],
    },
    "Lua": {
        "vi": "Lua",
        "category": "Programming Language",
        "aliases": ["lua", "ngôn ngữ lua"],
    },
    "Perl": {
        "vi": "Perl",
        "category": "Programming Language",
        "aliases": ["perl"],
    },
    "VBA": {
        "vi": "VBA",
        "category": "Programming Language",
        "aliases": ["vba", "visual basic", "visual basic for applications"],
    },
    "MATLAB": {
        "vi": "MATLAB",
        "category": "Programming Language",
        "aliases": ["matlab"],
    },

    # === Backend Frameworks (bổ sung) ===
    "Gin": {
        "vi": "Gin",
        "category": "Backend Framework",
        "aliases": ["gin", "gin-gonic"],
    },
    "Fiber": {
        "vi": "Fiber",
        "category": "Backend Framework",
        "aliases": ["fiber", "gofiber"],
    },
    "Symfony": {
        "vi": "Symfony",
        "category": "Backend Framework",
        "aliases": ["symfony"],
    },
    "CodeIgniter": {
        "vi": "CodeIgniter",
        "category": "Backend Framework",
        "aliases": ["codeigniter", "code igniter"],
    },
    "Yii": {
        "vi": "Yii",
        "category": "Backend Framework",
        "aliases": ["yii", "yii2", "yii framework"],
    },

    # === Frontend (bổ sung) ===
    "Nuxt.js": {
        "vi": "Nuxt.js",
        "category": "Frontend Framework",
        "aliases": ["nuxt", "nuxtjs", "nuxt.js"],
    },
    "Svelte": {
        "vi": "Svelte",
        "category": "Frontend Framework",
        "aliases": ["svelte", "sveltekit"],
    },
    "SASS/SCSS": {
        "vi": "SASS/SCSS",
        "category": "Frontend Library",
        "aliases": ["sass", "scss", "less"],
    },
    "Material UI": {
        "vi": "Material UI",
        "category": "Frontend Library",
        "aliases": ["material ui", "material-ui", "mui"],
    },
    "Ant Design": {
        "vi": "Ant Design",
        "category": "Frontend Library",
        "aliases": ["ant design", "antd", "ant-design"],
    },

    # === Databases (bổ sung) ===
    "ClickHouse": {
        "vi": "ClickHouse",
        "category": "Database",
        "aliases": ["clickhouse", "click house"],
    },
    "Neo4j": {
        "vi": "Neo4j",
        "category": "Database",
        "aliases": ["neo4j"],
    },
    "CouchDB": {
        "vi": "CouchDB",
        "category": "Database",
        "aliases": ["couchdb", "couch db"],
    },
    "InfluxDB": {
        "vi": "InfluxDB",
        "category": "Database",
        "aliases": ["influxdb", "influx db"],
    },
    "Memcached": {
        "vi": "Memcached",
        "category": "Database",
        "aliases": ["memcached", "memcache"],
    },

    # === DevOps & Infrastructure (bổ sung) ===
    "GitLab CI/CD": {
        "vi": "GitLab CI/CD",
        "category": "DevOps & Infrastructure",
        "aliases": ["gitlab ci", "gitlab ci/cd", "gitlab-ci"],
    },
    "GitHub Actions": {
        "vi": "GitHub Actions",
        "category": "DevOps & Infrastructure",
        "aliases": ["github actions", "github action"],
    },
    "ArgoCD": {
        "vi": "ArgoCD",
        "category": "DevOps & Infrastructure",
        "aliases": ["argocd", "argo cd"],
    },
    "Helm": {
        "vi": "Helm",
        "category": "DevOps & Infrastructure",
        "aliases": ["helm", "helm chart"],
    },
    "Prometheus": {
        "vi": "Prometheus",
        "category": "DevOps & Infrastructure",
        "aliases": ["prometheus"],
    },
    "Grafana": {
        "vi": "Grafana",
        "category": "DevOps & Infrastructure",
        "aliases": ["grafana"],
    },
    "ELK Stack": {
        "vi": "ELK Stack",
        "category": "DevOps & Infrastructure",
        "aliases": ["elk", "elk stack", "logstash", "kibana"],
    },
    "Docker Compose": {
        "vi": "Docker Compose",
        "category": "DevOps & Infrastructure",
        "aliases": ["docker compose", "docker-compose"],
    },
    "HAProxy": {
        "vi": "HAProxy",
        "category": "DevOps & Infrastructure",
        "aliases": ["haproxy", "ha proxy"],
    },
    "Load Balancer": {
        "vi": "Cân bằng tải",
        "category": "DevOps & Infrastructure",
        "aliases": ["load balancer", "load balancing", "cân bằng tải"],
    },
    "CDN": {
        "vi": "Mạng phân phối nội dung",
        "category": "DevOps & Infrastructure",
        "aliases": ["cdn", "cloudflare", "content delivery network"],
    },

    # === Cloud Services (bổ sung) ===
    "AWS Lambda": {
        "vi": "AWS Lambda",
        "category": "Cloud Platform",
        "aliases": ["lambda", "aws lambda", "serverless"],
    },
    "AWS S3": {
        "vi": "AWS S3",
        "category": "Cloud Platform",
        "aliases": ["s3", "aws s3", "amazon s3"],
    },
    "AWS EC2": {
        "vi": "AWS EC2",
        "category": "Cloud Platform",
        "aliases": ["ec2", "aws ec2", "amazon ec2"],
    },
    "Heroku": {
        "vi": "Heroku",
        "category": "Cloud Platform",
        "aliases": ["heroku"],
    },
    "DigitalOcean": {
        "vi": "DigitalOcean",
        "category": "Cloud Platform",
        "aliases": ["digitalocean", "digital ocean"],
    },

    # === Data & AI (bổ sung) ===
    "Scikit-learn": {
        "vi": "Scikit-learn",
        "category": "AI & Data Science",
        "aliases": ["scikit-learn", "sklearn", "scikit learn"],
    },
    "Keras": {
        "vi": "Keras",
        "category": "AI & Data Science",
        "aliases": ["keras"],
    },
    "OpenCV": {
        "vi": "OpenCV",
        "category": "AI & Data Science",
        "aliases": ["opencv", "open cv"],
    },
    "Hugging Face": {
        "vi": "Hugging Face",
        "category": "AI & Data Science",
        "aliases": ["hugging face", "huggingface", "transformers"],
    },
    "LLM": {
        "vi": "Mô hình ngôn ngữ lớn",
        "category": "AI & Data Science",
        "aliases": ["llm", "large language model", "mô hình ngôn ngữ lớn",
                     "chatgpt", "gpt"],
    },
    "MLOps": {
        "vi": "MLOps",
        "category": "AI & Data Science",
        "aliases": ["mlops", "ml ops"],
    },
    "Apache Airflow": {
        "vi": "Apache Airflow",
        "category": "Data Engineering",
        "aliases": ["airflow", "apache airflow"],
    },
    "dbt": {
        "vi": "dbt",
        "category": "Data Engineering",
        "aliases": ["dbt", "data build tool"],
    },
    "Apache Flink": {
        "vi": "Apache Flink",
        "category": "Data Engineering",
        "aliases": ["flink", "apache flink"],
    },
    "Data Lake": {
        "vi": "Hồ dữ liệu",
        "category": "Data Engineering",
        "aliases": ["data lake", "hồ dữ liệu", "data lakehouse"],
    },
    "Data Pipeline": {
        "vi": "Đường ống dữ liệu",
        "category": "Data Engineering",
        "aliases": ["data pipeline", "đường ống dữ liệu", "pipeline dữ liệu"],
    },
    "Google Analytics": {
        "vi": "Google Analytics",
        "category": "Data Visualization",
        "aliases": ["google analytics", "ga", "ga4"],
    },
    "Looker": {
        "vi": "Looker",
        "category": "Data Visualization",
        "aliases": ["looker", "looker studio"],
    },
    "Metabase": {
        "vi": "Metabase",
        "category": "Data Visualization",
        "aliases": ["metabase"],
    },

    # === Security (bổ sung) ===
    "OWASP": {
        "vi": "OWASP",
        "category": "Security",
        "aliases": ["owasp", "owasp top 10"],
    },
    "VPN": {
        "vi": "VPN",
        "category": "Security",
        "aliases": ["vpn", "virtual private network"],
    },
    "SSL/TLS": {
        "vi": "SSL/TLS",
        "category": "Security",
        "aliases": ["ssl", "tls", "ssl/tls", "https"],
    },
    "OAuth": {
        "vi": "OAuth",
        "category": "Security",
        "aliases": ["oauth", "oauth2", "oauth 2.0"],
    },
    "JWT": {
        "vi": "JWT",
        "category": "Security",
        "aliases": ["jwt", "json web token"],
    },

    # === Testing (bổ sung) ===
    "Cypress": {
        "vi": "Cypress",
        "category": "Testing",
        "aliases": ["cypress"],
    },
    "Appium": {
        "vi": "Appium",
        "category": "Testing",
        "aliases": ["appium"],
    },
    "JMeter": {
        "vi": "JMeter",
        "category": "Testing",
        "aliases": ["jmeter", "apache jmeter"],
    },
    "pytest": {
        "vi": "pytest",
        "category": "Testing",
        "aliases": ["pytest"],
    },
    "TestNG": {
        "vi": "TestNG",
        "category": "Testing",
        "aliases": ["testng", "test ng"],
    },

    # === Architecture (bổ sung) ===
    "WebSocket": {
        "vi": "WebSocket",
        "category": "Architecture",
        "aliases": ["websocket", "web socket", "socket.io"],
    },
    "gRPC": {
        "vi": "gRPC",
        "category": "Architecture",
        "aliases": ["grpc", "g rpc"],
    },
    "Message Queue": {
        "vi": "Hàng đợi tin nhắn",
        "category": "Architecture",
        "aliases": ["message queue", "hàng đợi", "message broker"],
    },
    "Event-Driven Architecture": {
        "vi": "Kiến trúc hướng sự kiện",
        "category": "Architecture",
        "aliases": ["event-driven", "event driven", "kiến trúc hướng sự kiện"],
    },
    "CQRS": {
        "vi": "CQRS",
        "category": "Architecture",
        "aliases": ["cqrs"],
    },
    "Domain-Driven Design": {
        "vi": "Thiết kế hướng miền",
        "category": "Architecture",
        "aliases": ["ddd", "domain-driven design", "domain driven design"],
    },
    "Clean Architecture": {
        "vi": "Kiến trúc sạch",
        "category": "Architecture",
        "aliases": ["clean architecture", "kiến trúc sạch"],
    },

    # === Methodology (bổ sung) ===
    "Waterfall": {
        "vi": "Thác nước",
        "category": "Methodology",
        "aliases": ["waterfall", "mô hình thác nước"],
    },
    "Kanban": {
        "vi": "Kanban",
        "category": "Methodology",
        "aliases": ["kanban"],
    },
    "TDD": {
        "vi": "Phát triển hướng kiểm thử",
        "category": "Methodology",
        "aliases": ["tdd", "test driven development", "test-driven development"],
    },
    "Code Review": {
        "vi": "Đánh giá mã nguồn",
        "category": "Methodology",
        "aliases": ["code review", "review code", "đánh giá mã nguồn"],
    },
    "SDLC": {
        "vi": "Vòng đời phát triển phần mềm",
        "category": "Methodology",
        "aliases": ["sdlc", "software development life cycle",
                     "vòng đời phát triển phần mềm"],
    },

    # === Soft Skills (bổ sung — rất phổ biến trong JD VN) ===
    "Independent Work": {
        "vi": "Làm việc độc lập",
        "category": "Soft Skill",
        "aliases": ["làm việc độc lập", "độc lập", "chủ động",
                     "independent", "work independently", "tự chủ"],
    },
    "Responsibility": {
        "vi": "Trách nhiệm",
        "category": "Soft Skill",
        "aliases": ["trách nhiệm", "tinh thần trách nhiệm", "responsibility",
                     "responsible", "trách nhiệm cao"],
    },
    "Attention to Detail": {
        "vi": "Cẩn thận chi tiết",
        "category": "Soft Skill",
        "aliases": ["cẩn thận", "tỉ mỉ", "chi tiết", "attention to detail",
                     "cẩn thận chi tiết", "tỉ mỉ chi tiết"],
    },
    "Creativity": {
        "vi": "Sáng tạo",
        "category": "Soft Skill",
        "aliases": ["sáng tạo", "creativity", "creative", "tư duy sáng tạo"],
    },
    "Customer Service": {
        "vi": "Chăm sóc khách hàng",
        "category": "Soft Skill",
        "aliases": ["chăm sóc khách hàng", "hỗ trợ khách hàng", "customer service",
                     "customer support"],
    },
    "Mentoring": {
        "vi": "Hướng dẫn/Đào tạo",
        "category": "Soft Skill",
        "aliases": ["mentor", "mentoring", "hướng dẫn", "đào tạo nhân viên",
                     "coaching"],
    },
    "Report Writing": {
        "vi": "Viết báo cáo",
        "category": "Soft Skill",
        "aliases": ["viết báo cáo", "báo cáo", "report", "reporting",
                     "viết tài liệu", "documentation"],
    },
    "Project Management": {
        "vi": "Quản lý dự án",
        "category": "Soft Skill",
        "aliases": ["quản lý dự án", "project management", "quản trị dự án"],
    },
    "Negotiation": {
        "vi": "Đàm phán",
        "category": "Soft Skill",
        "aliases": ["đàm phán", "negotiation", "thương lượng"],
    },

    # === Design Tools (bổ sung) ===
    "Sketch": {
        "vi": "Sketch",
        "category": "Design Tool",
        "aliases": ["sketch"],
    },
    "Adobe XD": {
        "vi": "Adobe XD",
        "category": "Design Tool",
        "aliases": ["adobe xd", "xd"],
    },
    "InVision": {
        "vi": "InVision",
        "category": "Design Tool",
        "aliases": ["invision"],
    },
    "Zeplin": {
        "vi": "Zeplin",
        "category": "Design Tool",
        "aliases": ["zeplin"],
    },
    "After Effects": {
        "vi": "After Effects",
        "category": "Design Tool",
        "aliases": ["after effects", "adobe after effects", "ae"],
    },

    # === Enterprise & Specific ===
    "ServiceNow": {
        "vi": "ServiceNow",
        "category": "Enterprise Software",
        "aliases": ["servicenow", "service now"],
    },
    "Microsoft Office": {
        "vi": "Tin học văn phòng",
        "category": "Enterprise Software",
        "aliases": ["microsoft office", "ms office", "office 365",
                     "tin học văn phòng", "vi tính văn phòng", "word", "excel",
                     "powerpoint"],
    },
    "Odoo": {
        "vi": "Odoo",
        "category": "Enterprise Software",
        "aliases": ["odoo"],
    },
    "ITIL": {
        "vi": "ITIL",
        "category": "Domain Knowledge",
        "aliases": ["itil", "it infrastructure library"],
    },
    "PCI DSS": {
        "vi": "PCI DSS",
        "category": "Domain Knowledge",
        "aliases": ["pci dss", "pci"],
    },
    "SLA": {
        "vi": "Thỏa thuận mức dịch vụ",
        "category": "Domain Knowledge",
        "aliases": ["sla", "service level agreement"],
    },
}


def main():
    print("=" * 70)
    print("Mở rộng taxonomy: bổ sung thêm skills")
    print("=" * 70)

    # Load existing taxonomy
    tax_path = Path("data/taxonomy/skills_taxonomy.json")
    with open(tax_path, encoding="utf-8") as f:
        taxonomy = json.load(f)

    existing_canonicals = {s["canonical"] for s in taxonomy["skills"]}
    print(f"✅ Taxonomy hiện có: {len(existing_canonicals)} skills")
    print(f"   Bổ sung thêm: {len(EXTRA_SKILLS)} skills mới")

    # Check for duplicates
    dupes = set(EXTRA_SKILLS.keys()) & existing_canonicals
    if dupes:
        print(f"⚠️  Trùng lặp (bỏ qua): {dupes}")

    # Load JDs for frequency counting
    jds_path = Path("data/processed/jds.json")
    with open(jds_path, encoding="utf-8") as f:
        jds = json.load(f)

    # Build alias lookup for new skills only
    alias_lookup = {}
    for canonical, info in EXTRA_SKILLS.items():
        if canonical in existing_canonicals:
            continue
        for alias in info["aliases"]:
            alias_lookup[alias.lower()] = canonical

    # Count frequency in JDs
    jd_counter = Counter()
    mention_counter = Counter()

    for jd in jds:
        req = (jd.get("requirements") or "").lower()
        resp = (jd.get("responsibilities") or "").lower()
        text = req + " " + resp

        found_in_jd = set()
        sorted_aliases = sorted(alias_lookup.keys(), key=len, reverse=True)

        for alias in sorted_aliases:
            if len(alias) <= 3:
                pattern = r'(?<![a-zA-Zà-ỹ])' + re.escape(alias) + r'(?![a-zA-Zà-ỹ])'
            else:
                pattern = r'\b' + re.escape(alias) + r'\b'

            matches = list(re.finditer(pattern, text))
            if matches:
                canonical = alias_lookup[alias]
                mention_counter[canonical] += len(matches)
                found_in_jd.add(canonical)

        for skill in found_in_jd:
            jd_counter[skill] += 1

    # Add new skills to taxonomy
    added = 0
    for canonical, info in EXTRA_SKILLS.items():
        if canonical in existing_canonicals:
            continue

        jd_count = jd_counter.get(canonical, 0)
        total_mentions = mention_counter.get(canonical, 0)

        entry = {
            "canonical": canonical,
            "vi": info["vi"],
            "category": info["category"],
            "aliases": info["aliases"],
            "frequency": {
                "jd_count": jd_count,
                "total_mentions": total_mentions,
                "jd_percentage": round(jd_count * 100 / len(jds), 1),
            },
        }
        taxonomy["skills"].append(entry)
        added += 1

    # Re-sort by jd_count
    taxonomy["skills"].sort(key=lambda x: x["frequency"]["jd_count"], reverse=True)

    # Update metadata
    taxonomy["metadata"]["total_skills"] = len(taxonomy["skills"])
    taxonomy["metadata"]["total_active_skills"] = sum(
        1 for s in taxonomy["skills"] if s["frequency"]["jd_count"] > 0
    )
    taxonomy["metadata"]["total_aliases"] = sum(
        len(s["aliases"]) for s in taxonomy["skills"]
    )
    taxonomy["metadata"]["version"] = "1.1.0"

    # Recalculate category summary
    from collections import defaultdict
    categories = defaultdict(lambda: {"total": 0, "active": 0})
    for skill in taxonomy["skills"]:
        cat = skill["category"]
        categories[cat]["total"] += 1
        if skill["frequency"]["jd_count"] > 0:
            categories[cat]["active"] += 1

    taxonomy["metadata"]["categories"] = [
        {"name": cat, "skill_count": info["total"], "active_in_jds": info["active"]}
        for cat, info in sorted(categories.items())
    ]

    # Save
    with open(tax_path, "w", encoding="utf-8") as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Đã thêm {added} skills mới")
    print("📊 Taxonomy cập nhật:")
    print(f"   - Tổng skills: {taxonomy['metadata']['total_skills']}")
    print(f"   - Active in JDs: {taxonomy['metadata']['total_active_skills']}")
    print(f"   - Tổng aliases: {taxonomy['metadata']['total_aliases']}")

    # Show new skills found in JDs
    print("\n🆕 Skills mới xuất hiện trong JD:")
    new_found = [(canonical, jd_counter[canonical])
                  for canonical in EXTRA_SKILLS
                  if canonical not in existing_canonicals and jd_counter.get(canonical, 0) > 0]
    new_found.sort(key=lambda x: -x[1])
    for skill, count in new_found:
        pct = count * 100 / len(jds)
        print(f"   [{count:>3} JD, {pct:4.1f}%] {skill}")

    # Update summary file
    summary_path = Path("data/taxonomy/skills_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"{'Rank':>4} | {'Skill':<35} | {'Category':<30} | "
                f"{'JD Count':>8} | {'%':>5} | {'Vi':<35}\n")
        f.write("-" * 140 + "\n")
        for i, entry in enumerate(taxonomy["skills"], 1):
            f.write(
                f"{i:>4} | {entry['canonical']:<35} | "
                f"{entry['category']:<30} | "
                f"{entry['frequency']['jd_count']:>8} | "
                f"{entry['frequency']['jd_percentage']:>5.1f} | "
                f"{entry['vi']:<35}\n"
            )
    print(f"💾 Đã cập nhật summary tại: {summary_path}")

    # Final check
    total = taxonomy['metadata']['total_skills']
    if total >= 200:
        print(f"\n✅ ĐẠT MỤC TIÊU: {total} skills (yêu cầu 200-500)")
    else:
        print(f"\n⚠️  Chưa đạt mục tiêu: {total}/200 skills — cần bổ sung thêm")


if __name__ == "__main__":
    main()
