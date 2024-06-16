import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")