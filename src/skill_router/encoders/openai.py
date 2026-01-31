"""OpenAI encoder for embeddings."""

import os
from typing import Optional
from skill_router.encoders.base import BaseEncoder


class OpenAIEncoder(BaseEncoder):
    """
    OpenAI encoder using text-embedding-3-small by default.

    Provides high-quality embeddings via OpenAI API.
    """

    # Model dimensions
    DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        dimensions: Optional[int] = None
    ):
        """
        Initialize the OpenAI encoder.

        Args:
            model: OpenAI embedding model name
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            dimensions: Optional dimension override for text-embedding-3-* models
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai is required for OpenAIEncoder. "
                "Install with: pip install skill-router[openai]"
            )

        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._dimensions = dimensions or self.DIMENSIONS.get(model, 1536)

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts into embeddings."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimensions
