"""Hybrid routing strategy with LLM fallback."""

from collections.abc import Callable

from skill_router.core.registry import SkillRegistry
from skill_router.core.types import DispatchResult
from skill_router.strategies.semantic import SemanticStrategy


class HybridStrategy:
    """
    Semantic routing with LLM fallback for low-confidence cases.

    Uses fast semantic matching for high-confidence routes,
    falls back to LLM-based selection for ambiguous cases.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.85,
        llm_selector: Callable[[str, list[tuple[str, float]]], str] | None = None,
        top_k: int = 5
    ):
        """
        Initialize hybrid strategy.

        Args:
            confidence_threshold: Minimum confidence for semantic-only dispatch
            llm_selector: Optional LLM-based selector function
            top_k: Number of alternatives to consider
        """
        self.threshold = confidence_threshold
        self.llm_selector = llm_selector
        self.semantic = SemanticStrategy(top_k=top_k)
        self.top_k = top_k

    def dispatch(self, query: str, registry: SkillRegistry) -> DispatchResult:
        """
        Route query with optional LLM fallback.

        Args:
            query: User query to route
            registry: Skill registry to search

        Returns:
            DispatchResult with selected skill
        """
        # Try semantic routing first
        result = self.semantic.dispatch(query, registry)

        # If high confidence, return immediately
        if result.confidence >= self.threshold:
            result.audit_trail["fallback_used"] = False
            return result

        # If no LLM selector, return semantic result anyway
        if self.llm_selector is None:
            result.audit_trail["fallback_used"] = False
            result.audit_trail["below_threshold"] = True
            return result

        # Use LLM fallback for low-confidence cases
        return self._llm_fallback(query, registry, result)

    def _llm_fallback(
        self,
        query: str,
        registry: SkillRegistry,
        semantic_result: DispatchResult
    ) -> DispatchResult:
        """
        Use LLM to select skill from candidates.

        Args:
            query: Original query
            registry: Skill registry
            semantic_result: Result from semantic matching

        Returns:
            DispatchResult with LLM-selected skill
        """
        # Get all candidates
        candidates = [(semantic_result.skill_name, semantic_result.confidence)]
        candidates.extend(semantic_result.alternatives)

        # Call LLM selector
        selected_name = self.llm_selector(query, candidates)

        # Find selected skill
        skill_entry = registry.get_skill(selected_name)
        if skill_entry is None:
            # Fall back to semantic result if LLM returns invalid skill
            semantic_result.audit_trail["fallback_used"] = True
            semantic_result.audit_trail["llm_error"] = f"Invalid skill: {selected_name}"
            return semantic_result

        # Find confidence for selected skill
        confidence = next(
            (score for name, score in candidates if name == selected_name),
            0.0
        )

        return DispatchResult(
            skill_name=selected_name,
            skill_path=skill_entry.path,
            confidence=confidence,
            alternatives=[(n, s) for n, s in candidates if n != selected_name],
            routing_strategy="hybrid_llm",
            audit_trail={
                "query": query,
                "semantic_pick": semantic_result.skill_name,
                "semantic_confidence": semantic_result.confidence,
                "llm_pick": selected_name,
                "fallback_used": True
            }
        )
