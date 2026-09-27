"""Tầng 2 phía JD — trích skill từ requirements + responsibilities bằng LLM thật.

- llm: NVIDIA NIM (OpenAI-compatible), JSON schema {skills, years_required,
  evidence_snippet}, validate pydantic, retry 1 lần khi JSON hỏng.
- rule: fallback deterministic — match canonical/alias của taxonomy D4 trực tiếp
  trong text. CHỈ dùng khi LLM lỗi/timeout/JSON hỏng.
- skills trả về phải thuộc taxonomy 235 skill của A (canonical name) — LLM được
  cung cấp danh sách canonical trong prompt, output bị lọc lại theo taxonomy.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from app.services.cv_extraction import _match_skills

log = logging.getLogger(__name__)

MAX_JD_CHARS = 6000
TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "taxonomy" / "skills_taxonomy.json"


class JDSchema(BaseModel):
    skills: list[str] = Field(default_factory=list)
    years_required: float | None = None
    evidence_snippet: str = ""  # trích nguyên văn đoạn JD làm bằng chứng


def _load_canonical_skills(taxonomy_path: Path = TAXONOMY_PATH) -> list[str]:
    with open(taxonomy_path, encoding="utf-8") as f:
        return [s["canonical"] for s in json.load(f)["skills"]]


_LLM_SYSTEM = (
    "Bạn là bộ trích xuất kỹ năng từ JD (job description) tuyển dụng IT tiếng Việt. "
    "Chỉ trả về JSON hợp lệ theo schema, không giải thích. "
    "skills CHỈ được chọn từ danh sách canonical cho sẵn, đúng chính tả từng kỹ năng. "
    "years_required = số năm kinh nghiệm JD yêu cầu (null nếu không ghi / fresher). "
    "evidence_snippet = trích NGUYÊN VĂN 1-2 câu từ JD chứa yêu cầu chính."
)

_LLM_INSTRUCTION = """Danh sách skill canonical được phép dùng:
{canonical}

Trích xuất JD sau thành JSON:
{{"skills": [string], "years_required": number|null, "evidence_snippet": string}}

JD:
{text}"""


def extract_jd_llm(text: str, client=None, model: str | None = None,
                   taxonomy_path: Path = TAXONOMY_PATH) -> JDSchema:
    from openai import OpenAI

    from app.config import settings

    client = client or OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    model = model or settings.llm_model
    canonical = _load_canonical_skills(taxonomy_path)
    payload = _LLM_INSTRUCTION.format(canonical=", ".join(canonical), text=text[:MAX_JD_CHARS])

    last_err: Exception | None = None
    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _LLM_SYSTEM},
                    {"role": "user", "content": payload},
                ],
                response_format={"type": "json_object"},
                temperature=0,
                timeout=60,
            )
            data = json.loads(resp.choices[0].message.content)
            result = JDSchema.model_validate(data)
            # Lọc skill ngoài taxonomy (LLM bịa tên) — giữ đúng canonical
            valid = set(canonical)
            result.skills = sorted({s for s in result.skills if s in valid})
            return result
        except (json.JSONDecodeError, ValidationError, KeyError, IndexError) as e:
            last_err = e
            log.warning("LLM JD extraction attempt %d failed: %s", attempt + 1, e)
    raise RuntimeError(f"LLM JD extraction failed after 2 attempts: {last_err}")


_BATCH_INSTRUCTION = """Danh sách skill canonical được phép dùng:
{canonical}

Trích xuất TỪNG JD bên dưới thành JSON:
{{"results": [{{"index": int, "skills": [string], "years_required": number|null, "evidence_snippet": string}}]}}
- index = số thứ tự JD trong danh sách (bắt đầu từ 0)
- skills CHỈ chọn từ danh sách canonical; evidence_snippet trích nguyên văn từ JD đó

Các JD:
{texts}"""


def extract_jd_batch_llm(texts: list[str], client=None, model: str | None = None,
                         taxonomy_path: Path = TAXONOMY_PATH) -> list[JDSchema]:
    """Gom N JD vào 1 LLM call (NIM free tier rat cham — goi le tung JD khong kha thi)."""
    from openai import OpenAI

    from app.config import settings

    client = client or OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    model = model or settings.llm_model
    canonical = _load_canonical_skills(taxonomy_path)
    joined = "\n\n".join(f"--- JD {i} ---\n{t[:MAX_JD_CHARS // 2]}" for i, t in enumerate(texts))
    payload = _BATCH_INSTRUCTION.format(canonical=", ".join(canonical), texts=joined)

    last_err: Exception | None = None
    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _LLM_SYSTEM},
                    {"role": "user", "content": payload},
                ],
                response_format={"type": "json_object"},
                temperature=0,
                timeout=300,
            )
            data = json.loads(resp.choices[0].message.content)
            valid = set(canonical)
            by_index = {}
            for item in data["results"]:
                r = JDSchema.model_validate(item)
                r.skills = sorted({s for s in r.skills if s in valid})
                by_index[item["index"]] = r
            if len(by_index) != len(texts):
                raise ValueError(f"Thieu ket qua: {len(by_index)}/{len(texts)} JD")
            return [by_index[i] for i in range(len(texts))]
        except (json.JSONDecodeError, ValidationError, KeyError, IndexError, ValueError) as e:
            last_err = e
            log.warning("LLM batch attempt %d failed: %s", attempt + 1, e)
    raise RuntimeError(f"LLM batch extraction failed after 2 attempts: {last_err}")


def extract_jd_rule(text: str, taxonomy_path: Path = TAXONOMY_PATH) -> JDSchema:
    return JDSchema(skills=_match_skills(text, taxonomy_path), years_required=None, evidence_snippet="")


def extract_jd(text: str, mode: str = "llm", **kwargs) -> JDSchema:
    """Điểm vào thống nhất. mode='llm' tự fallback về rule khi LLM lỗi."""
    if mode == "rule":
        return extract_jd_rule(text, kwargs.get("taxonomy_path", TAXONOMY_PATH))
    if mode == "llm":
        try:
            return extract_jd_llm(text, kwargs.get("client"), kwargs.get("model"),
                                   kwargs.get("taxonomy_path", TAXONOMY_PATH))
        except Exception as e:  # noqa: BLE001 — fallback boundary: moi loi LLM deu ve rule
            log.warning("LLM JD extraction unavailable, fallback to rule: %s", e)
            return extract_jd_rule(text, kwargs.get("taxonomy_path", TAXONOMY_PATH))
    raise ValueError(f"Unknown mode: {mode}")
