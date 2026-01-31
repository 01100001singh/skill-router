"""Local encoder using sentence-transformers."""

from typing import Optional
from skill_router.encoders.base import BaseEncoder


class LocalEncoder(BaseEncoder):
    """
    Local encoder using sentence-transformers.

    Uses all-MiniLM-L6-v2 by default for fast, efficient embeddings.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize the local encoder.

        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu', 'cuda', etc.)
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for LocalEncoder. "
                "Install with: pip install skill-router[local]"
            )

        self.model = SentenceTransformer(model_name, device=device)
        self._dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts into embeddings."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimension
