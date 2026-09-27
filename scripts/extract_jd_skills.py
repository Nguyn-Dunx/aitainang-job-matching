"""Chay Tang 2 cho 450 JD: LLM that (NVIDIA NIM, batch 5 JD/call) + fallback rule.

    python scripts/extract_jd_skills.py --limit 5     # test nhanh 1 batch
    python scripts/extract_jd_skills.py               # chay full 450

Output: data/processed/jds_skills.json — list cung thu tu voi jds.json:
{title, skills, years_required, evidence_snippet, method: "llm"|"rule"}
Checkpoint sau moi batch — chet giua chung chay lai khong mat ket qua.
Batch loi -> tung JD trong batch do fallback rule (khong bo sot JD nao).
"""

import argparse
import json
import logging
import time
from pathlib import Path

from app.services.jd_extraction import extract_jd_batch_llm, extract_jd_rule

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
JDS_PATH = ROOT / "data" / "processed" / "jds.json"
OUT_PATH = ROOT / "data" / "processed" / "jds_skills.json"
BATCH_SIZE = 5


def jd_text(it: dict) -> str:
    return "\n\n".join(p for p in [it.get("title", ""), it.get("responsibilities", ""),
                                   it.get("requirements", "")] if p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Chi chay N JD dau (test)")
    args = ap.parse_args()

    items = json.load(open(JDS_PATH, encoding="utf-8"))
    if args.limit:
        items = items[: args.limit]

    results: list[dict] = []
    done_titles = set()
    if OUT_PATH.exists():
        results = json.load(open(OUT_PATH, encoding="utf-8"))
        done_titles = {r["title"] for r in results}
        log.info("Resume: da co %d ket qua", len(results))

    todo = [it for it in items if it["title"] not in done_titles]
    log.info("Can chay: %d/%d JD", len(todo), len(items))

    n_llm = n_rule = 0
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start : start + BATCH_SIZE]
        texts = [jd_text(it) for it in batch]
        t0 = time.perf_counter()
        try:
            extracted = extract_jd_batch_llm(texts)
            methods = ["llm"] * len(batch)
            n_llm += len(batch)
        except Exception as e:  # noqa: BLE001 — batch loi thi tung JD ve rule
            log.warning("Batch %d loi (%s) -> fallback rule cho %d JD", start, e, len(batch))
            extracted = [extract_jd_rule(t) for t in texts]
            methods = ["rule"] * len(batch)
            n_rule += len(batch)
        for it, r, m in zip(batch, extracted, methods):
            results.append({"title": it["title"], "skills": r.skills,
                            "years_required": r.years_required,
                            "evidence_snippet": r.evidence_snippet, "method": m})
        log.info("[%d/%d] batch %d JD xong (%.0fs), tong skills batch dau: %d",
                 min(start + BATCH_SIZE, len(todo)), len(todo), len(batch),
                 time.perf_counter() - t0, len(extracted[0].skills))
        json.dump(results, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    log.info("XONG: %d JD (llm=%d, rule=%d) -> %s", len(results), n_llm, n_rule, OUT_PATH)


if __name__ == "__main__":
    main()
