"""DocIntel Core Configuration via Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with strict validation."""

    app_name: str = "DocIntel Backend"
    environment: str = Field(default="development", alias="ENV")
    debug: bool = Field(default=False, alias="DOCINTEL_DEBUG")
    port: int = 8000

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://docintel:docintel_secret_password@localhost:5436/docintel_db",
        alias="DATABASE_URL",
    )
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # ML & AI Keys
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")

    # Artifact Registry Paths
    model_artifact_path: str = "ml/artifacts/classification"
    faiss_index_path: str = "ml/artifacts/retrieval/corpus_faiss.index"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Observability
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
