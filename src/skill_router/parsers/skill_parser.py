"""Skill file parser."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import yaml


@dataclass
class ParsedSkill:
    """Parsed skill data."""
    name: str
    description: str
    path: Path
    utterances: list[str]
    keywords: list[str]
    metadata: dict
    body: str


class SkillParser:
    """Parser for SKILL.md files."""

    def parse(self, skill_path: Path | str) -> ParsedSkill:
        """
        Parse a SKILL.md file.

        Args:
            skill_path: Path to skill directory or SKILL.md file

        Returns:
            ParsedSkill instance
        """
        skill_path = Path(skill_path)

        if skill_path.is_dir():
            skill_file = skill_path / "SKILL.md"
        else:
            skill_file = skill_path
            skill_path = skill_file.parent

        if not skill_file.exists():
            raise FileNotFoundError(f"SKILL.md not found: {skill_file}")

        content = skill_file.read_text()
        frontmatter, body = self._split_frontmatter(content)

        return ParsedSkill(
            name=frontmatter.get("name", skill_path.name),
            description=frontmatter.get("description", ""),
            path=skill_path,
            utterances=frontmatter.get("utterances", []),
            keywords=frontmatter.get("keywords", []),
            metadata=frontmatter,
            body=body
        )

    def _split_frontmatter(self, content: str) -> tuple[dict, str]:
        """Split YAML frontmatter from markdown body."""
        if not content.startswith("---"):
            return {}, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content

        frontmatter = yaml.safe_load(parts[1]) or {}
        body = parts[2].strip()

        return frontmatter, body

    def validate(self, skill_path: Path | str) -> list[str]:
        """
        Validate a skill file.

        Args:
            skill_path: Path to skill

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            parsed = self.parse(skill_path)

            if not parsed.name:
                errors.append("Skill must have a 'name' field")

            if not parsed.description:
                errors.append("Skill should have a 'description' field")

            if not parsed.utterances and not parsed.keywords:
                errors.append("Skill should have 'utterances' or 'keywords' for better routing")

        except FileNotFoundError as e:
            errors.append(str(e))
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML frontmatter: {e}")

        return errors
