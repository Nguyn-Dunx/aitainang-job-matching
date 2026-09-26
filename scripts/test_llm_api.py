"""Script kiểm tra kết nối API NVIDIA NIM (Kimi-K3 và Nemotron fallback)."""

import sys
from openai import OpenAI
from app.config import settings

def test_api():
    print(f"Base URL: {settings.llm_base_url}")
    print(f"Primary model: {settings.llm_model}")
    print(f"Fallback model: {settings.llm_fallback_model}")
    print(f"Key configured: {'Có' if settings.llm_api_key else 'Không'}")

    if not settings.llm_api_key:
        print("LỖI: Chưa có LLM_API_KEY trong .env")
        return

    client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)

    # 1. Test model chinh
    print(f"\n--- [1] Testing primary model: {settings.llm_model} ---")
    try:
        res = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": "Xin chao! Hay phan hoi 1 cau ngan xac nhan ket noi."}],
            max_tokens=60,
            temperature=0.2,
        )
        print("=> SUCCESS from primary model:")
        print(res.choices[0].message.content.encode('utf-8', errors='replace').decode('utf-8'))
    except Exception as e:
        print(f"=> ERROR primary: {e}")

    # 2. Test model fallback
    print(f"\n--- [2] Testing fallback model: {settings.llm_fallback_model} ---")
    try:
        res = client.chat.completions.create(
            model=settings.llm_fallback_model,
            messages=[{"role": "user", "content": "Xin chao! Hay phan hoi 1 cau ngan xac nhan ket noi."}],
            max_tokens=60,
            temperature=0.2,
        )
        print("=> SUCCESS fallback:")
        print(res.choices[0].message.content.encode('utf-8', errors='replace').decode('utf-8'))
    except Exception as e:
        print(f"=> ERROR fallback: {e}")

if __name__ == "__main__":
    test_api()
