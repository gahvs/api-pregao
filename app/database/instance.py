from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from environment.variables import get_db_url, get_db_schema

print(get_db_url())
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=MetaData(schema=get_db_schema()))

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()