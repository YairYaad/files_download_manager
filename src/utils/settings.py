from pydantic_settings import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    KAGGLE_API_TOKEN: str
    KAGGLE_DOWNLOAD_URL: str
    LOCAL_DOWNLOADS_LOCATION: str


settings = Settings()
