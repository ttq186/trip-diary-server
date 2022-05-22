from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


    class Config:
        env_file = ".env"


settings = Settings()
