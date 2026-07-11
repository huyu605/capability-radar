# Evaluation model

Score each criterion from 0 to 100 using verified evidence. The weighted result is also 0–100.

| Criterion | Default weight | Interpretation |
| --- | ---: | --- |
| `fit` | 25 | Required outcomes, must-haves, and exclusions |
| `integration` | 15 | Environment compatibility and adoption effort |
| `maturity` | 15 | Reliability, documentation, tests, releases, and users |
| `security` | 15 | Supply-chain trust, permissions, vulnerabilities, and data handling |
| `maintenance` | 10 | Maintainer health, release cadence, issue handling, and momentum |
| `license` | 10 | License clarity and compatibility with intended use |
| `operations` | 10 | Infrastructure, support, migration, and total operating cost |

## Anchors

- **90–100**: unusually strong evidence and minimal material gaps.
- **75–89**: good, production-relevant evidence with manageable trade-offs.
- **50–74**: partial fit or meaningful validation work remains.
- **25–49**: major deficiencies or weak evidence.
- **0–24**: incompatible, absent, or unacceptable.

Do not convert missing evidence into a neutral score. Score the demonstrated state and list the gap.

## Confidence

The script derives confidence from candidate evidence:

- **High**: at least two primary sources, at least one independent source, and no critical missing evidence.
- **Medium**: at least one primary source and no more than one critical evidence gap.
- **Low**: no primary source or multiple critical gaps.

## Classification

- **Adopt**: score at least 80, confidence High or Medium, and no blockers.
- **Trial**: score 65–79, or score at least 80 with Low confidence.
- **Watch**: score 50–64.
- **Avoid**: score below 50 or any explicit blocker.

Use blockers only for decisive constraints such as an incompatible license, a missing must-have, an unacceptable security exposure, or an unsupported platform.

## Input contract

Pass a JSON object with optional metadata, optional custom `weights`, and a non-empty `candidates` list. Each candidate requires `name`, `type`, `url`, all seven `scores`, and structured `evidence`. Add `blockers` only for decisive constraints.

```json
{
  "as_of": "2026-07-11",
  "candidates": [
    {
      "name": "Example",
      "type": "library",
      "url": "https://github.com/example/project",
      "scores": {
        "fit": 85,
        "integration": 80,
        "maturity": 75,
        "security": 70,
        "maintenance": 80,
        "license": 90,
        "operations": 85
      },
      "evidence": {
        "primary_sources": 2,
        "independent_sources": 1,
        "missing_critical": []
      },
      "blockers": []
    }
  ]
}
```
