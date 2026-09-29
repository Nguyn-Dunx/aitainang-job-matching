"""Cấu hình ứng dụng, đọc từ biến môi trường / file .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/aitainang"

    # LLM cho Tầng 2 & Tầng 5 — Mặc định dùng NVIDIA NIM (Kimi-K3 + Nemotron fallback)
    llm_provider: str = "openai"  # OpenAI client tương thích NVIDIA NIM
    llm_base_url: str = "https://integrate.api.nvidia.com/v1"
    llm_api_key: str = ""
    llm_model: str = "moonshotai/kimi-k3"
    llm_fallback_model: str = "nvidia/nemotron-3-ultra-550b-a55b"
    llm_timeout_s: int = 30  # timeout moi lan goi LLM; chuoi retry Tầng 5 toi da 2 lan = ~60s


settings = Settings()
