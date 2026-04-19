from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "NAF-ROME API"
    app_version: str = "1.0.0"
    debug: bool = False
    data_naf_path: Path = Path("data/naf_codes_001_desc.csv")
    data_rome_path: Path = Path("data/rome.csv")
    data_matching_path: Path = Path("data/rome_with_naf__thenlper_gte-large.csv")
    cors_origins: list[str] = ["*"]

    model_config = {"env_prefix": "APP_"}


settings = Settings()
