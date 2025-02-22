from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from emp_agents.models.shared.message import Message
from emp_agents.models.shared.tools import GenericTool


class Request(BaseModel):
    """
    https://platform.openai.com/docs/api-reference/chat/create
    """

    model_config = ConfigDict(populate_by_name=True)

    model: str
    max_tokens: Optional[int] = Field(default=4096, lt=128_000, gt=0)
    temperature: Optional[float] = Field(default=None, ge=0, le=2.0)
    tool_choice: Literal["none", "required", "auto", None] = Field(default=None)
    tools: Optional[list[GenericTool]] = None
    response_format: type[BaseModel] | None = None

    system: str | None = None  # anthropic field
    messages: list[Message]

    frequency_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)  # openai
    presence_penalty: Optional[float] = Field(default=None, ge=-2.0, le=2.0)  # openai
    num_responses: Optional[int] = Field(
        default=None, serialization_alias="n"
    )  # openai
    top_p: Optional[int] = Field(default=None)  # openai

    def model_dump(self, *, exclude_none=True, by_alias=True, **kwargs):
        return super().model_dump(
            exclude_none=exclude_none, by_alias=by_alias, **kwargs
        )
