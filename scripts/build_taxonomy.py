"""
Bước 7: Xây taxonomy kỹ năng song ngữ D4 từ 400 JD IT đã lọc.

Quy trình:
  1. Đọc 400 JD từ data/processed/jds.json
  2. Trích xuất skill mentions từ requirements + responsibilities
  3. Đếm tần suất, merge alias, phân loại
  4. Bổ sung tên tiếng Việt
  5. Lưu data/taxonomy/skills_taxonomy.json

Usage:
    python scripts/build_taxonomy.py
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# ============================================================================
# SEED TAXONOMY: Từ điển kỹ năng gốc, phân loại sẵn
# Mỗi entry: canonical_en -> { vi, category, aliases (case-insensitive) }
# Alias bao gồm các biến thể viết hoa/thường, viết tắt, tiếng Việt
# ============================================================================

SEED_TAXONOMY = {
    # ======================== PROGRAMMING LANGUAGES ========================
    "Python": {
        "vi": "Python",
        "category": "Programming Language",
        "aliases": ["python", "python3", "python 3", "python 3.x", "lập trình python",
                     "ngôn ngữ python", "python programming"],
    },
    "Java": {
        "vi": "Java",
        "category": "Programming Language",
        "aliases": ["java", "java se", "java ee", "core java", "lập trình java",
                     "ngôn ngữ java"],
    },
    "JavaScript": {
        "vi": "JavaScript",
        "category": "Programming Language",
        "aliases": ["javascript", "js", "ecmascript", "es6", "es6+", "es2015",
                     "lập trình javascript"],
    },
    "TypeScript": {
        "vi": "TypeScript",
        "category": "Programming Language",
        "aliases": ["typescript", "ts"],
    },
    "C#": {
        "vi": "C#",
        "category": "Programming Language",
        "aliases": ["c#", "csharp", "c sharp", "lập trình c#"],
    },
    "C++": {
        "vi": "C++",
        "category": "Programming Language",
        "aliases": ["c++", "cpp", "c plus plus", "lập trình c++"],
    },
    "C": {
        "vi": "C",
        "category": "Programming Language",
        "aliases": ["ngôn ngữ c", "lập trình c"],
    },
    "PHP": {
        "vi": "PHP",
        "category": "Programming Language",
        "aliases": ["php", "php7", "php8", "lập trình php"],
    },
    "Go": {
        "vi": "Go",
        "category": "Programming Language",
        "aliases": ["golang", "go lang", "ngôn ngữ go"],
    },
    "Ruby": {
        "vi": "Ruby",
        "category": "Programming Language",
        "aliases": ["ruby", "ngôn ngữ ruby"],
    },
    "Swift": {
        "vi": "Swift",
        "category": "Programming Language",
        "aliases": ["swift", "ngôn ngữ swift"],
    },
    "Kotlin": {
        "vi": "Kotlin",
        "category": "Programming Language",
        "aliases": ["kotlin"],
    },
    "Rust": {
        "vi": "Rust",
        "category": "Programming Language",
        "aliases": ["rust", "ngôn ngữ rust"],
    },
    "Scala": {
        "vi": "Scala",
        "category": "Programming Language",
        "aliases": ["scala"],
    },
    "Dart": {
        "vi": "Dart",
        "category": "Programming Language",
        "aliases": ["dart", "ngôn ngữ dart"],
    },
    "R": {
        "vi": "R",
        "category": "Programming Language",
        "aliases": ["ngôn ngữ r", "r programming"],
    },
    "Objective-C": {
        "vi": "Objective-C",
        "category": "Programming Language",
        "aliases": ["objective-c", "objective c", "obj-c", "objc"],
    },
    "Shell/Bash": {
        "vi": "Shell/Bash",
        "category": "Programming Language",
        "aliases": ["bash", "shell", "shell script", "bash script", "sh"],
    },
    "SQL": {
        "vi": "SQL",
        "category": "Programming Language",
        "aliases": ["sql", "structured query language", "ngôn ngữ sql", "truy vấn sql"],
    },
    "HTML": {
        "vi": "HTML",
        "category": "Web Technology",
        "aliases": ["html", "html5", "html 5"],
    },
    "CSS": {
        "vi": "CSS",
        "category": "Web Technology",
        "aliases": ["css", "css3", "css 3"],
    },

    # ======================== FRAMEWORKS & LIBRARIES ========================
    "React": {
        "vi": "React",
        "category": "Frontend Framework",
        "aliases": ["react", "reactjs", "react.js", "react js"],
    },
    "Angular": {
        "vi": "Angular",
        "category": "Frontend Framework",
        "aliases": ["angular", "angularjs", "angular.js", "angular js", "angular 2+"],
    },
    "Vue.js": {
        "vi": "Vue.js",
        "category": "Frontend Framework",
        "aliases": ["vue", "vuejs", "vue.js", "vue js", "vue 3", "vue2", "vue3"],
    },
    "Next.js": {
        "vi": "Next.js",
        "category": "Frontend Framework",
        "aliases": ["next.js", "nextjs", "next js"],
    },
    "Node.js": {
        "vi": "Node.js",
        "category": "Backend Framework",
        "aliases": ["node.js", "nodejs", "node js", "node"],
    },
    "Express.js": {
        "vi": "Express.js",
        "category": "Backend Framework",
        "aliases": ["express", "expressjs", "express.js"],
    },
    "NestJS": {
        "vi": "NestJS",
        "category": "Backend Framework",
        "aliases": ["nestjs", "nest.js", "nest js"],
    },
    "Django": {
        "vi": "Django",
        "category": "Backend Framework",
        "aliases": ["django"],
    },
    "Flask": {
        "vi": "Flask",
        "category": "Backend Framework",
        "aliases": ["flask"],
    },
    "FastAPI": {
        "vi": "FastAPI",
        "category": "Backend Framework",
        "aliases": ["fastapi", "fast api"],
    },
    "Spring": {
        "vi": "Spring",
        "category": "Backend Framework",
        "aliases": ["spring", "spring boot", "springboot", "spring framework",
                     "spring mvc", "spring cloud"],
    },
    "Laravel": {
        "vi": "Laravel",
        "category": "Backend Framework",
        "aliases": ["laravel"],
    },
    ".NET": {
        "vi": ".NET",
        "category": "Backend Framework",
        "aliases": [".net", "dotnet", "dot net", ".net core", ".net framework",
                     "asp.net", "asp net"],
    },
    "Ruby on Rails": {
        "vi": "Ruby on Rails",
        "category": "Backend Framework",
        "aliases": ["rails", "ruby on rails", "ror"],
    },
    "React Native": {
        "vi": "React Native",
        "category": "Mobile Framework",
        "aliases": ["react native", "react-native"],
    },
    "Flutter": {
        "vi": "Flutter",
        "category": "Mobile Framework",
        "aliases": ["flutter"],
    },
    "jQuery": {
        "vi": "jQuery",
        "category": "Frontend Library",
        "aliases": ["jquery", "jquery"],
    },
    "Bootstrap": {
        "vi": "Bootstrap",
        "category": "Frontend Library",
        "aliases": ["bootstrap"],
    },
    "Tailwind CSS": {
        "vi": "Tailwind CSS",
        "category": "Frontend Library",
        "aliases": ["tailwind", "tailwindcss", "tailwind css"],
    },
    "Redux": {
        "vi": "Redux",
        "category": "Frontend Library",
        "aliases": ["redux", "redux toolkit"],
    },
    "Webpack": {
        "vi": "Webpack",
        "category": "Build Tool",
        "aliases": ["webpack"],
    },

    # ======================== DATABASES ========================
    "MySQL": {
        "vi": "MySQL",
        "category": "Database",
        "aliases": ["mysql", "my sql"],
    },
    "PostgreSQL": {
        "vi": "PostgreSQL",
        "category": "Database",
        "aliases": ["postgresql", "postgres", "postgre", "pgsql"],
    },
    "MongoDB": {
        "vi": "MongoDB",
        "category": "Database",
        "aliases": ["mongodb", "mongo", "mongo db"],
    },
    "Redis": {
        "vi": "Redis",
        "category": "Database",
        "aliases": ["redis"],
    },
    "Microsoft SQL Server": {
        "vi": "SQL Server",
        "category": "Database",
        "aliases": ["sql server", "mssql", "ms sql", "ms sql server",
                     "microsoft sql server"],
    },
    "Oracle Database": {
        "vi": "Oracle Database",
        "category": "Database",
        "aliases": ["oracle", "oracle db", "oracle database", "db oracle", "oracle sql"],
    },
    "Elasticsearch": {
        "vi": "Elasticsearch",
        "category": "Database",
        "aliases": ["elasticsearch", "elastic search", "elastic"],
    },
    "Firebase": {
        "vi": "Firebase",
        "category": "Database",
        "aliases": ["firebase"],
    },
    "DynamoDB": {
        "vi": "DynamoDB",
        "category": "Database",
        "aliases": ["dynamodb", "dynamo db", "amazon dynamodb"],
    },
    "Cassandra": {
        "vi": "Cassandra",
        "category": "Database",
        "aliases": ["cassandra", "apache cassandra"],
    },
    "SQLite": {
        "vi": "SQLite",
        "category": "Database",
        "aliases": ["sqlite", "sqlite3"],
    },
    "MariaDB": {
        "vi": "MariaDB",
        "category": "Database",
        "aliases": ["mariadb", "maria db"],
    },

    # ======================== CLOUD & INFRASTRUCTURE ========================
    "AWS": {
        "vi": "Amazon Web Services",
        "category": "Cloud Platform",
        "aliases": ["aws", "amazon web services", "amazon aws"],
    },
    "Azure": {
        "vi": "Microsoft Azure",
        "category": "Cloud Platform",
        "aliases": ["azure", "microsoft azure", "ms azure"],
    },
    "Google Cloud Platform": {
        "vi": "Google Cloud",
        "category": "Cloud Platform",
        "aliases": ["gcp", "google cloud", "google cloud platform"],
    },
    "Docker": {
        "vi": "Docker",
        "category": "DevOps & Infrastructure",
        "aliases": ["docker", "docker container", "dockerfile"],
    },
    "Kubernetes": {
        "vi": "Kubernetes",
        "category": "DevOps & Infrastructure",
        "aliases": ["kubernetes", "k8s", "kube"],
    },
    "Jenkins": {
        "vi": "Jenkins",
        "category": "DevOps & Infrastructure",
        "aliases": ["jenkins"],
    },
    "CI/CD": {
        "vi": "Tích hợp/Triển khai liên tục",
        "category": "DevOps & Infrastructure",
        "aliases": ["ci/cd", "cicd", "ci cd", "continuous integration",
                     "continuous delivery", "continuous deployment"],
    },
    "Terraform": {
        "vi": "Terraform",
        "category": "DevOps & Infrastructure",
        "aliases": ["terraform"],
    },
    "Ansible": {
        "vi": "Ansible",
        "category": "DevOps & Infrastructure",
        "aliases": ["ansible"],
    },
    "Nginx": {
        "vi": "Nginx",
        "category": "DevOps & Infrastructure",
        "aliases": ["nginx"],
    },
    "Apache": {
        "vi": "Apache",
        "category": "DevOps & Infrastructure",
        "aliases": ["apache", "apache http", "apache server"],
    },
    "Linux": {
        "vi": "Linux",
        "category": "Operating System",
        "aliases": ["linux", "hệ điều hành linux", "centos", "ubuntu", "debian",
                     "redhat", "red hat"],
    },
    "Windows Server": {
        "vi": "Windows Server",
        "category": "Operating System",
        "aliases": ["windows server", "windows server 2019", "windows server 2022"],
    },
    "VMware": {
        "vi": "VMware",
        "category": "Virtualization",
        "aliases": ["vmware", "vmware vsphere", "vmware vsan", "vmware cloud",
                     "vmware esxi"],
    },

    # ======================== DATA & AI ========================
    "Machine Learning": {
        "vi": "Học máy",
        "category": "AI & Data Science",
        "aliases": ["machine learning", "ml", "học máy", "máy học"],
    },
    "Deep Learning": {
        "vi": "Học sâu",
        "category": "AI & Data Science",
        "aliases": ["deep learning", "dl", "học sâu"],
    },
    "Natural Language Processing": {
        "vi": "Xử lý ngôn ngữ tự nhiên",
        "category": "AI & Data Science",
        "aliases": ["nlp", "natural language processing", "xử lý ngôn ngữ tự nhiên"],
    },
    "Computer Vision": {
        "vi": "Thị giác máy tính",
        "category": "AI & Data Science",
        "aliases": ["computer vision", "cv", "thị giác máy tính"],
    },
    "TensorFlow": {
        "vi": "TensorFlow",
        "category": "AI & Data Science",
        "aliases": ["tensorflow", "tensor flow", "tf"],
    },
    "PyTorch": {
        "vi": "PyTorch",
        "category": "AI & Data Science",
        "aliases": ["pytorch", "py torch"],
    },
    "Pandas": {
        "vi": "Pandas",
        "category": "Data Engineering",
        "aliases": ["pandas"],
    },
    "NumPy": {
        "vi": "NumPy",
        "category": "Data Engineering",
        "aliases": ["numpy", "num py"],
    },
    "Apache Spark": {
        "vi": "Apache Spark",
        "category": "Data Engineering",
        "aliases": ["spark", "apache spark", "pyspark"],
    },
    "Apache Kafka": {
        "vi": "Apache Kafka",
        "category": "Data Engineering",
        "aliases": ["kafka", "apache kafka"],
    },
    "Hadoop": {
        "vi": "Hadoop",
        "category": "Data Engineering",
        "aliases": ["hadoop", "apache hadoop"],
    },
    "Power BI": {
        "vi": "Power BI",
        "category": "Data Visualization",
        "aliases": ["power bi", "powerbi", "power-bi"],
    },
    "Tableau": {
        "vi": "Tableau",
        "category": "Data Visualization",
        "aliases": ["tableau"],
    },
    "ETL": {
        "vi": "Trích xuất-Chuyển đổi-Nạp dữ liệu",
        "category": "Data Engineering",
        "aliases": ["etl", "extract transform load"],
    },
    "Data Warehouse": {
        "vi": "Kho dữ liệu",
        "category": "Data Engineering",
        "aliases": ["data warehouse", "data warehousing", "kho dữ liệu", "dwh"],
    },
    "Big Data": {
        "vi": "Dữ liệu lớn",
        "category": "Data Engineering",
        "aliases": ["big data", "dữ liệu lớn"],
    },
    "Data Analysis": {
        "vi": "Phân tích dữ liệu",
        "category": "Data Engineering",
        "aliases": ["data analysis", "phân tích dữ liệu", "data analytics"],
    },

    # ======================== TOOLS & PRACTICES ========================
    "Git": {
        "vi": "Git",
        "category": "Version Control",
        "aliases": ["git", "github", "gitlab", "bitbucket", "quản lý mã nguồn"],
    },
    "Jira": {
        "vi": "Jira",
        "category": "Project Management Tool",
        "aliases": ["jira", "atlassian jira"],
    },
    "Confluence": {
        "vi": "Confluence",
        "category": "Project Management Tool",
        "aliases": ["confluence"],
    },
    "Trello": {
        "vi": "Trello",
        "category": "Project Management Tool",
        "aliases": ["trello"],
    },
    "Figma": {
        "vi": "Figma",
        "category": "Design Tool",
        "aliases": ["figma"],
    },
    "Adobe Photoshop": {
        "vi": "Adobe Photoshop",
        "category": "Design Tool",
        "aliases": ["photoshop", "adobe photoshop", "ps"],
    },
    "Adobe Illustrator": {
        "vi": "Adobe Illustrator",
        "category": "Design Tool",
        "aliases": ["illustrator", "adobe illustrator", "ai illustrator"],
    },
    "Postman": {
        "vi": "Postman",
        "category": "API Tool",
        "aliases": ["postman"],
    },
    "Swagger": {
        "vi": "Swagger",
        "category": "API Tool",
        "aliases": ["swagger", "openapi"],
    },
    "RabbitMQ": {
        "vi": "RabbitMQ",
        "category": "Message Queue",
        "aliases": ["rabbitmq", "rabbit mq"],
    },
    "Microservices": {
        "vi": "Kiến trúc vi dịch vụ",
        "category": "Architecture",
        "aliases": ["microservices", "microservice", "micro services", "vi dịch vụ",
                     "kiến trúc microservice"],
    },
    "RESTful API": {
        "vi": "API RESTful",
        "category": "Architecture",
        "aliases": ["restful", "rest api", "restful api", "rest", "api restful"],
    },
    "GraphQL": {
        "vi": "GraphQL",
        "category": "Architecture",
        "aliases": ["graphql", "graph ql"],
    },

    # ======================== TESTING ========================
    "Unit Testing": {
        "vi": "Kiểm thử đơn vị",
        "category": "Testing",
        "aliases": ["unit test", "unit testing", "kiểm thử đơn vị"],
    },
    "Selenium": {
        "vi": "Selenium",
        "category": "Testing",
        "aliases": ["selenium", "selenium webdriver"],
    },
    "JUnit": {
        "vi": "JUnit",
        "category": "Testing",
        "aliases": ["junit"],
    },
    "Jest": {
        "vi": "Jest",
        "category": "Testing",
        "aliases": ["jest"],
    },
    "Automation Testing": {
        "vi": "Kiểm thử tự động",
        "category": "Testing",
        "aliases": ["automation testing", "automated testing", "test automation",
                     "kiểm thử tự động", "tự động hóa kiểm thử"],
    },
    "Manual Testing": {
        "vi": "Kiểm thử thủ công",
        "category": "Testing",
        "aliases": ["manual testing", "kiểm thử thủ công", "test thủ công"],
    },
    "Performance Testing": {
        "vi": "Kiểm thử hiệu năng",
        "category": "Testing",
        "aliases": ["performance testing", "kiểm thử hiệu năng", "load testing",
                     "stress testing"],
    },
    "API Testing": {
        "vi": "Kiểm thử API",
        "category": "Testing",
        "aliases": ["api testing", "kiểm thử api"],
    },

    # ======================== SECURITY ========================
    "Cybersecurity": {
        "vi": "An ninh mạng",
        "category": "Security",
        "aliases": ["cybersecurity", "cyber security", "an ninh mạng", "bảo mật mạng",
                     "information security", "infosec", "bảo mật thông tin"],
    },
    "Penetration Testing": {
        "vi": "Kiểm thử xâm nhập",
        "category": "Security",
        "aliases": ["penetration testing", "pentest", "pen test",
                     "kiểm thử xâm nhập"],
    },
    "Firewall": {
        "vi": "Tường lửa",
        "category": "Security",
        "aliases": ["firewall", "tường lửa"],
    },

    # ======================== NETWORKING ========================
    "Networking": {
        "vi": "Mạng máy tính",
        "category": "Networking",
        "aliases": ["networking", "network", "mạng", "mạng máy tính",
                     "hệ thống mạng"],
    },
    "Cisco": {
        "vi": "Cisco",
        "category": "Networking",
        "aliases": ["cisco", "cisco systems", "ccna", "ccnp"],
    },
    "TCP/IP": {
        "vi": "TCP/IP",
        "category": "Networking",
        "aliases": ["tcp/ip", "tcp ip", "giao thức tcp/ip"],
    },

    # ======================== METHODOLOGIES ========================
    "Agile": {
        "vi": "Agile",
        "category": "Methodology",
        "aliases": ["agile", "agile methodology", "phương pháp agile"],
    },
    "Scrum": {
        "vi": "Scrum",
        "category": "Methodology",
        "aliases": ["scrum", "scrum framework"],
    },
    "OOP": {
        "vi": "Lập trình hướng đối tượng",
        "category": "Methodology",
        "aliases": ["oop", "object oriented", "object-oriented",
                     "hướng đối tượng", "lập trình hướng đối tượng"],
    },
    "Design Patterns": {
        "vi": "Mẫu thiết kế",
        "category": "Methodology",
        "aliases": ["design patterns", "design pattern", "mẫu thiết kế"],
    },
    "SOLID": {
        "vi": "Nguyên tắc SOLID",
        "category": "Methodology",
        "aliases": ["solid principles", "nguyên tắc solid"],
    },

    # ======================== SOFT SKILLS ========================
    "Teamwork": {
        "vi": "Làm việc nhóm",
        "category": "Soft Skill",
        "aliases": ["teamwork", "team work", "làm việc nhóm", "làm việc team",
                     "làm việc theo nhóm", "phối hợp nhóm", "tinh thần đồng đội"],
    },
    "Communication": {
        "vi": "Giao tiếp",
        "category": "Soft Skill",
        "aliases": ["communication", "giao tiếp", "kỹ năng giao tiếp",
                     "communication skills"],
    },
    "Problem Solving": {
        "vi": "Giải quyết vấn đề",
        "category": "Soft Skill",
        "aliases": ["problem solving", "problem-solving", "giải quyết vấn đề",
                     "xử lý vấn đề", "khả năng giải quyết vấn đề"],
    },
    "Time Management": {
        "vi": "Quản lý thời gian",
        "category": "Soft Skill",
        "aliases": ["time management", "quản lý thời gian"],
    },
    "Leadership": {
        "vi": "Lãnh đạo",
        "category": "Soft Skill",
        "aliases": ["leadership", "lãnh đạo", "kỹ năng lãnh đạo", "dẫn dắt"],
    },
    "Analytical Thinking": {
        "vi": "Tư duy phân tích",
        "category": "Soft Skill",
        "aliases": ["analytical thinking", "analytical skills", "tư duy phân tích",
                     "phân tích logic", "tư duy logic"],
    },
    "Presentation": {
        "vi": "Thuyết trình",
        "category": "Soft Skill",
        "aliases": ["presentation", "thuyết trình", "kỹ năng thuyết trình"],
    },
    "Pressure Resilience": {
        "vi": "Chịu áp lực",
        "category": "Soft Skill",
        "aliases": ["chịu áp lực", "chịu được áp lực", "làm việc áp lực",
                     "chịu áp lực cao", "áp lực công việc", "work under pressure"],
    },
    "Self-Learning": {
        "vi": "Tự học",
        "category": "Soft Skill",
        "aliases": ["tự học", "ham học hỏi", "tự nghiên cứu", "học hỏi",
                     "tinh thần học hỏi", "khả năng tự học", "self-learning",
                     "continuous learning"],
    },
    "English Proficiency": {
        "vi": "Tiếng Anh",
        "category": "Language Skill",
        "aliases": ["tiếng anh", "english", "ngoại ngữ", "toeic", "ielts",
                     "đọc hiểu tiếng anh", "giao tiếp tiếng anh",
                     "tiếng anh giao tiếp", "tiếng anh đọc hiểu"],
    },
    "Japanese Proficiency": {
        "vi": "Tiếng Nhật",
        "category": "Language Skill",
        "aliases": ["tiếng nhật", "japanese", "jlpt", "n1", "n2", "n3"],
    },

    # ======================== DOMAIN KNOWLEDGE ========================
    "ERP": {
        "vi": "Hệ thống hoạch định nguồn lực doanh nghiệp",
        "category": "Domain Knowledge",
        "aliases": ["erp", "enterprise resource planning", "sap erp"],
    },
    "CRM": {
        "vi": "Quản lý quan hệ khách hàng",
        "category": "Domain Knowledge",
        "aliases": ["crm", "customer relationship management",
                     "quản lý quan hệ khách hàng", "salesforce"],
    },
    "E-commerce": {
        "vi": "Thương mại điện tử",
        "category": "Domain Knowledge",
        "aliases": ["e-commerce", "ecommerce", "thương mại điện tử", "tmđt"],
    },
    "Fintech": {
        "vi": "Công nghệ tài chính",
        "category": "Domain Knowledge",
        "aliases": ["fintech", "financial technology", "công nghệ tài chính"],
    },
    "Blockchain": {
        "vi": "Chuỗi khối",
        "category": "Domain Knowledge",
        "aliases": ["blockchain", "block chain", "chuỗi khối"],
    },
    "IoT": {
        "vi": "Internet vạn vật",
        "category": "Domain Knowledge",
        "aliases": ["iot", "internet of things", "internet vạn vật"],
    },

    # ======================== SPECIFIC TOOLS ========================
    "SAP": {
        "vi": "SAP",
        "category": "Enterprise Software",
        "aliases": ["sap", "sap erp", "sap hana", "sap b1"],
    },
    "Salesforce": {
        "vi": "Salesforce",
        "category": "Enterprise Software",
        "aliases": ["salesforce"],
    },
    "SharePoint": {
        "vi": "SharePoint",
        "category": "Enterprise Software",
        "aliases": ["sharepoint", "microsoft sharepoint", "ms sharepoint"],
    },
    "Unity": {
        "vi": "Unity",
        "category": "Game Engine",
        "aliases": ["unity", "unity3d", "unity 3d", "game engine unity"],
    },
    "Unreal Engine": {
        "vi": "Unreal Engine",
        "category": "Game Engine",
        "aliases": ["unreal", "unreal engine", "ue4", "ue5"],
    },

    # ======================== MOBILE ========================
    "Android Development": {
        "vi": "Phát triển Android",
        "category": "Mobile Development",
        "aliases": ["android", "android development", "phát triển android",
                     "lập trình android", "android sdk"],
    },
    "iOS Development": {
        "vi": "Phát triển iOS",
        "category": "Mobile Development",
        "aliases": ["ios", "ios development", "phát triển ios", "lập trình ios",
                     "xcode"],
    },

    # ======================== UX/UI ========================
    "UI/UX Design": {
        "vi": "Thiết kế UI/UX",
        "category": "Design",
        "aliases": ["ui/ux", "ux/ui", "ui ux", "ux ui", "thiết kế ui/ux",
                     "user experience", "user interface", "trải nghiệm người dùng"],
    },
    "Responsive Design": {
        "vi": "Thiết kế đáp ứng",
        "category": "Design",
        "aliases": ["responsive", "responsive design", "responsive web",
                     "thiết kế responsive"],
    },
}


def build_alias_lookup(seed):
    """Build reverse lookup: alias (lowered) -> canonical name."""
    lookup = {}
    for canonical, info in seed.items():
        for alias in info["aliases"]:
            lookup[alias.lower()] = canonical
    return lookup


def extract_skills_from_text(text, alias_lookup):
    """
    Extract skill mentions from text using alias matching.
    Returns Counter of canonical skill names.
    """
    if not text:
        return Counter()

    text_lower = text.lower()
    found = Counter()

    # Sort aliases by length (longest first) to match longest patterns first
    sorted_aliases = sorted(alias_lookup.keys(), key=len, reverse=True)

    # Track matched positions to avoid double-counting overlapping matches
    matched_positions = set()

    for alias in sorted_aliases:
        # Use word boundary matching for short aliases, substring for longer ones
        if len(alias) <= 3:
            # Short aliases need word boundaries to avoid false positives
            # e.g., "go" matching "good", "r" matching "requirements"
            if alias in ("c", "r", "go", "js", "ts", "dl", "ml", "sh", "ps",
                         "ai", "cv", "tf"):
                # Very short/ambiguous — require stricter context
                pattern = r'(?<![a-zA-Z])' + re.escape(alias) + r'(?![a-zA-Z])'
            else:
                pattern = r'\b' + re.escape(alias) + r'\b'
        else:
            pattern = r'\b' + re.escape(alias) + r'\b'

        for match in re.finditer(pattern, text_lower):
            start, end = match.start(), match.end()
            # Check if this position was already matched by a longer pattern
            if any(pos in matched_positions for pos in range(start, end)):
                continue
            canonical = alias_lookup[alias]
            found[canonical] += 1
            for pos in range(start, end):
                matched_positions.add(pos)

    return found


def main():
    print("=" * 70)
    print("Bước 7: Xây taxonomy kỹ năng song ngữ D4")
    print("=" * 70)

    # Load JDs
    jds_path = Path("data/processed/jds.json")
    with open(jds_path, encoding="utf-8") as f:
        jds = json.load(f)
    print(f"\n✅ Đã đọc {len(jds)} JD từ {jds_path}")

    # Build alias lookup
    alias_lookup = build_alias_lookup(SEED_TAXONOMY)
    print(f"✅ Seed taxonomy: {len(SEED_TAXONOMY)} skills, {len(alias_lookup)} aliases")

    # Extract skills from all JDs
    print("\n🔍 Trích xuất kỹ năng từ requirements + responsibilities...")
    global_counter = Counter()
    skill_jd_count = Counter()  # How many JDs mention each skill
    skill_by_jd = []  # Skills per JD for coverage analysis

    for jd in jds:
        req = jd.get("requirements", "") or ""
        resp = jd.get("responsibilities", "") or ""
        text = req + " " + resp

        jd_skills = extract_skills_from_text(text, alias_lookup)
        skill_by_jd.append(jd_skills)

        # Count total mentions
        global_counter.update(jd_skills)

        # Count JD presence (binary)
        for skill in jd_skills:
            skill_jd_count[skill] += 1

    # Coverage stats
    jds_with_skills = sum(1 for s in skill_by_jd if len(s) > 0)
    avg_skills = sum(len(s) for s in skill_by_jd) / len(skill_by_jd)
    print("\n📊 Thống kê trích xuất:")
    print(f"  - JD có ít nhất 1 skill: {jds_with_skills}/{len(jds)} "
          f"({jds_with_skills*100//len(jds)}%)")
    print(f"  - Trung bình skill/JD: {avg_skills:.1f}")
    print(f"  - Số skill unique tìm thấy: {len(global_counter)}")

    # Top skills
    print("\n🏆 Top 30 kỹ năng phổ biến nhất (theo số JD đề cập):")
    for i, (skill, count) in enumerate(skill_jd_count.most_common(30), 1):
        cat = SEED_TAXONOMY[skill]["category"]
        pct = count * 100 / len(jds)
        print(f"  {i:3d}. [{count:>3} JD, {pct:4.1f}%] {skill} ({cat})")

    # Skills NOT found in any JD
    unused = [s for s in SEED_TAXONOMY if s not in skill_jd_count]
    print(f"\n⚠️  Skill trong seed nhưng không tìm thấy: {len(unused)}")
    for s in sorted(unused):
        print(f"      - {s}")

    # ---- Build final taxonomy ----
    print("\n" + "=" * 70)
    print("Xây dựng taxonomy cuối cùng")
    print("=" * 70)

    # Only include skills found in at least 1 JD, plus important seeds
    # that might not appear due to regex issues
    taxonomy_entries = []
    for canonical, info in SEED_TAXONOMY.items():
        jd_count = skill_jd_count.get(canonical, 0)
        total_mentions = global_counter.get(canonical, 0)

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
        taxonomy_entries.append(entry)

    # Sort by jd_count descending
    taxonomy_entries.sort(key=lambda x: x["frequency"]["jd_count"], reverse=True)

    # Group by category for the final output
    categories = defaultdict(list)
    for entry in taxonomy_entries:
        categories[entry["category"]].append(entry)

    # Category summary
    print("\n📊 Phân bố theo nhóm:")
    cat_summary = []
    for cat, entries in sorted(categories.items()):
        active = sum(1 for e in entries if e["frequency"]["jd_count"] > 0)
        cat_summary.append((cat, len(entries), active))
        print(f"  {cat}: {len(entries)} skills ({active} xuất hiện trong JD)")

    # Build final output
    taxonomy_output = {
        "metadata": {
            "version": "1.0.0",
            "created_date": "2026-09-26",
            "source": "Thống kê tần suất từ 400 JD IT (dataset tinixai/vietnamese-job-descriptions)",
            "total_skills": len(taxonomy_entries),
            "total_active_skills": sum(
                1 for e in taxonomy_entries if e["frequency"]["jd_count"] > 0
            ),
            "total_aliases": sum(len(e["aliases"]) for e in taxonomy_entries),
            "categories": [
                {
                    "name": cat,
                    "skill_count": total,
                    "active_in_jds": active,
                }
                for cat, total, active in sorted(cat_summary)
            ],
        },
        "skills": taxonomy_entries,
    }

    # Save
    out_path = Path("data/taxonomy/skills_taxonomy.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(taxonomy_output, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Đã lưu taxonomy tại: {out_path}")
    print(f"   - {taxonomy_output['metadata']['total_skills']} skills")
    print(f"   - {taxonomy_output['metadata']['total_active_skills']} active in JDs")
    print(f"   - {taxonomy_output['metadata']['total_aliases']} aliases")

    # Also export a flat CSV-like summary for quick review
    summary_path = Path("data/taxonomy/skills_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"{'Rank':>4} | {'Skill':<30} | {'Category':<25} | "
                f"{'JD Count':>8} | {'%':>5} | {'Vi':>30}\n")
        f.write("-" * 120 + "\n")
        for i, entry in enumerate(taxonomy_entries, 1):
            f.write(
                f"{i:>4} | {entry['canonical']:<30} | "
                f"{entry['category']:<25} | "
                f"{entry['frequency']['jd_count']:>8} | "
                f"{entry['frequency']['jd_percentage']:>5.1f} | "
                f"{entry['vi']:<30}\n"
            )
    print(f"💾 Đã lưu summary tại: {summary_path}")

    print("\n✅ Hoàn tất bước 7!")
    print("\n📌 Lưu ý:")
    print(f"   - Taxonomy hiện có {taxonomy_output['metadata']['total_skills']} mục "
          f"(mục tiêu D4: 200-500)")
    if taxonomy_output['metadata']['total_skills'] < 200:
        print("   - Cần bổ sung thêm để đạt mục tiêu tối thiểu 200 mục")
    print("   - Nên review thủ công các alias, bổ sung domain-specific skills")
    print("   - Có thể dùng LLM để phát hiện thêm skill từ text tự do")


if __name__ == "__main__":
    main()
