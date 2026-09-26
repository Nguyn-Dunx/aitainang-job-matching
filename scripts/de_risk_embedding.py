"""De-risk Tang 3: xac nhan model embedding chay on dinh tren may hien co.

    python scripts/de_risk_embedding.py [model_name]

Mac dinh: BAAI/bge-m3 (1024 dim, khop EMBEDDING_DIM trong app/models.py).
Do: thoi gian load, thoi gian encode 10 cau song ngu Viet-Anh, kich thuoc vector,
sanity check cosine similarity (cau cung y phai gan nhau hon cau khac y).
KHONG gan voi bo JD that — chi dung cau mau doc lap.
"""

import sys
import time

SENTENCES = [
    "Phát triển REST API bằng Python và Django",
    "Develop backend services using Python and Django",
    "Xây dựng giao diện người dùng bằng React",
    "Build user interfaces with React and TypeScript",
    "Phân tích dữ liệu bằng SQL và Power BI",
    "Vận hành hệ thống trên AWS, Docker, Kubernetes",
    "Thiết kế đồ họa bằng Adobe Photoshop",
    "Nấu ăn và pha chế đồ uống",
    "Kế toán tổng hợp và lập báo cáo tài chính",
    "Machine learning model deployment with Docker",
]


def main() -> None:
    model_name = sys.argv[1] if len(sys.argv) > 1 else "BAAI/bge-m3"
    from sentence_transformers import SentenceTransformer

    t0 = time.perf_counter()
    model = SentenceTransformer(model_name)
    t_load = time.perf_counter() - t0

    t0 = time.perf_counter()
    emb = model.encode(SENTENCES, normalize_embeddings=True)
    t_encode = time.perf_counter() - t0

    print(f"model: {model_name}")
    print(f"load: {t_load:.1f}s | encode {len(SENTENCES)} cau: {t_encode:.2f}s "
          f"({t_encode / len(SENTENCES) * 1000:.0f} ms/cau)")
    print(f"vector shape: {emb.shape} (dim={emb.shape[1]})")

    # Sanity: cap cung y (0-1: Python/Django Viet-Anh) phai gan hon cap khac y (0-6: Python vs Photoshop)
    import numpy as np

    sim = np.asarray(emb) @ np.asarray(emb).T
    print(f"cosine(cung y, Viet-Anh): {sim[0][1]:.3f} (mong doi > 0.7)")
    print(f"cosine(khac y):           {sim[0][6]:.3f} (mong doi < 0.5)")
    ok = sim[0][1] > 0.7 and sim[0][6] < 0.5 and emb.shape[1] == 1024
    print("KET LUAN:", "ON — model san sang cho Tang 3" if ok else "CAN XEM LAI")


if __name__ == "__main__":
    main()
