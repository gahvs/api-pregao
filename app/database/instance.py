from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from environment.variables import POSTGRES_URL, POSTGRES_SCHEMA

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=MetaData(schema=POSTGRES_SCHEMA))

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()