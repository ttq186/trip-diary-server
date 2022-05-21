from sqlalchemy import create_engine

from core import settings

DB_URL = (
    f"postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DB_URL)
SessionLocal = create_engine(autoflush=False, autoCommit=False, bind=engine)
