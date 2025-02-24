from abc import ABC, abstractmethod
from typing import AsyncIterator

class Provider(ABC):
    @abstractmethod
    def invoke(self, prompt: str, attachment: str=None) -> AsyncIterator[str]:
        pass

