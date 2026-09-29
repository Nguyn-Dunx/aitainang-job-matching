"""Probe chẩn đoán: gọi 1 model NIM với đúng prompt Tầng 5, in exception hoặc latency thật.

Không phải số liệu chính thức (số liệu chính thức đo qua endpoint) — chỉ dùng để
biết LÝ DO ultra thất bại (lỗi gì, hay chỉ là chậm hơn budget 15s).

Cách chạy:
    .venv/Scripts/python.exe scripts/probe_model_once.py nvidia/nemotron-3-ultra-550b-a55b
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

from app.config import settings
from app.services.cv_improve import _SUGGEST_PROMPT, _extract_json

PROMPT = _SUGGEST_PROMPT.format(
    job_title="Backend Developer (Node.JS/PHP)",
    missing_skills="- Docker\n- Kubernetes\n- Redis\n- GraphQL\n- Microservices",
    experience="- Xây dựng REST API bằng Node.js và Express\n- Viết unit test, deploy lên staging",
)


def main() -> None:
    model = sys.argv[1]
    tmo = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key, max_retries=0)
    t0 = time.perf_counter()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=0,
            timeout=tmo,
            response_format={"type": "json_object"},
        )
        elapsed = time.perf_counter() - t0
        content = resp.choices[0].message.content
        data = _extract_json(content)
        n = len(data.get("suggestions", [])) if data else 0
        print(f"OK: model={model} | {elapsed:.1f}s | suggestions={n} | "
              f"finish_reason={resp.choices[0].finish_reason}")
        print(f"content[:300]={content[:300]!r}")
    except Exception as e:  # noqa: BLE001
        elapsed = time.perf_counter() - t0
        print(f"FAIL sau {elapsed:.1f}s: {type(e).__name__}: {str(e)[:500]}")


if __name__ == "__main__":
    main()
