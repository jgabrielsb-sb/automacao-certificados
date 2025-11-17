from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings for the application.
    """
    groq_api_key: Optional[str] = None
    base_certificado_api_url: Optional[str] = None

    # ppe api
    base_ppe_api_url: str
    ppe_api_key: str

    # ✅ new way to define config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
