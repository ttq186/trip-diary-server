from pydantic import BaseSettings


class Settings(BaseSettings):
    ROOT_PATH: str = ""
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SENDGRID_FROM_EMAIL: str
    SENDGRID_TEMPLATE_ID: str
    SENDGRID_API_KEY: str
    PASSWORD_RESET_BASE_URL: str = "http://localhost:3000"
    EMAIL_VERIFIER_API_KEY: str
    GOOGLE_CLIENT_ID: str
    AZURE_STORAGE_ACCOUNT_NAME: str
    AZURE_CONTAINER_NAME: str
    AZURE_ACCESS_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
