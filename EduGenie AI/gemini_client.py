from __future__ import annotations

import json
from typing import Any, Optional

from google import genai
from google.genai import types

from config import get_settings


class GeminiService:
    """
    Central service for Gemini API communication.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

        self.client: Optional[genai.Client] = None

        if self.settings.gemini_api_key:
            self.client = genai.Client(
                api_key=self.settings.gemini_api_key
            )

    def is_configured(self) -> bool:
        return self.client is not None

    def _require_client(self) -> genai.Client:
        if self.client is None:
            raise RuntimeError(
                "Gemini API key is not configured. "
                "Create a .env file and set GEMINI_API_KEY."
            )

        return self.client

    def generate_text(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        temperature: float = 0.3,
        max_output_tokens: int = 2048,
    ) -> str:
        """
        Generate normal text using Gemini.
        """

        client = self._require_client()

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
        )

        response = client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=config,
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    def generate_json(
        self,
        prompt: str,
        response_schema: Any,
        *,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 4096,
    ) -> Any:
        """
        Generate structured JSON using Gemini's response schema support.
        """

        client = self._require_client()

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
        )

        response = client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=config,
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty JSON response."
            )

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Gemini returned invalid JSON: {exc}"
            ) from exc


gemini_service = GeminiService()