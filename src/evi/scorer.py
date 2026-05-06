"""EVI scorer entrypoint.

Pre-release scaffold. The ``audit`` function is the public API surface; its
implementation will be filled in for the v0.1.0 release on 2026-05-12.

The implementation will:

1. Resolve the canonical hostname (DNS + redirect resolution).
2. Run per-surface detectors (each detector lives in ``evi.detect.*``).
3. Aggregate per-axis scores.
4. Apply tier-eligibility logic per ``evi/spec/thresholds.md``.
5. Run auto-fail checks per the same spec.
6. Return an ``AuditResult``.

The scoring logic mirrors the canonical scorer in the Elephant Accountability
orchestrator (private repo). Spec changes land in the spec repo first; this
implementation follows.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from evi.types import (
    AuditResult,
    AutoFailCheck,
    AxisName,
    AxisScore,
    SurfaceDetection,
    Tier,
)

METHODOLOGY_VERSION = "evi-v2.0-draft"


def audit(domain: str, *, methodology_version: str = METHODOLOGY_VERSION) -> AuditResult:
    """Score a domain against EVI v2.

    Pre-release scaffold. Currently raises ``NotImplementedError``. The release
    on 2026-05-12 will return a populated ``AuditResult``.

    Args:
        domain: Bare hostname or full URL. Bare hostname recommended.
        methodology_version: Override the methodology version. Defaults to
            the latest spec this package targets.

    Returns:
        An ``AuditResult`` with overall score, tier, per-axis breakdown,
        per-surface detection results, and auto-fail check results.

    Raises:
        NotImplementedError: until v0.1.0 ships.
        ValueError: when ``domain`` is empty or malformed.
    """
    if not domain or not domain.strip():
        raise ValueError("domain must be a non-empty string")

    raise NotImplementedError(
        "evi-python is in pre-release. The scorer ships in v0.1.0 on 2026-05-12. "
        "For now, run scans at https://eaccountability.org/evi or use the orchestrator's "
        "internal scorer directly."
    )


def _empty_result(domain: str) -> AuditResult:
    """Return a zeroed AuditResult — used by tests, not by callers."""
    axes = {
        axis: AxisScore(
            axis=axis,
            score=0,
            max_score=_axis_max(axis),
            minimum_for_bronze=_axis_minimum(axis, Tier.BRONZE),
            minimum_for_silver=_axis_minimum(axis, Tier.SILVER),
            minimum_for_gold=_axis_minimum(axis, Tier.GOLD),
        )
        for axis in AxisName
    }
    return AuditResult(
        domain=domain,
        score=0,
        tier=Tier.NONE,
        axis_scores=axes,
        surfaces=[],
        auto_fail_checks=[],
        methodology_version=METHODOLOGY_VERSION,
        detection_run_id=str(uuid4()),
        audited_at=datetime.now(timezone.utc),
    )


def _axis_max(axis: AxisName) -> int:
    """Maximum points per axis (per evi-v2.md)."""
    return {
        AxisName.DISCOVERABILITY: 15,
        AxisName.IDENTITY: 15,
        AxisName.AUTHORITY: 15,
        AxisName.COMMERCIAL_READABILITY: 20,
        AxisName.COMMERCE_PLUMBING: 15,
        AxisName.AGENT_PROTOCOL_SURFACE: 20,
    }[axis]


def _axis_minimum(axis: AxisName, tier: Tier) -> int | None:
    """Per-axis minimums (per evi/spec/thresholds.md)."""
    table = {
        Tier.BRONZE: {
            AxisName.DISCOVERABILITY: 10,
            AxisName.IDENTITY: 8,
        },
        Tier.SILVER: {
            AxisName.DISCOVERABILITY: 12,
            AxisName.IDENTITY: 10,
            AxisName.AUTHORITY: 8,
            AxisName.COMMERCIAL_READABILITY: 12,
        },
        Tier.GOLD: {
            AxisName.DISCOVERABILITY: 13,
            AxisName.IDENTITY: 12,
            AxisName.AUTHORITY: 12,
            AxisName.COMMERCIAL_READABILITY: 16,
            AxisName.AGENT_PROTOCOL_SURFACE: 12,
        },
    }
    return table.get(tier, {}).get(axis)


__all__ = ["audit", "METHODOLOGY_VERSION"]
