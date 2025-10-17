from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = Field("0.0.0.0", alias="HOST")
    port: int = Field(8002, alias="PORT")
    csv_path: str = Field("data/test.csv", alias="CSV_PATH")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5174"], alias="CORS_ORIGINS")

    openai_api_key: str | None = Field(None, alias="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4.1", alias="OPENAI_MODEL")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()