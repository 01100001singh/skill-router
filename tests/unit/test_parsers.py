"""Tests for skill parsers."""

import pytest
from pathlib import Path
from skill_router.parsers.skill_parser import SkillParser, ParsedSkill


@pytest.fixture
def parser():
    return SkillParser()


@pytest.fixture
def valid_skill(tmp_path):
    """Create a valid skill file."""
    skill_dir = tmp_path / "valid"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: valid-skill
description: A valid skill
utterances:
  - "query one"
  - "query two"
keywords:
  - key1
  - key2
custom_field: custom_value
---

# Valid Skill

This is the body content.
""")
    return skill_dir


@pytest.fixture
def minimal_skill(tmp_path):
    """Create a minimal skill file."""
    skill_dir = tmp_path / "minimal"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: minimal
---

# Minimal Skill
""")
    return skill_dir


class TestSkillParser:
    """Tests for SkillParser class."""

    def test_parse_valid_skill(self, parser, valid_skill):
        """Test parsing a valid skill."""
        parsed = parser.parse(valid_skill)

        assert parsed.name == "valid-skill"
        assert parsed.description == "A valid skill"
        assert "query one" in parsed.utterances
        assert "key1" in parsed.keywords
        assert parsed.metadata["custom_field"] == "custom_value"
        assert "Valid Skill" in parsed.body

    def test_parse_minimal_skill(self, parser, minimal_skill):
        """Test parsing a minimal skill."""
        parsed = parser.parse(minimal_skill)

        assert parsed.name == "minimal"
        assert parsed.description == ""
        assert parsed.utterances == []

    def test_parse_skill_file_directly(self, parser, valid_skill):
        """Test parsing SKILL.md file directly."""
        parsed = parser.parse(valid_skill / "SKILL.md")

        assert parsed.name == "valid-skill"

    def test_parse_missing_file(self, parser, tmp_path):
        """Test parsing non-existent skill."""
        with pytest.raises(FileNotFoundError):
            parser.parse(tmp_path / "nonexistent")

    def test_validate_valid_skill(self, parser, valid_skill):
        """Test validating a valid skill."""
        errors = parser.validate(valid_skill)
        assert len(errors) == 0

    def test_validate_minimal_skill(self, parser, minimal_skill):
        """Test validating a minimal skill."""
        errors = parser.validate(minimal_skill)
        # Should have warning about missing description
        assert any("description" in e.lower() for e in errors)

    def test_validate_missing_file(self, parser, tmp_path):
        """Test validating non-existent skill."""
        errors = parser.validate(tmp_path / "nonexistent")
        assert len(errors) > 0
