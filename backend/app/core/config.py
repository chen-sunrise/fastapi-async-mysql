from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str

    MONGO_DB_URI: str
    MONGO_DB_DATABASE: str
    MONGO_DB_USER_COLLECTION: str
    MONGO_DB_ITEM_COLLECTION: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60 * 60 * 30


settings = Settings()
