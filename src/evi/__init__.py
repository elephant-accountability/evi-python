"""evi — Python reference implementation of the Elephant Visibility Index.

The canonical methodology lives at https://github.com/elephant-accountability/evi.
This package mirrors the scoring engine used by Elephant Accountability's
audit pipeline, exposed as a pip-installable library for self-audits and CI gating.

Pre-release status. Public API is the `audit` function and the dataclasses in
`evi.types`. Internal modules (`evi.scorer`, `evi.detect.*`) may change without
notice until the v0.1.0 release on 2026-05-12.
"""

from evi.scorer import audit
from evi.types import AuditResult, AxisScore, SurfaceDetection, Tier

__version__ = "0.1.0"
__all__ = ["audit", "AuditResult", "AxisScore", "SurfaceDetection", "Tier"]
