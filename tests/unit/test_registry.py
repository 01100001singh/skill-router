"""Tests for SkillRegistry."""

import pytest
from pathlib import Path
from skill_router.core.registry import SkillRegistry


class MockEncoder:
    """Mock encoder for testing."""

    def encode(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * 384 for _ in texts]

    @property
    def dimension(self) -> int:
        return 384


@pytest.fixture
def mock_encoder():
    return MockEncoder()


@pytest.fixture
def sample_skill(tmp_path):
    """Create a sample skill for testing."""
    skill_dir = tmp_path / "sample"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("""---
name: sample
description: A sample skill for testing
utterances:
  - "test query"
  - "sample request"
keywords:
  - test
  - sample
---

# Sample Skill

This is a sample skill.
""")
    return skill_dir


class TestSkillRegistry:
    """Tests for SkillRegistry class."""

    def test_register_skill(self, mock_encoder, sample_skill):
        """Test registering a skill."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder, auto_discover=False)
        entry = registry.register_skill(sample_skill)

        assert entry.name == "sample"
        assert entry.description == "A sample skill for testing"
        assert len(entry.utterances) > 0

    def test_discover_skills(self, mock_encoder, sample_skill):
        """Test auto-discovery of skills."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        assert "sample" in registry

    def test_get_skill(self, mock_encoder, sample_skill):
        """Test getting a skill by name."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        entry = registry.get_skill("sample")

        assert entry is not None
        assert entry.name == "sample"

    def test_list_skills(self, mock_encoder, sample_skill):
        """Test listing all skills."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        skills = registry.list_skills()

        assert "sample" in skills

    def test_find_similar(self, mock_encoder, sample_skill):
        """Test finding similar skills."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        query_embedding = mock_encoder.encode(["test query"])[0]

        similar = registry.find_similar(query_embedding)
        assert len(similar) > 0
        assert similar[0][0] == "sample"

    def test_unregister_skill(self, mock_encoder, sample_skill):
        """Test unregistering a skill."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        assert "sample" in registry

        result = registry.unregister_skill("sample")
        assert result is True
        assert "sample" not in registry

    def test_len(self, mock_encoder, sample_skill):
        """Test __len__ method."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        assert len(registry) == 1

    def test_contains(self, mock_encoder, sample_skill):
        """Test __contains__ method."""
        registry = SkillRegistry(sample_skill.parent, mock_encoder)
        assert "sample" in registry
        assert "nonexistent" not in registry
