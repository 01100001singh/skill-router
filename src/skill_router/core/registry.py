"""Skill Registry - Thread-safe registry of available skills with embeddings."""

import threading
from pathlib import Path

import numpy as np
import yaml

from skill_router.core.types import Encoder, SkillEntry


class SkillRegistry:
    """Thread-safe registry of available skills with embeddings."""

    def __init__(
        self,
        skills_dir: Path | str,
        encoder: Encoder,
        auto_discover: bool = True
    ):
        """
        Initialize the skill registry.

        Args:
            skills_dir: Directory containing skill folders
            encoder: Embedding encoder instance
            auto_discover: Whether to auto-discover skills on init
        """
        self.skills_dir = Path(skills_dir)
        self.encoder = encoder
        self._skills: dict[str, SkillEntry] = {}
        self._embeddings: dict[str, np.ndarray] = {}
        self._lock = threading.RLock()

        if auto_discover:
            self.discover_skills()

    def discover_skills(self) -> int:
        """
        Discover and register all skills in the skills directory.

        Returns:
            Number of skills discovered
        """
        count = 0
        if not self.skills_dir.exists():
            return count

        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill_file = skill_path / "SKILL.md"
                if skill_file.exists():
                    try:
                        self.register_skill(skill_path)
                        count += 1
                    except Exception as e:
                        print(f"Warning: Failed to register skill at {skill_path}: {e}")

        return count

    def register_skill(self, skill_path: Path | str) -> SkillEntry:
        """
        Parse skill, generate utterances, compute embeddings.

        Args:
            skill_path: Path to skill directory containing SKILL.md

        Returns:
            The registered SkillEntry
        """
        skill_path = Path(skill_path)
        skill_file = skill_path / "SKILL.md"

        if not skill_file.exists():
            raise FileNotFoundError(f"SKILL.md not found at {skill_path}")

        with self._lock:
            frontmatter = self._parse_frontmatter(skill_file)
            utterances = self._generate_utterances(frontmatter)
            embeddings = self.encoder.encode(utterances)

            entry = SkillEntry(
                name=frontmatter["name"],
                description=frontmatter.get("description", ""),
                path=skill_path,
                utterances=utterances,
                metadata=frontmatter
            )

            self._skills[frontmatter["name"]] = entry
            self._embeddings[frontmatter["name"]] = self._mean_pool(embeddings)

            return entry

    def unregister_skill(self, name: str) -> bool:
        """Remove a skill from the registry."""
        with self._lock:
            if name in self._skills:
                del self._skills[name]
                del self._embeddings[name]
                return True
            return False

    def get_skill(self, name: str) -> SkillEntry | None:
        """Get a skill by name."""
        return self._skills.get(name)

    def list_skills(self) -> list[str]:
        """List all registered skill names."""
        return list(self._skills.keys())

    def find_similar(
        self,
        query_embedding: list[float] | np.ndarray,
        top_k: int = 5
    ) -> list[tuple[str, float]]:
        """
        Cosine similarity search across all skills.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return

        Returns:
            List of (skill_name, similarity_score) tuples
        """
        if not self._embeddings:
            return []

        query = np.array(query_embedding)
        query_norm = query / (np.linalg.norm(query) + 1e-10)

        similarities = []
        for name, embedding in self._embeddings.items():
            emb_norm = embedding / (np.linalg.norm(embedding) + 1e-10)
            similarity = float(np.dot(query_norm, emb_norm))
            similarities.append((name, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def _parse_frontmatter(self, skill_file: Path) -> dict:
        """Parse YAML frontmatter from SKILL.md file."""
        content = skill_file.read_text()

        if not content.startswith("---"):
            raise ValueError(f"SKILL.md must start with YAML frontmatter: {skill_file}")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Invalid frontmatter format in: {skill_file}")

        frontmatter = yaml.safe_load(parts[1])

        if "name" not in frontmatter:
            raise ValueError(f"Skill must have a 'name' field: {skill_file}")

        # Store the markdown body for reference
        frontmatter["_body"] = parts[2].strip()

        return frontmatter

    def _generate_utterances(self, frontmatter: dict) -> list[str]:
        """Generate utterances from skill metadata for embedding."""
        utterances = []

        # Add name and description
        utterances.append(frontmatter["name"])
        if "description" in frontmatter:
            utterances.append(frontmatter["description"])

        # Add explicit utterances if provided
        if "utterances" in frontmatter:
            utterances.extend(frontmatter["utterances"])

        # Add keywords if provided
        if "keywords" in frontmatter:
            utterances.extend(frontmatter["keywords"])

        # Generate from description if few utterances
        if len(utterances) < 5 and "description" in frontmatter:
            # Simple heuristic: split description into phrases
            desc = frontmatter["description"]
            phrases = [p.strip() for p in desc.replace(",", ".").split(".") if p.strip()]
            utterances.extend(phrases[:3])

        return utterances

    def _mean_pool(self, embeddings: list[list[float]]) -> np.ndarray:
        """Mean pool multiple embeddings into a single vector."""
        arr = np.array(embeddings)
        return np.mean(arr, axis=0)

    def __len__(self) -> int:
        return len(self._skills)

    def __contains__(self, name: str) -> bool:
        return name in self._skills
