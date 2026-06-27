from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    API_SECRET: str  # Maps directly to your service_role key

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()