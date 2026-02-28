from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fastapi-enterprise-app"
    environment: str = "local"  # local, dev, qa, stage, prod
    log_level: str = "INFO"

    database_url: str = "postgresql://app:app@localhost:5432/app"

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")


settings = Settings()