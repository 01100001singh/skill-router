"""Core routing components."""

from skill_router.core.vtable import SkillVTable, DispatchResult
from skill_router.core.registry import SkillRegistry, SkillEntry
from skill_router.core.types import RoutingStrategy

__all__ = [
    "SkillVTable",
    "DispatchResult",
    "SkillRegistry",
    "SkillEntry",
    "RoutingStrategy",
]
