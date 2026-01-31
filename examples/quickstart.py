"""Quick start example for Skill Router."""

from pathlib import Path

# For this example, we'll use a mock encoder
# In production, use: from skill_router.encoders import OpenAIEncoder


class SimpleEncoder:
    """Simple encoder for demonstration."""

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Create simple embeddings based on text length and content."""
        embeddings = []
        for text in texts:
            # Simple heuristic embedding
            vec = [0.0] * 384
            vec[0] = len(text) / 100
            vec[1] = text.lower().count("pdf") / 10
            vec[2] = text.lower().count("word") / 10
            vec[3] = text.lower().count("docx") / 10
            vec[4] = text.lower().count("credit") / 10
            vec[5] = text.lower().count("loan") / 10
            embeddings.append(vec)
        return embeddings

    @property
    def dimension(self) -> int:
        return 384


def main():
    """Run quick start example."""
    from skill_router import SkillVTable
    from skill_router.strategies import HybridStrategy

    # Path to example skills
    skills_dir = Path(__file__).parent.parent / "skills" / "examples"

    # Initialize router
    vtable = SkillVTable(
        skills_dir=skills_dir,
        encoder=SimpleEncoder(),
        strategy=HybridStrategy(confidence_threshold=0.85)
    )

    print(f"Loaded {len(vtable.registry)} skills: {vtable.list_skills()}")
    print()

    # Test queries
    queries = [
        "Extract tables from financial_report.pdf",
        "Read the Word document",
        "Evaluate this loan application",
    ]

    for query in queries:
        result = vtable.dispatch(query)
        print(f"Query: {query}")
        print(f"  -> Skill: {result.skill_name}")
        print(f"  -> Confidence: {result.confidence:.2%}")
        print(f"  -> Strategy: {result.routing_strategy}")
        print()

    # Get explanation
    print("=== Detailed Explanation ===")
    explanation = vtable.explain(queries[0])
    print(f"Query: {explanation['query']}")
    print(f"Selected: {explanation['selected_skill']}")
    print(f"Confidence: {explanation['confidence']:.2%}")
    print("Alternatives:")
    for alt in explanation["alternatives"]:
        print(f"  - {alt['skill']}: {alt['score']:.2%}")


if __name__ == "__main__":
    main()
