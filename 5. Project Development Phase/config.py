from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    gemini_api_key: str | None = None
    hf_token: str | None = None
    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-3.8-flash"
    image_provider: str = "hf_api"
    hf_image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"
    local_image_model: str = "runwayml/stable-diffusion-v1-5"
    panel_count: int = 5
    image_width: int = 768
    image_height: int = 768
    image_steps: int = 20
    max_story_prompt_chars: int = 2000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.panel_count = max(1, min(settings.panel_count, 8))
    return settings


settings = get_settings()
