from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses .env file in backend/ or root directory.
    """
    # --- App ---
    app_name: str = "AI Content Agentic System"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = Field(default="change-this-in-production", env="SECRET_KEY")
    allowed_origins: str = Field(default="http://localhost:3000", env="ALLOWED_ORIGINS")

    # --- LLM Provider Selector ---
    # Giá trị hợp lệ: "openai" | "anthropic" | "ollama" | "mixed"
    # "mixed" = Ollama cho writing, OpenAI cho reasoning/vision (tiết kiệm chi phí)
    llm_provider: str = Field(default="ollama", env="LLM_PROVIDER")

    # --- OpenAI ---
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    openai_model_vision: str = Field(default="gpt-4o", env="OPENAI_MODEL_VISION")

    # --- Anthropic ---
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")

    # --- Ollama (Local) ---
    # Kết nối đến container Ollama tại D:\HUYTQ\docker-volumes\n8n-ollama
    # Nếu backend chạy NATIVE: dùng localhost:11434
    # Nếu backend chạy trong Docker (cùng n8n-network): dùng ollama:11434
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model_reasoning: str = Field(default="llama3.2", env="OLLAMA_MODEL_REASONING")
    ollama_model_writing: str = Field(default="llama3.2", env="OLLAMA_MODEL_WRITING")
    ollama_model_vision: str = Field(default="llava", env="OLLAMA_MODEL_VISION")

    # --- YouTube ---
    youtube_api_key: str = Field(default="", env="YOUTUBE_API_KEY")

    # --- Database ---
    database_url: str = Field(
        default="postgresql://content_agent:changeme@localhost:5432/content_machine",
        env="DATABASE_URL"
    )

    # --- ChromaDB ---
    chroma_host: str = Field(default="localhost", env="CHROMA_HOST")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT")

    # --- n8n ---
    # n8n đang chạy trong container n8n-ollama tại D:\HUYTQ\docker-volumes\n8n-ollama
    n8n_host: str = Field(default="localhost", env="N8N_HOST")
    n8n_port: int = Field(default=5678, env="N8N_PORT")

    # --- Knowledge System ---
    knowledge_base_path: str = Field(
        default="../knowledge",
        env="KNOWLEDGE_BASE_PATH"
    )

    @property
    def n8n_base_url(self) -> str:
        return f"http://{self.n8n_host}:{self.n8n_port}"

    @property
    def chroma_base_url(self) -> str:
        return f"http://{self.chroma_host}:{self.chroma_port}"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    model_config = {"env_file": ["../.env", ".env"], "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    """Cache settings instance — only reads .env once."""
    return Settings()
