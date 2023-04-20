from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import postgres_settings
import pandas as pd

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{postgres_settings.database_username}:{postgres_settings.database_password}@{postgres_settings.database_hostname}:{postgres_settings.postgres_database_port}/{postgres_settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

with SessionLocal() as session:
    df = pd.read_csv('../data/fraud.csv') 
    df.to_sql('transactions', con=engine, if_exists='append',index=False)