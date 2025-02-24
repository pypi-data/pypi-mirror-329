"""Settings for affect."""

from pathlib import Path

from pydantic_settings import BaseSettings

__all__ = ["settings"]


class PathSettings(BaseSettings):
    """Settings for the paths."""

    ROOT: Path = Path(__file__).parent.parent
    affect: Path = ROOT / "affect"


class Settings:
    """Settings for affect."""

    path: PathSettings = PathSettings()


settings = Settings()
