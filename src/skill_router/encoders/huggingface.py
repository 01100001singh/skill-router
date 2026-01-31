"""HuggingFace encoder for embeddings."""

from typing import Optional
from skill_router.encoders.base import BaseEncoder


class HuggingFaceEncoder(BaseEncoder):
    """
    HuggingFace encoder using sentence-transformers models.

    Supports any model from the HuggingFace Hub compatible with
    sentence-transformers.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-mpnet-base-v2",
        device: Optional[str] = None,
        normalize_embeddings: bool = True
    ):
        """
        Initialize the HuggingFace encoder.

        Args:
            model_name: HuggingFace model name or path
            device: Device to run on ('cpu', 'cuda', etc.)
            normalize_embeddings: Whether to L2-normalize embeddings
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for HuggingFaceEncoder. "
                "Install with: pip install skill-router[huggingface]"
            )

        self.model = SentenceTransformer(model_name, device=device)
        self.normalize = normalize_embeddings
        self._dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts into embeddings."""
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize
        )
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimension
