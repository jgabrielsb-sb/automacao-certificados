from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Settings for the application.
    """
    groq_api_key: Optional[str] = None
    base_certificado_api_url: Optional[str] = None

    headless: bool
    run_cron_time: str
    run_with_cron: bool
    
    # ppe api
    base_ppe_api_url: str
    ppe_api_key: str

    # direct data api
    direct_data_api_key: str
    base_direct_data_api_url: str

    # receita api
    nota_facil_username: str
    nota_facil_password: str
    nota_facil_base_url: str

    ##### EMAIL SETTINGS #####
    email_host: str
    email_port: int
    is_tls: bool
    email_host_user: str
    email_host_password: str

    ####
    email_financeiro: str

    # ✅ new way to define config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
