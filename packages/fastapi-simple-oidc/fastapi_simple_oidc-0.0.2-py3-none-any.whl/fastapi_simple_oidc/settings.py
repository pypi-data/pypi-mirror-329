from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SSOConfig(BaseModel):
    url: str | None = None
    id: str
    secret: str
    name: str | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='_'
    )

    sso: dict[str, SSOConfig] = {}
