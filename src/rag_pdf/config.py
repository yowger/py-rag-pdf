from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    # API keys
    openai_api_key: str

    # LLM models
    intent_model: str = "gpt-4o-mini"
    answer_model: str = "gpt-4o-mini"
    query_rewrite_model: str = "gpt-4o-mini"

    # Embedding model
    embedding_model: str = "text-embedding-3-small"

    # Retrieval configuration
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4

    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "rag-pdf"

    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    rate_limit: str = "20/minute"
    cache_ttl_seconds: int = 300
    max_retries: int = 3

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance - loaded once, reused everywhere."""
    return Settings()
