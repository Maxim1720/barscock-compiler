from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ROOT_DIR: str = Field(alias="root_dir")

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

print(f"Using .env file at: {Config.model_config}")