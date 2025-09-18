from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    backend_base_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///./newsbite.db"
    timezone: str = "Asia/Seoul"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # import side-effect로 로드

