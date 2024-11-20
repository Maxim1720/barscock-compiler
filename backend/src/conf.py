from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    
    OUT_DIR: str
    RES_DIR: str
    
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        #env_nested_delimiter="__",
        env_file_encoding="utf-8",
    )
    #model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_global_config():
    s = Settings()
    return s
