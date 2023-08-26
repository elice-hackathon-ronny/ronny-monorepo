from dotenv import find_dotenv, load_dotenv
from os import environ
from google.cloud import secretmanager

load_dotenv(find_dotenv('.env'))


def get_gcp_secret(key: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/elice-hackathon/secrets/{key}/versions/1"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload


def mongo_db_url() -> str:
    env_value = environ.get("MONGO_DB_URL")
    if env_value:
        return env_value

    return get_gcp_secret("MONGO_DB_URL")


def mongo_db_database() -> str:
    return "database"


def open_ai_api_key() -> str:
    env_value = environ.get("OPEN_AI_API_KEY")
    if env_value:
        return env_value

    return get_gcp_secret("OPEN_AI_API_KEY")
