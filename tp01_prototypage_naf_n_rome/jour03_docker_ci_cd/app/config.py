from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "NAF-ROME API"
    app_version: str = "1.0.0"
    debug: bool = False
    data_path: Path = Path("data/sample_naf_rome.csv")
    cors_origins: list[str] = ["*"]

    model_config = {"env_prefix": "APP_"}


settings = Settings()
