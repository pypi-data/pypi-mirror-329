from typing import TypeVar
from koil.composition.base import KoiledModel
from alpaka.vars import current_alpaka
import asyncio
from ollama import AsyncClient


T = TypeVar("T")


class OllamaClient(KoiledModel):
    endpoint_url: str
    _client: AsyncClient = None

    async def aconnect(self, **kwargs):
        self._client = AsyncClient(self.endpoint_url)

    async def chat(self, *args, **kwargs):
        if not self._client:
            await self.aconnect()

        return await self._client.chat(*args, **kwargs)

    async def pull(self, *args, **kwargs):
        if not self._client:
            await self.aconnect()

        return await self._client.pull(*args, **kwargs)

    async def __aenter__(self: T) -> T:
        current_alpaka.set(self)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await super().__aexit__(exc_type, exc_value, traceback)
        if self._client:
            print("Closing client???", self._client)
        current_alpaka.set(None)

    class Config:
        arbitrary_types_allowed = True
