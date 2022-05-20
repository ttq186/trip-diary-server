from sqlalchemy import create_engine

DB_URL = "dafj"

engine = create_engine(DB_URL)
SessionLocal = create_engine(autoflush=False, autoCommit=False, bind=engine)
