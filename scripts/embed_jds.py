"""Tang 3: sinh embedding BGE-M3 cho 450 JD (title + responsibilities + requirements).

    python scripts/embed_jds.py              # luu data/processed/jds_embeddings.npy
    python scripts/embed_jds.py --to-db      # ghi vao cot embedding (pgvector) — can DB

Mac dinh chi luu file .npy (doc lap DB). Khi DB san sang, chay --to-db de nap.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
JDS_PATH = ROOT / "data" / "processed" / "jds.json"
OUT_PATH = ROOT / "data" / "processed" / "jds_embeddings.npy"
MODEL_NAME = "BAAI/bge-m3"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--to-db", action="store_true", help="Ghi embedding vao bang jds")
    args = ap.parse_args()

    items = json.load(open(JDS_PATH, encoding="utf-8"))
    texts = ["\n\n".join(p for p in [it.get("title", ""), it.get("responsibilities", ""),
                                     it.get("requirements", "")] if p) for it in items]
    print(f"Encode {len(texts)} JD bang {MODEL_NAME}...")

    from sentence_transformers import SentenceTransformer

    t0 = time.perf_counter()
    model = SentenceTransformer(MODEL_NAME)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    dt = time.perf_counter() - t0
    print(f"shape={emb.shape}, {dt:.1f}s tong ({dt / len(texts) * 1000:.0f} ms/JD)")

    np.save(OUT_PATH, emb)
    print(f"Da luu {OUT_PATH}")

    if args.to_db:
        from sqlalchemy import text

        from app.db import SessionLocal

        with SessionLocal() as db:
            titles = [it["title"] for it in items]
            rows = db.execute(text(
                "SELECT id, title FROM jds WHERE title = ANY(:titles)"),
                {"titles": titles}).all()
            by_title = {r.title: r.id for r in rows}
            for it, vec in zip(items, emb):
                jd_id = by_title.get(it["title"])
                if jd_id:
                    db.execute(text("UPDATE jds SET embedding = :v WHERE id = :id"),
                               {"v": vec.tolist(), "id": jd_id})
            db.commit()
            print(f"Da ghi embedding vao DB cho {len(by_title)}/{len(items)} JD")


if __name__ == "__main__":
    main()
