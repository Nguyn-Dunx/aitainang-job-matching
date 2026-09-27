"""Import data/processed/jds.json (ban moi nhat cua A) vao bang jds.

    python scripts/import_jds_json.py

- XOA toan bo JD cu truoc khi insert (tranh trung lap khi A cap nhat bo JD).
- 3 truong location_normalized / level_normalized / industry_group nam o TOP-LEVEL
  cua moi JD -> insert truc tiep vao 3 cot loc (PA2), khong qua JSONB.
- Phan con lai (level, location, metadata goc) luu trong parsed JSONB de audit.
"""

import json
from pathlib import Path

from sqlalchemy import text

from app.db import SessionLocal, engine
from app.models import JD

JDS_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "jds.json"


def main() -> None:
    with open(JDS_PATH, encoding="utf-8") as f:
        items = json.load(f)
    print(f"Doc {len(items)} JD tu {JDS_PATH.name}")

    with SessionLocal() as db:
        deleted = db.execute(text("DELETE FROM jds")).rowcount
        print(f"Da xoa {deleted} JD cu")

        for i, it in enumerate(items):
            raw_text = "\n\n".join(
                p for p in [it.get("title", ""), it.get("responsibilities", ""), it.get("requirements", "")] if p
            )
            db.add(JD(
                title=it.get("title", ""),
                raw_text=raw_text,
                # idx = khoa ghep on dinh voi jds.json/jds_embeddings.npy (title bi trung)
                parsed={"idx": i, "level": it.get("level"), "location": it.get("location"),
                        "metadata": it.get("metadata")},
                location_normalized=it.get("location_normalized"),
                level_normalized=it.get("level_normalized"),
                industry_group=it.get("industry_group"),
            ))
        db.commit()

        total = db.execute(text("SELECT count(*) FROM jds")).scalar()
        nulls = db.execute(text(
            "SELECT count(*) FROM jds WHERE location_normalized IS NULL "
            "OR level_normalized IS NULL OR industry_group IS NULL"
        )).scalar()
        print(f"Insert xong: {total} JD, {nulls} dong thieu cot loc")


if __name__ == "__main__":
    main()
