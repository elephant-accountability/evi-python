"""Type definitions for the EVI Python reference implementation.

These dataclasses are the public interface. They are stable across minor
versions; breaking changes bump the major version.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Tier(str, Enum):
    """EVI tier outcomes."""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    NONE = "none"  # site is not certifiable


class AxisName(str, Enum):
    """The six axes in EVI v2."""

    DISCOVERABILITY = "discoverability"
    IDENTITY = "identity"
    AUTHORITY = "authority"
    COMMERCIAL_READABILITY = "commercial_readability"
    COMMERCE_PLUMBING = "commerce_plumbing"
    AGENT_PROTOCOL_SURFACE = "agent_protocol_surface"


class SurfaceStatus(str, Enum):
    """Detection result for a single surface."""

    PRESENT = "present"
    PARTIAL = "partial"
    ABSENT = "absent"
    ERROR = "error"  # detection failed; treated as absent for scoring


@dataclass(frozen=True)
class SurfaceDetection:
    """The result of detecting a single surface on the audited domain."""

    surface_id: str  # e.g. "S1", "S22"
    name: str  # human-readable name
    axis: AxisName
    status: SurfaceStatus
    score: int  # points contributed (0 ≤ score ≤ surface max)
    max_score: int
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AxisScore:
    """Per-axis aggregated score."""

    axis: AxisName
    score: int  # sum of surface scores in this axis
    max_score: int  # axis maximum (per spec)
    minimum_for_bronze: int | None = None
    minimum_for_silver: int | None = None
    minimum_for_gold: int | None = None


@dataclass(frozen=True)
class AutoFailCheck:
    """A single auto-fail condition check result."""

    name: str
    triggered: bool
    detail: str = ""


@dataclass(frozen=True)
class AuditResult:
    """The full result of an EVI audit run.

    Returned by ``evi.audit("example.com")``.
    """

    domain: str
    score: int  # overall 0-100
    tier: Tier
    axis_scores: dict[AxisName, AxisScore]
    surfaces: list[SurfaceDetection]
    auto_fail_checks: list[AutoFailCheck]
    methodology_version: str
    detection_run_id: str
    audited_at: datetime

    @property
    def axis_minimums_passed(self) -> bool:
        """True if all axis minimums for the issued tier are satisfied."""
        if self.tier == Tier.NONE:
            return False
        attr = {
            Tier.BRONZE: "minimum_for_bronze",
            Tier.SILVER: "minimum_for_silver",
            Tier.GOLD: "minimum_for_gold",
        }[self.tier]
        for axis_score in self.axis_scores.values():
            minimum = getattr(axis_score, attr)
            if minimum is not None and axis_score.score < minimum:
                return False
        return True

    @property
    def auto_fail_triggered(self) -> bool:
        """True if any auto-fail condition fired during this audit."""
        return any(check.triggered for check in self.auto_fail_checks)
