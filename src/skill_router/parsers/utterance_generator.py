"""Utterance generation from skill metadata."""

from typing import Optional, Callable


class UtteranceGenerator:
    """
    Generate utterances from skill descriptions.

    Can use LLM for higher quality utterance generation.
    """

    def __init__(
        self,
        llm_generator: Optional[Callable[[str], list[str]]] = None,
        min_utterances: int = 5
    ):
        """
        Initialize utterance generator.

        Args:
            llm_generator: Optional LLM function for generating utterances
            min_utterances: Minimum utterances to generate
        """
        self.llm_generator = llm_generator
        self.min_utterances = min_utterances

    def generate(
        self,
        name: str,
        description: str,
        keywords: Optional[list[str]] = None
    ) -> list[str]:
        """
        Generate utterances from skill metadata.

        Args:
            name: Skill name
            description: Skill description
            keywords: Optional keywords

        Returns:
            List of utterances
        """
        utterances = [name]

        if description:
            utterances.append(description)

        if keywords:
            utterances.extend(keywords)

        # Use LLM if available and need more utterances
        if self.llm_generator and len(utterances) < self.min_utterances:
            prompt = self._build_prompt(name, description)
            generated = self.llm_generator(prompt)
            utterances.extend(generated)

        # Fall back to heuristic generation
        if len(utterances) < self.min_utterances:
            utterances.extend(self._heuristic_generate(name, description))

        return list(set(utterances))  # Deduplicate

    def _build_prompt(self, name: str, description: str) -> str:
        """Build LLM prompt for utterance generation."""
        return f"""Generate 5 different ways a user might ask for the "{name}" skill.

Skill description: {description}

Examples should be natural user queries that would invoke this skill.
Return only the queries, one per line."""

    def _heuristic_generate(self, name: str, description: str) -> list[str]:
        """Generate utterances using simple heuristics."""
        utterances = []

        # Action phrases
        actions = ["help me", "I need to", "can you", "please", "I want to"]
        for action in actions[:3]:
            utterances.append(f"{action} {name}")

        # Split description into phrases
        if description:
            phrases = [
                p.strip()
                for p in description.replace(",", ".").split(".")
                if p.strip() and len(p.strip()) > 10
            ]
            utterances.extend(phrases[:3])

        return utterances
