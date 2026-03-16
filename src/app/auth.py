from src.utils.settings import settings


def get_kaggle_auth_header() -> dict:

    return {
        "Authorization": f"Bearer {settings.KAGGLE_API_TOKEN}",
        "Accept": "application/json"
    }
