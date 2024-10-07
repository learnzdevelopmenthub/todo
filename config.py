import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    database_url = os.getenv("DATABASE_URL", "default_database_url")
    secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()