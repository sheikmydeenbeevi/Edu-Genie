from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables and the .env file.
    """

    app_name: str = Field(default="EduGenie", validation_alias="APP_NAME")
    app_version: str = Field(default="1.0.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=True, validation_alias="DEBUG")

    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias="GEMINI_MODEL",
    )

    use_local_explainer: bool = Field(
        default=False,
        validation_alias="USE_LOCAL_EXPLAINER",
    )

    local_explainer_model: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M",
        validation_alias="LOCAL_EXPLAINER_MODEL",
    )

    max_input_length: int = Field(
        default=20000,
        validation_alias="MAX_INPUT_LENGTH",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()