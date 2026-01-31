"""Cohere encoder for embeddings."""

import os
from typing import Optional
from skill_router.encoders.base import BaseEncoder


class CohereEncoder(BaseEncoder):
    """
    Cohere encoder using embed-english-v3.0 by default.

    Provides high-quality embeddings via Cohere API.
    """

    DIMENSIONS = {
        "embed-english-v3.0": 1024,
        "embed-multilingual-v3.0": 1024,
        "embed-english-light-v3.0": 384,
        "embed-multilingual-light-v3.0": 384,
    }

    def __init__(
        self,
        model: str = "embed-english-v3.0",
        api_key: Optional[str] = None,
        input_type: str = "search_query"
    ):
        """
        Initialize the Cohere encoder.

        Args:
            model: Cohere embedding model name
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
            input_type: Type of input ('search_query', 'search_document', etc.)
        """
        try:
            import cohere
        except ImportError:
            raise ImportError(
                "cohere is required for CohereEncoder. "
                "Install with: pip install skill-router[cohere]"
            )

        self.model = model
        self.input_type = input_type
        self.client = cohere.Client(api_key=api_key or os.getenv("COHERE_API_KEY"))
        self._dimension = self.DIMENSIONS.get(model, 1024)

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts into embeddings."""
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=self.input_type
        )
        return response.embeddings

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimension
