"""Base encoder interface."""

from abc import ABC, abstractmethod


class BaseEncoder(ABC):
    """Abstract base class for embedding encoders."""

    @abstractmethod
    def encode(self, texts: list[str]) -> list[list[float]]:
        """
        Encode texts into embeddings.

        Args:
            texts: List of texts to encode

        Returns:
            List of embedding vectors
        """
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension."""
        ...

    def encode_single(self, text: str) -> list[float]:
        """Encode a single text."""
        return self.encode([text])[0]
