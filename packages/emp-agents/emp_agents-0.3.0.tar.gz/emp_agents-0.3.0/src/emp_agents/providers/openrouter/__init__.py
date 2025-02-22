import os
from typing import ClassVar

from pydantic import Field

from ..openai import OpenAIProvider
from .types import OpenRouterModelType


class OpenRouterProvider(OpenAIProvider):
    URL: ClassVar[str] = "https://openrouter.ai/api/v1/chat/completions"

    api_key: str = Field(default_factory=lambda: os.environ["OPENROUTER_API_KEY"])
    default_model: OpenRouterModelType = Field(default=OpenRouterModelType.gpt3_5_turbo)  # type: ignore
