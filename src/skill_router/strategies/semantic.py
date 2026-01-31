"""Semantic routing strategy using embedding similarity."""

from skill_router.core.registry import SkillRegistry
from skill_router.core.types import DispatchResult


class SemanticStrategy:
    """
    Pure semantic routing using embedding cosine similarity.

    Fast and deterministic - routes based solely on embedding distance.
    """

    def __init__(self, top_k: int = 5):
        """
        Initialize semantic strategy.

        Args:
            top_k: Number of alternatives to include in result
        """
        self.top_k = top_k

    def dispatch(self, query: str, registry: SkillRegistry) -> DispatchResult:
        """
        Route query to best matching skill via semantic similarity.

        Args:
            query: User query to route
            registry: Skill registry to search

        Returns:
            DispatchResult with selected skill
        """
        if len(registry) == 0:
            raise ValueError("No skills registered in registry")

        # Encode query
        query_embedding = registry.encoder.encode([query])[0]

        # Find similar skills
        similar = registry.find_similar(query_embedding, top_k=self.top_k)

        if not similar:
            raise ValueError("No similar skills found")

        best_name, best_score = similar[0]
        skill_entry = registry.get_skill(best_name)

        if skill_entry is None:
            raise ValueError(f"Skill {best_name} not found in registry")

        return DispatchResult(
            skill_name=best_name,
            skill_path=skill_entry.path,
            confidence=best_score,
            alternatives=similar[1:],
            routing_strategy="semantic",
            audit_trail={
                "query": query,
                "top_match": best_name,
                "top_score": best_score,
                "method": "cosine_similarity"
            }
        )
