"""Rule-based routing strategy using regex/keyword matching."""

import re
from dataclasses import dataclass

from skill_router.core.registry import SkillRegistry
from skill_router.core.types import DispatchResult


@dataclass
class RoutingRule:
    """A routing rule with pattern and target skill."""
    pattern: str
    skill_name: str
    priority: int = 0
    case_sensitive: bool = False


class RuleBasedStrategy:
    """
    Rule-based routing using regex patterns.

    Useful for deterministic routing of known patterns,
    can be combined with semantic routing as a pre-filter.
    """

    def __init__(self, rules: list[RoutingRule] | None = None):
        """
        Initialize rule-based strategy.

        Args:
            rules: List of routing rules
        """
        self.rules = sorted(rules or [], key=lambda r: -r.priority)
        self._compiled: list[tuple[re.Pattern, str]] = []
        self._compile_rules()

    def _compile_rules(self) -> None:
        """Compile regex patterns for efficiency."""
        self._compiled = []
        for rule in self.rules:
            flags = 0 if rule.case_sensitive else re.IGNORECASE
            pattern = re.compile(rule.pattern, flags)
            self._compiled.append((pattern, rule.skill_name))

    def add_rule(self, rule: RoutingRule) -> None:
        """Add a routing rule."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -r.priority)
        self._compile_rules()

    def dispatch(self, query: str, registry: SkillRegistry) -> DispatchResult:
        """
        Route query using rule matching.

        Args:
            query: User query to route
            registry: Skill registry

        Returns:
            DispatchResult with matched skill

        Raises:
            ValueError: If no rule matches
        """
        for pattern, skill_name in self._compiled:
            if pattern.search(query):
                skill_entry = registry.get_skill(skill_name)

                if skill_entry is None:
                    continue  # Skip if skill not in registry

                return DispatchResult(
                    skill_name=skill_name,
                    skill_path=skill_entry.path,
                    confidence=1.0,  # Rule matches are deterministic
                    alternatives=[],
                    routing_strategy="rule_based",
                    audit_trail={
                        "query": query,
                        "matched_pattern": pattern.pattern,
                        "method": "regex_match"
                    }
                )

        raise ValueError(f"No rule matched for query: {query}")
