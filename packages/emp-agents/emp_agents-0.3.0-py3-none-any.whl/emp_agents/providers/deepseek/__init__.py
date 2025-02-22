from typing import ClassVar

from pydantic import Field

from ..openai import OpenAIProvider
from .types import DeepSeekModelType


class DeepSeekProvider(OpenAIProvider):
    URL: ClassVar[str] = "https://api.deepseek.com/v1/chat/completions"

    default_model: DeepSeekModelType = Field(default=DeepSeekModelType.deepseek_chat)
