import os
from typing import ClassVar

import httpx
from pydantic import Field

from ._type import Rag


class Ragie(Rag):
    name: str = "Ragie Middleware"
    description: str = (
        "This middleware uses the Ragie API to retrieve context from relevant datasources."
    )
    BASE_URL: ClassVar[str] = "https://api.ragie.ai"

    api_key: str | None = Field(
        default_factory=lambda: os.environ.get("RAGIE_API_KEY"),
        description="The API key for the Ragie API",
    )
    partition: str | None = Field(
        default=None, description="The partition to use for the Ragie API"
    )
    num_chunks: int = Field(1, description="The number of chunks to retrieve")

    async def get_context(self, query: str) -> str:
        context = await self.retrieve(query)
        chunks = context["scored_chunks"]
        if len(chunks) == 0:
            return ""

        data = "\n-------\n".join(c["text"] for c in chunks[: self.num_chunks])
        return data

    async def retrieve(self, query: str):
        payload = {"query": query}

        if self.partition:
            payload["partition"] = self.partition

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._build_url("retrievals"),
                json=payload,
                headers=self._make_headers(),
            )

        return response.json()

    def _make_headers(self, content_type: str = "application/json"):
        headers = {
            "accept": "application/json",
            "content-type": content_type,
            "authorization": f"Bearer {self.api_key}",
        }
        if self.partition:
            headers["partition"] = self.partition
        return headers

    def _build_url(self, path: str):
        return f"{self.BASE_URL}/{path}"
