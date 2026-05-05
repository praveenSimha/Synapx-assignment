import json
import requests
from .config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME


def normalize_response_content(content: str) -> str:
    if "```json" in content:
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in content:
        content = content.split("```", 1)[1].split("```", 1)[0].strip()
    return content.strip()


class OpenRouterClient:
    def __init__(self) -> None:
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.model_name = MODEL_NAME
        self.is_available = bool(self.api_key and "sk-or-v1" in self.api_key)

    def create_payload(self, prompt: str) -> dict:
        return {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
        }

    def request(self, prompt: str) -> str:
        if not self.is_available:
            raise RuntimeError("OpenRouter API key is missing or invalid.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            self.base_url,
            headers=headers,
            json=self.create_payload(prompt),
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        return normalize_response_content(content)
