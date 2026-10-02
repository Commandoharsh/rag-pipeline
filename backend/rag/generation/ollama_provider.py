import json

import requests

from backend.rag.generation.llm_provider import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str = "llama3.2",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            ""
        ).strip()

    def stream(
        self,
        prompt: str,
        system_prompt: str | None = None
    ):

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(
                line.decode("utf-8")
            )

            token = data.get("response", "")

            if token:
                yield token

            if data.get("done"):
                break