from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./secr_online.db"
    secret_key: str = "CHANGE_THIS_SECRET_KEY"
    access_token_expire_minutes: int = 480
    admin_hrms_id: str = "ADMIN001"
    admin_password: str = "ChangeMe123!"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
