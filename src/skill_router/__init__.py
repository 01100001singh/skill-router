"""
Skill Router - Runtime polymorphism for AI agent expertise.

Intelligent, embedding-based dispatch to modular AI skills.
"""

from skill_router.core.registry import SkillEntry, SkillRegistry
from skill_router.core.types import RoutingStrategy
from skill_router.core.vtable import DispatchResult, SkillVTable

__version__ = "0.1.0"

__all__ = [
    "SkillVTable",
    "DispatchResult",
    "SkillRegistry",
    "SkillEntry",
    "RoutingStrategy",
]
