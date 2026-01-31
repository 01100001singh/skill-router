"""Claude Code integration for skill routing."""

from pathlib import Path
from typing import Optional
from skill_router.core.vtable import SkillVTable
from skill_router.core.types import DispatchResult


class ClaudeCodeIntegration:
    """
    Integration layer for Claude Code.

    Provides skill routing for Claude Code agents and skills.
    """

    def __init__(
        self,
        vtable: SkillVTable,
        skills_base_path: Optional[Path] = None
    ):
        """
        Initialize Claude Code integration.

        Args:
            vtable: Skill VTable instance
            skills_base_path: Base path for .claude/skills directory
        """
        self.vtable = vtable
        self.skills_base_path = skills_base_path or Path(".claude/skills")

    def route_request(self, user_request: str) -> tuple[DispatchResult, str]:
        """
        Route a user request to the appropriate skill.

        Args:
            user_request: The user's request/query

        Returns:
            Tuple of (DispatchResult, skill_content)
        """
        return self.vtable.dispatch_with_content(user_request)

    def format_for_context(self, result: DispatchResult, content: str) -> str:
        """
        Format skill for injection into Claude context.

        Args:
            result: Dispatch result
            content: Skill content

        Returns:
            Formatted string for context injection
        """
        return f"""<skill name="{result.skill_name}" confidence="{result.confidence:.2f}">
{content}
</skill>"""

    def get_routing_explanation(self, user_request: str) -> str:
        """
        Get human-readable explanation of routing decision.

        Args:
            user_request: The user's request

        Returns:
            Markdown explanation
        """
        explanation = self.vtable.explain(user_request)

        md = f"""## Skill Routing Decision

**Query**: {explanation['query']}
**Selected**: {explanation['selected_skill']} ({explanation['confidence']:.1%} confidence)
**Strategy**: {explanation['strategy_used']}

### Alternatives
"""
        for alt in explanation['alternatives']:
            md += f"- {alt['skill']}: {alt['score']:.1%}\n"

        return md

    def discover_claude_skills(self, project_root: Path) -> int:
        """
        Discover skills from Claude Code project structure.

        Args:
            project_root: Root of the project

        Returns:
            Number of skills discovered
        """
        skills_dir = project_root / ".claude" / "skills"
        if not skills_dir.exists():
            return 0

        count = 0
        for skill_path in skills_dir.iterdir():
            if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
                try:
                    self.vtable.add_skill(skill_path)
                    count += 1
                except Exception:
                    pass

        return count
