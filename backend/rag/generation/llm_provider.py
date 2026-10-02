from abc import ABC, abstractmethod
from collections.abc import Iterator


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:
        pass

    def stream(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> Iterator[str]:
        raise NotImplementedError(
            "Streaming is not implemented by this provider."
        )