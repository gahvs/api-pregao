import os
from dotenv import load_dotenv

PRODUCTION = "prod"

load_dotenv()

ENVIRONMENT = os.getenv("ENV")

def get_db_url():
    
    if ENVIRONMENT == "prod":
        return os.getenv("POSTGRES_PROD_URL")
    
    return os.getenv("POSTGRES_DEV_URL")

def get_db_schema():
    
    if ENVIRONMENT == "prod":
        return os.getenv("POSTGRES_PROD_SCHEMA")
    
    return os.getenv("POSTGRES_DEV_SCHEMA")