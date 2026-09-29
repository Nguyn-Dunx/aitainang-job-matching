"""Che thong tin bi mat trong thu muc transcript da export (Prompt Log).

- Nhan 1 thu muc transcript (da export) -> tao ban da che sang thu muc output.
- Che: nvapi-*, npg_*, postgresql://user:pass@..., sk-*, VA tung gia tri bien trong .env
  hien tai (doc truc tiep tu .env, khong hardcode danh sach).
- In "file X: N chuoi da che" — KHONG in noi dung bi mat ra terminal/log.
- --verify: quet lai thu muc DA CHE, exit code != 0 neu con khop mau.

Cach dung:
    python scripts/redact_secrets.py <input_dir> <output_dir>
    python scripts/redact_secrets.py <input_dir> <output_dir> --verify
    python scripts/redact_secrets.py <redacted_dir> --verify
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ENV_PATH = Path(".env")
PLACEHOLDER = "[REDACTED]"

# Mau co dinh (khong phu thuoc .env)
FIXED_PATTERNS = [
    re.compile(r"nvapi-[A-Za-z0-9_\-]{6,}"),
    re.compile(r"npg_[A-Za-z0-9]{6,}"),
    re.compile(r"postgres(?:ql)?://[^\s\"']+"),
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
]

TEXT_SUFFIXES = {".txt", ".md", ".json", ".log", ".csv", ".vtt", ".srt", ".jsonl"}


def load_env_values(env_path: Path = ENV_PATH) -> list[str]:
    """Doc .env, tra ve danh sach gia tri bien (bo qua gia tri ngan/rong)."""
    if not env_path.exists():
        return []
    values: list[str] = []
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        _, _, val = line.partition("=")
        val = val.strip().strip('"').strip("'")
        # Bo qua gia tri qua ngan (vd so, true/false) de tranh che bua.
        if len(val) >= 6:
            values.append(val)
    return values


def build_patterns(env_values: list[str]) -> list[re.Pattern]:
    pats = list(FIXED_PATTERNS)
    for v in env_values:
        pats.append(re.compile(re.escape(v)))
    return pats


def redact_text(text: str, patterns: list[re.Pattern]) -> tuple[str, int]:
    count = 0
    for p in patterns:
        text, n = p.subn(PLACEHOLDER, text)
        count += n
    return text, count


def iter_text_files(root: Path):
    for f in sorted(root.rglob("*")):
        if f.is_file() and (f.suffix.lower() in TEXT_SUFFIXES or f.suffix == ""):
            yield f


def do_redact(in_dir: Path, out_dir: Path, patterns: list[re.Pattern]) -> int:
    total = 0
    for f in iter_text_files(in_dir):
        rel = f.relative_to(in_dir)
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            print(f"file {rel}: LOI doc ({e.__class__.__name__})")
            continue
        redacted, n = redact_text(text, patterns)
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(redacted, encoding="utf-8")
        print(f"file {rel}: {n} chuoi da che")
        total += n
    print(f"TONG: {total} chuoi da che -> {out_dir}")
    return total


def do_verify(dir_path: Path, patterns: list[re.Pattern]) -> int:
    """Quet lai thu muc da che; tra ve so file con khop mau (0 = sach)."""
    dirty = 0
    for f in iter_text_files(dir_path):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hits = sum(len(p.findall(text)) for p in patterns)
        if hits:
            print(f"file {f.relative_to(dir_path)}: CON {hits} khop mau (CHUA SACH)")
            dirty += 1
    if dirty == 0:
        print(f"VERIFY OK: {dir_path} sach (khong con khop mau)")
    else:
        print(f"VERIFY FAIL: {dirty} file con khop mau")
    return dirty


def main() -> int:
    ap = argparse.ArgumentParser(description="Che bi mat trong transcript Prompt Log.")
    ap.add_argument("input_dir", help="Thu muc transcript da export (hoac thu muc da che khi --verify)")
    ap.add_argument("output_dir", nargs="?", help="Thu muc xuat ban da che")
    ap.add_argument("--verify", action="store_true", help="Quet lai thu muc da che, exit != 0 neu con khop")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    if not in_dir.is_dir():
        print(f"LOI: khong phai thu muc: {in_dir}")
        return 2

    patterns = build_patterns(load_env_values())

    if args.verify:
        target = Path(args.output_dir) if args.output_dir else in_dir
        return 1 if do_verify(target, patterns) else 0

    if not args.output_dir:
        print("LOI: can output_dir khi khong dung --verify")
        return 2
    do_redact(in_dir, Path(args.output_dir), patterns)
    return 0


if __name__ == "__main__":
    sys.exit(main())
