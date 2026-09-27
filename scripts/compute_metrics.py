"""Tinh metric danh gia he thong (muc 9): Precision@5, nDCG@10, Spearman, MAE.

    python scripts/compute_metrics.py \
        --pairs data/labeled/annotation_pairs_pilot.csv \
        --labels data/labeled/annotations_merged.csv \
        --variants hybrid_v2 keyword_only embedding_only

- Retrieval: voi moi CV, xep hang cac JD trong bo pairs theo diem he thong;
  relevant = nhan nguoi cham >= 4 (thang 1-5).
- Ranking: Spearman giua diem he thong (0-100) va score_mean; MAE sau khi scale
  diem he thong ve thang 1-5 (chia 20).
- Doc du lieu tu FILE (jds.json + jds_skills.json + jds_embeddings.npy, khoa = idx),
  khong can DB. CV embed bang BGE-M3 qua app.services.embedding.
"""

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RELEVANT_THRESHOLD = 4.0


def precision_at_k(ranked_relevance: list[int], k: int) -> float:
    top = ranked_relevance[:k]
    return sum(top) / k if top else 0.0


def ndcg_at_k(ranked_scores: list[float], k: int) -> float:
    def dcg(scores):
        return sum(s / math.log2(i + 2) for i, s in enumerate(scores[:k]))
    ideal = dcg(sorted(ranked_scores, reverse=True))
    return dcg(ranked_scores) / ideal if ideal > 0 else 0.0


def spearman(x: list[float], y: list[float]) -> float:
    from scipy.stats import spearmanr
    if len(set(x)) < 2 or len(set(y)) < 2:
        return float("nan")
    return float(spearmanr(x, y).statistic)


def mae_scaled(system_scores: list[float], human_scores: list[float]) -> float:
    return float(np.mean([abs(s / 20 - h) for s, h in zip(system_scores, human_scores)]))


def jd_index(jd_id: str, jds: list[dict]) -> int:
    """jd_id = source_id (str) hoac jd_XXXX (fallback positional)."""
    if jd_id.startswith("jd_"):
        return int(jd_id.split("_")[1])
    for i, jd in enumerate(jds):
        if str(jd.get("metadata", {}).get("source_id")) == jd_id:
            return i
    raise KeyError(jd_id)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--variants", nargs="+", default=["hybrid_v2"])
    args = ap.parse_args()

    from app.services.embedding import embed_query
    from app.services.scoring import VARIANTS, PairInput

    jds = json.load(open(ROOT / "data/processed/jds.json", encoding="utf-8"))
    skills = json.load(open(ROOT / "data/processed/jds_skills.json", encoding="utf-8"))
    embeddings = np.load(ROOT / "data/processed/jds_embeddings.npy")

    labels = {}
    for row in csv.DictReader(open(args.labels, encoding="utf-8")):
        labels[(row["cv_id"], row["jd_id"])] = float(row["score_mean"])

    pairs = [r for r in csv.DictReader(open(args.pairs, encoding="utf-8"))
             if (r["cv_id"], r["jd_id"]) in labels]

    # Load CV pilot (json da parse) + embed 1 lan
    cv_cache: dict[str, dict] = {}
    for p in pairs:
        cid = p["cv_id"]
        if cid not in cv_cache:
            rec = json.load(open(ROOT / "data/processed/cvs_pilot" / f"{cid}.json", encoding="utf-8"))
            cv_text = " ".join(rec.get("skills", [])) + " " + str(rec.get("target_industry", ""))
            cv_cache[cid] = {"skills": rec.get("skills", []), "text": cv_text,
                             "vec": embed_query(cv_text)}

    for variant_name in args.variants:
        fn = VARIANTS[variant_name]
        rows = []
        for p in pairs:
            i = jd_index(p["jd_id"], jds)
            jd = jds[i]
            jd_text = "\n".join([jd.get("title", ""), jd.get("responsibilities", ""),
                                 jd.get("requirements", "")])
            cv = cv_cache[p["cv_id"]]
            cos = float(np.dot(cv["vec"], embeddings[i]))
            r = fn(PairInput(cv_text=cv["text"], cv_skills=cv["skills"], jd_text=jd_text,
                             jd_skills=skills[i]["skills"], cosine_sim=cos,
                             jd_evidence=skills[i].get("evidence_snippet", "")))
            if r["score_total"] is None:
                continue
            rows.append({"cv_id": p["cv_id"], "system": r["score_total"],
                         "human": labels[(p["cv_id"], p["jd_id"])]})

        # Retrieval metrics theo tung CV
        p5s, ndcg10s = [], []
        for cid in {r["cv_id"] for r in rows}:
            group = sorted([r for r in rows if r["cv_id"] == cid],
                           key=lambda r: r["system"], reverse=True)
            rel = [1 if r["human"] >= RELEVANT_THRESHOLD else 0 for r in group]
            p5s.append(precision_at_k(rel, 5))
            ndcg10s.append(ndcg_at_k([r["human"] for r in group], 10))

        sys_scores = [r["system"] for r in rows]
        hum_scores = [r["human"] for r in rows]
        print(f"\n=== {variant_name} ({len(rows)} cap) ===")
        print(f"Precision@5 : {np.mean(p5s):.3f}")
        print(f"nDCG@10     : {np.mean(ndcg10s):.3f}")
        print(f"Spearman    : {spearman(sys_scores, hum_scores):.3f}")
        print(f"MAE (1-5)   : {mae_scaled(sys_scores, hum_scores):.3f}")


if __name__ == "__main__":
    main()
