from typing import TypeVar
from koil.composition import Composition
from alpaka.vars import current_alpaka
import asyncio
from .ollama_client import OllamaClient
from .rath import AlpakaRath

T = TypeVar("T")


class Alpaka(Composition):
    rath: AlpakaRath
    ollama: OllamaClient
