"""Migration 002: them 3 cot loc vao bang jds (PA2 — cot rieng co index, khong JSONB).

    python scripts/migrate_002_jd_filter_columns.py

Idempotent: dung IF NOT EXISTS, chay lai bao nhieu lan cung an toan.
"""

from sqlalchemy import text

from app.db import engine

STATEMENTS = [
    "ALTER TABLE jds ADD COLUMN IF NOT EXISTS location_normalized VARCHAR(100)",
    "ALTER TABLE jds ADD COLUMN IF NOT EXISTS level_normalized VARCHAR(50)",
    "ALTER TABLE jds ADD COLUMN IF NOT EXISTS industry_group VARCHAR(100)",
    "CREATE INDEX IF NOT EXISTS ix_jds_location_normalized ON jds (location_normalized)",
    "CREATE INDEX IF NOT EXISTS ix_jds_level_normalized ON jds (level_normalized)",
    "CREATE INDEX IF NOT EXISTS ix_jds_industry_group ON jds (industry_group)",
]


def main() -> None:
    with engine.begin() as conn:
        for stmt in STATEMENTS:
            conn.execute(text(stmt))
            print("OK:", stmt)
    print("Migration 002 hoan tat.")


if __name__ == "__main__":
    main()
