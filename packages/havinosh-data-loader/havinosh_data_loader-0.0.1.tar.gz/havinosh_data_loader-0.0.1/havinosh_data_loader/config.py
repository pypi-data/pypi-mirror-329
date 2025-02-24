import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "your_database"),
    "user": os.getenv("DB_USER", "your_username"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}
