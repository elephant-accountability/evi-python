# evi-python

Python reference implementation of the [Elephant Visibility Index (EVI)](https://github.com/elephant-accountability/evi).

Drop-in scorer that takes a domain and returns the same EVI breakdown the Elephant Accountability audit engine produces. Useful for self-audits, CI gating, and contribution to the spec.

## Status

**Pre-release v0.1.0 — Monday 2026-05-12.** This package is a scaffold; the scorer methods raise `NotImplementedError` until the canonical scoring code lands. The canonical scorer lives in the Elephant Accountability orchestrator. This repo is the public, pip-installable mirror.

## Install (when released)

```bash
pip install evi
```

## Planned API

```python
from evi import audit

result = audit("example.com")
print(result.score)        # 0-100
print(result.tier)         # "bronze" | "silver" | "gold" | None
print(result.axis_scores)  # per-axis breakdown
print(result.surfaces)     # detected surfaces with raw evidence
```

## Versioning policy

The package version follows semver and pins to a specific EVI spec version:

- `evi 0.x` → tracks `evi-spec v2.x` (scoring weights and rules from the v2 draft).
- `evi 1.x` → first stable release, locks in v2-final scoring.
- `evi 2.x` → tracks future spec major versions.

Material spec changes that affect scored outputs bump the package major version.

## Running tests

```bash
pip install -e ".[test]"
pytest
```

## License

MIT.

## Contributing

Issues and PRs welcome. The spec lives at [`elephant-accountability/evi`](https://github.com/elephant-accountability/evi); this repo is the implementation. Spec changes go to that repo first; implementation follows.

---

Maintained by [Elephant Accountability](https://eaccountability.org).
