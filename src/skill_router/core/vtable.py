"""Skill VTable - Main dispatch logic for skill routing."""

from pathlib import Path

from skill_router.core.registry import SkillRegistry
from skill_router.core.types import DispatchResult, Encoder, RoutingStrategy


class SkillVTable:
    """
    Virtual table for skill dispatch.

    Routes queries to the most appropriate skill using embedding-based
    similarity matching with optional fallback strategies.
    """

    strategy: RoutingStrategy

    def __init__(
        self,
        skills_dir: Path | str,
        encoder: Encoder,
        strategy: RoutingStrategy | None = None,
        confidence_threshold: float = 0.85
    ):
        """
        Initialize the Skill VTable.

        Args:
            skills_dir: Directory containing skill folders
            encoder: Embedding encoder instance
            strategy: Routing strategy (defaults to HybridStrategy)
            confidence_threshold: Minimum confidence for direct dispatch
        """
        self.skills_dir = Path(skills_dir)
        self.encoder = encoder
        self.confidence_threshold = confidence_threshold
        self.registry = SkillRegistry(skills_dir, encoder)

        # Import here to avoid circular dependency
        if strategy is None:
            from skill_router.strategies import HybridStrategy
            self.strategy = HybridStrategy(confidence_threshold)
        else:
            self.strategy = strategy

    def dispatch(self, query: str) -> DispatchResult:
        """
        Route a query to the best matching skill.

        Args:
            query: User query/request to route

        Returns:
            DispatchResult with selected skill and metadata
        """
        return self.strategy.dispatch(query, self.registry)

    def dispatch_with_content(self, query: str) -> tuple[DispatchResult, str]:
        """
        Route query and return skill content.

        Args:
            query: User query/request to route

        Returns:
            Tuple of (DispatchResult, skill_content)
        """
        result = self.dispatch(query)
        skill_file = result.skill_path / "SKILL.md"
        content = skill_file.read_text() if skill_file.exists() else ""
        return result, content

    def add_skill(self, skill_path: Path | str) -> None:
        """Register a new skill at runtime."""
        self.registry.register_skill(skill_path)

    def remove_skill(self, name: str) -> bool:
        """Remove a skill from the registry."""
        return self.registry.unregister_skill(name)

    def list_skills(self) -> list[str]:
        """List all registered skills."""
        return self.registry.list_skills()

    def get_skill_content(self, name: str) -> str | None:
        """Get the content of a skill by name."""
        entry = self.registry.get_skill(name)
        if entry:
            skill_file = entry.path / "SKILL.md"
            if skill_file.exists():
                return skill_file.read_text()
        return None

    def explain(self, query: str) -> dict:
        """
        Explain why a particular skill was selected.

        Args:
            query: The query to explain routing for

        Returns:
            Dictionary with explanation details
        """
        result = self.dispatch(query)

        return {
            "query": query,
            "selected_skill": result.skill_name,
            "confidence": result.confidence,
            "threshold": self.confidence_threshold,
            "above_threshold": result.confidence >= self.confidence_threshold,
            "strategy_used": result.routing_strategy,
            "alternatives": [
                {"skill": name, "score": score}
                for name, score in result.alternatives
            ],
            "audit_trail": result.audit_trail
        }

    def __repr__(self) -> str:
        return (
            f"SkillVTable(skills={len(self.registry)}, "
            f"threshold={self.confidence_threshold})"
        )
