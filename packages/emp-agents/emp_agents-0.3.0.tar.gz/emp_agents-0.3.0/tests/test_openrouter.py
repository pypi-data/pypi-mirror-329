import pytest

from emp_agents.agents import AgentBase
from emp_agents.providers import OpenRouterModelType, OpenRouterProvider


class AgentForTesting(AgentBase):
    description: str = "a simple agent for testing"
    prompt: str = (
        "Ignore the user questions and just respond with the text 'test complete' and nothing else"
    )


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.skip(
    reason="This test is disabled because it requires an OpenRouter API key"
)
async def test_basic_agent():
    agent = AgentForTesting(
        provider=OpenRouterProvider(
            default_model=OpenRouterModelType.gpt3_5_turbo,
        )
    )
    response = await agent.answer("what is the meaning of life?")
    assert response == "test complete"

    response = await agent.answer(
        "what is the meaning of life?",
        model=OpenRouterModelType.deepseek_r1_free,
    )
    assert response == "test complete"
