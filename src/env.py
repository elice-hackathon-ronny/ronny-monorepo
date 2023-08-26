from dotenv import find_dotenv, load_dotenv
from os import environ

load_dotenv(find_dotenv('.env'))


def mongo_db_url() -> str:
    return environ.get('MONGO_DB_URL')


def mongo_db_database() -> str:
    return "database"


OPEN_AI_API_KEY = environ.get("OPEN_AI_API_KEY")
