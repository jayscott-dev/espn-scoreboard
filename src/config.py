from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    espn_user_agent: str = "espn-scoreboard-learning-script/1.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
