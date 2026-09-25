"""Cấu hình ứng dụng, đọc từ biến môi trường / file .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/aitainang"

    # LLM cho Tầng 2 (extraction) — provider cụ thể chốt ở T2 theo API key hiện có.
    llm_provider: str = ""  # "openai" | "anthropic" | "google"
    llm_api_key: str = ""
    llm_model: str = ""


settings = Settings()
