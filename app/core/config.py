from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Summit Market API"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file = ".env"


settings = Settings()
