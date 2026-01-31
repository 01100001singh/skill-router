"""
Skill Router - Runtime polymorphism for AI agent expertise.

Intelligent, embedding-based dispatch to modular AI skills.
"""

from skill_router.core.vtable import SkillVTable, DispatchResult
from skill_router.core.registry import SkillRegistry, SkillEntry
from skill_router.core.types import RoutingStrategy

__version__ = "0.1.0"

__all__ = [
    "SkillVTable",
    "DispatchResult",
    "SkillRegistry",
    "SkillEntry",
    "RoutingStrategy",
]
