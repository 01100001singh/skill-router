"""Core routing components."""

from skill_router.core.registry import SkillEntry, SkillRegistry
from skill_router.core.types import RoutingStrategy
from skill_router.core.vtable import DispatchResult, SkillVTable

__all__ = [
    "SkillVTable",
    "DispatchResult",
    "SkillRegistry",
    "SkillEntry",
    "RoutingStrategy",
]
