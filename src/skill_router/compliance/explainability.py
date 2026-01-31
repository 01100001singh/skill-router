"""Explainability reports for skill routing decisions."""

from dataclasses import dataclass
from skill_router.core.types import DispatchResult


@dataclass
class ExplainabilityReport:
    """
    Human-readable explanation of a routing decision.

    Designed for regulatory review and debugging.
    """

    query: str
    selected_skill: str
    confidence: float
    strategy: str
    reasoning: str
    alternatives: list[dict]
    audit_trail: dict

    @classmethod
    def from_dispatch_result(
        cls,
        query: str,
        result: DispatchResult,
        threshold: float = 0.85
    ) -> "ExplainabilityReport":
        """
        Create report from dispatch result.

        Args:
            query: Original query
            result: Dispatch result
            threshold: Confidence threshold used

        Returns:
            ExplainabilityReport instance
        """
        # Generate reasoning
        if result.confidence >= threshold:
            reasoning = (
                f"The query '{query}' was routed to skill '{result.skill_name}' "
                f"with {result.confidence:.1%} confidence using {result.routing_strategy} strategy. "
                f"This exceeded the confidence threshold of {threshold:.1%}."
            )
        else:
            reasoning = (
                f"The query '{query}' was routed to skill '{result.skill_name}' "
                f"with {result.confidence:.1%} confidence. "
                f"This was below the threshold of {threshold:.1%}, "
                f"so fallback strategies may have been employed."
            )

        if result.alternatives:
            alt_names = [name for name, _ in result.alternatives[:3]]
            reasoning += f" Alternative skills considered: {', '.join(alt_names)}."

        return cls(
            query=query,
            selected_skill=result.skill_name,
            confidence=result.confidence,
            strategy=result.routing_strategy,
            reasoning=reasoning,
            alternatives=[
                {"skill": name, "score": f"{score:.1%}"}
                for name, score in result.alternatives
            ],
            audit_trail=result.audit_trail
        )

    def to_markdown(self) -> str:
        """Generate markdown report."""
        md = f"""## Skill Routing Explanation

**Query**: {self.query}

**Selected Skill**: {self.selected_skill}

**Confidence**: {self.confidence:.1%}

**Strategy**: {self.strategy}

### Reasoning

{self.reasoning}

### Alternatives Considered

| Skill | Score |
|-------|-------|
"""
        for alt in self.alternatives:
            md += f"| {alt['skill']} | {alt['score']} |\n"

        md += "\n### Audit Trail\n\n```json\n"
        import json
        md += json.dumps(self.audit_trail, indent=2)
        md += "\n```\n"

        return md

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "selected_skill": self.selected_skill,
            "confidence": self.confidence,
            "strategy": self.strategy,
            "reasoning": self.reasoning,
            "alternatives": self.alternatives,
            "audit_trail": self.audit_trail
        }
