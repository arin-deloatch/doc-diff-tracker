"""Configuration management for QA generation."""

from qa_generation.config.settings import (
    QAGenerationSettings,
    load_settings,
    load_settings_from_yaml,
)

__all__ = [
    "QAGenerationSettings",
    "load_settings",
    "load_settings_from_yaml",
]
