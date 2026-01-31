"""Tests for SkillVTable."""

import pytest
from pathlib import Path
from unittest.mock import Mock
from skill_router.core.vtable import SkillVTable
from skill_router.core.registry import SkillRegistry


class MockEncoder:
    """Mock encoder for testing."""

    def __init__(self, dimension: int = 384):
        self._dimension = dimension

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Return mock embeddings."""
        return [[0.1] * self._dimension for _ in texts]

    @property
    def dimension(self) -> int:
        return self._dimension


@pytest.fixture
def mock_encoder():
    return MockEncoder()


@pytest.fixture
def temp_skills_dir(tmp_path):
    """Create temporary skills directory with test skills."""
    # Create PDF skill
    pdf_dir = tmp_path / "pdf"
    pdf_dir.mkdir()
    (pdf_dir / "SKILL.md").write_text("""---
name: pdf
description: Extract text from PDF files
utterances:
  - "read PDF"
  - "extract PDF text"
---

# PDF Skill
""")

    # Create DOCX skill
    docx_dir = tmp_path / "docx"
    docx_dir.mkdir()
    (docx_dir / "SKILL.md").write_text("""---
name: docx
description: Process Word documents
utterances:
  - "read Word file"
  - "parse docx"
---

# DOCX Skill
""")

    return tmp_path


class TestSkillVTable:
    """Tests for SkillVTable class."""

    def test_init_discovers_skills(self, temp_skills_dir, mock_encoder):
        """Test that VTable discovers skills on init."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        assert len(vtable.registry) == 2
        assert "pdf" in vtable.list_skills()
        assert "docx" in vtable.list_skills()

    def test_dispatch_returns_result(self, temp_skills_dir, mock_encoder):
        """Test dispatch returns a DispatchResult."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        result = vtable.dispatch("extract text from PDF file")

        assert result.skill_name in ["pdf", "docx"]
        assert 0 <= result.confidence <= 1
        assert result.routing_strategy is not None

    def test_dispatch_with_content(self, temp_skills_dir, mock_encoder):
        """Test dispatch_with_content returns skill content."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        result, content = vtable.dispatch_with_content("read PDF")

        assert result.skill_name is not None
        assert "SKILL" in content or "Skill" in content

    def test_add_skill(self, temp_skills_dir, mock_encoder, tmp_path):
        """Test adding skill at runtime."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        initial_count = len(vtable.registry)

        # Create new skill
        new_skill = tmp_path / "new_skill"
        new_skill.mkdir()
        (new_skill / "SKILL.md").write_text("""---
name: new-skill
description: A new skill
---
# New Skill
""")

        vtable.add_skill(new_skill)
        assert len(vtable.registry) == initial_count + 1

    def test_remove_skill(self, temp_skills_dir, mock_encoder):
        """Test removing skill."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        initial_count = len(vtable.registry)

        result = vtable.remove_skill("pdf")
        assert result is True
        assert len(vtable.registry) == initial_count - 1

    def test_explain(self, temp_skills_dir, mock_encoder):
        """Test explain method."""
        vtable = SkillVTable(temp_skills_dir, mock_encoder)
        explanation = vtable.explain("read PDF file")

        assert "query" in explanation
        assert "selected_skill" in explanation
        assert "confidence" in explanation
        assert "alternatives" in explanation
