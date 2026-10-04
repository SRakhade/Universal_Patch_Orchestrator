from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="UPO_", extra="ignore")
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://upo:changeme@postgres:5432/upo"
    redis_url: str = "redis://redis:6379/0"
    bigfix_base_url: str = "https://bigfix.example.com:52311"
    bigfix_username: str = ""
    bigfix_password: str = ""
    bigfix_verify_tls: bool = True

settings = Settings()
