"""Smoke tests for the evi scorer scaffold.

These tests verify the scaffold behaves correctly while the scorer itself is
not yet implemented. When v0.1.0 implements the scorer, these tests are
augmented with real scoring assertions; the pre-release behavior tests remain
to lock in the public-API contract.
"""

from __future__ import annotations

import pytest

from evi import AuditResult, AxisScore, SurfaceDetection, Tier, audit
from evi.scorer import _empty_result, _axis_max, _axis_minimum
from evi.types import AxisName


def test_audit_raises_not_implemented_for_now():
    """Pre-release scaffold raises NotImplementedError. Replace with real
    assertions once v0.1.0 implements the scorer."""
    with pytest.raises(NotImplementedError, match="pre-release"):
        audit("example.com")


def test_audit_rejects_empty_domain():
    with pytest.raises(ValueError, match="non-empty"):
        audit("")
    with pytest.raises(ValueError, match="non-empty"):
        audit("   ")


def test_empty_result_has_all_axes():
    result = _empty_result("example.com")
    assert isinstance(result, AuditResult)
    assert result.domain == "example.com"
    assert result.tier == Tier.NONE
    assert set(result.axis_scores.keys()) == set(AxisName)


def test_axis_max_total_is_100():
    """The six axes sum to 100 points."""
    total = sum(_axis_max(axis) for axis in AxisName)
    assert total == 100, f"Axis maxes must sum to 100; got {total}"


def test_axis_minimum_returns_none_when_axis_is_unconstrained():
    # Commerce Plumbing has no minimum at any tier (per thresholds.md)
    assert _axis_minimum(AxisName.COMMERCE_PLUMBING, Tier.BRONZE) is None
    assert _axis_minimum(AxisName.COMMERCE_PLUMBING, Tier.SILVER) is None
    assert _axis_minimum(AxisName.COMMERCE_PLUMBING, Tier.GOLD) is None


def test_axis_minimum_for_bronze_only_constrains_two_axes():
    # Bronze only requires minimums on Discoverability + Identity
    assert _axis_minimum(AxisName.DISCOVERABILITY, Tier.BRONZE) == 10
    assert _axis_minimum(AxisName.IDENTITY, Tier.BRONZE) == 8
    assert _axis_minimum(AxisName.AUTHORITY, Tier.BRONZE) is None


def test_audit_result_axis_minimums_passed_for_none_tier():
    result = _empty_result("example.com")
    assert result.axis_minimums_passed is False
