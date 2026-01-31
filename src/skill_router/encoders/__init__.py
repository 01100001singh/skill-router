"""Embedding encoders for skill routing."""

from skill_router.encoders.base import BaseEncoder
from skill_router.encoders.local import LocalEncoder

__all__ = [
    "BaseEncoder",
    "LocalEncoder",
]

# Optional imports based on installed dependencies
try:
    from skill_router.encoders.openai import OpenAIEncoder
    __all__.append("OpenAIEncoder")
except ImportError:
    pass

try:
    from skill_router.encoders.cohere import CohereEncoder
    __all__.append("CohereEncoder")
except ImportError:
    pass

try:
    from skill_router.encoders.huggingface import HuggingFaceEncoder
    __all__.append("HuggingFaceEncoder")
except ImportError:
    pass
