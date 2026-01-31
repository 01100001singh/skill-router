"""Type definitions for Skill Router."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable
from datetime import datetime


@dataclass
class DispatchResult:
    """Result of skill routing decision."""

    skill_name: str
    skill_path: Path
    confidence: float
    alternatives: list[tuple[str, float]]
    routing_strategy: str
    audit_trail: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Add timestamp to audit trail."""
        if "timestamp" not in self.audit_trail:
            self.audit_trail["timestamp"] = datetime.utcnow().isoformat()
        self.audit_trail["skill_name"] = self.skill_name
        self.audit_trail["confidence"] = self.confidence
        self.audit_trail["strategy"] = self.routing_strategy


@dataclass
class SkillEntry:
    """Registry entry for a skill."""

    name: str
    description: str
    path: Path
    utterances: list[str]
    metadata: dict = field(default_factory=dict)


@runtime_checkable
class RoutingStrategy(Protocol):
    """Interface for routing strategies - enables polymorphism."""

    def dispatch(
        self,
        query: str,
        registry: "SkillRegistry"  # type: ignore
    ) -> DispatchResult:
        """Route a query to the best matching skill."""
        ...


@runtime_checkable
class Encoder(Protocol):
    """Interface for embedding encoders."""

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Encode texts into embeddings."""
        ...

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        ...
