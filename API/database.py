from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import postgres_settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{postgres_settings.database_username}:{postgres_settings.database_password}@{postgres_settings.database_hostname}:{postgres_settings.postgres_database_port}/{postgres_settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()