import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

def get_db_url():

    if load_dotenv():
        # Getting Credentials
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        password = os.getenv("POSTGRES_PASS")
        user = os.getenv("POSTGRES_USER")
        database = os.getenv("POSTGRES_DATABASE")

        # Coding the password to URL-Safe
        password = quote_plus(password)

        # Build Postgres URL Connection
        url_connection = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        return url_connection

    return ""

def get_db_schema() -> str:

    if load_dotenv():
        schema = os.getenv("POSTGRES_SCHEMA")
        return schema

    return ""