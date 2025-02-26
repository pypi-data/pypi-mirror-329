from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    source_plugin: str
    destination_plugin: str
    interval_seconds: int


settings = Settings()  # type: ignore
