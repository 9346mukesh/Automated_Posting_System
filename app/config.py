
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str = ""

    bluesky_handle: str = ""
    bluesky_app_password: str = ""

    mastodon_instance_url: str = ""
    mastodon_access_token: str = ""

    telegram_bot_token: str = ""
    telegram_channel_id: str = ""
    telegram_channel_username: str = ""

    discord_webhook_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
