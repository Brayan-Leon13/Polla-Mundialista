from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./polla.db"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    admin_email: str = "admin@pollamundialista.com"
    admin_password: str = "Admin123!"

    class Config:
        env_file = ".env"


settings = Settings()
