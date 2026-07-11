#!/usr/bin/env python3
"""Validate and score capability-radar candidate JSON using only the standard library."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


DEFAULT_WEIGHTS = {
    "fit": 25,
    "integration": 15,
    "maturity": 15,
    "security": 15,
    "maintenance": 10,
    "license": 10,
    "operations": 10,
}
CLASSIFICATION_ORDER = {"Adopt": 0, "Trial": 1, "Watch": 2, "Avoid": 3}


class ValidationError(ValueError):
    pass


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{label} must be a number")
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ValidationError(f"{label} must be between 0 and 100")
    return value


def validate_weights(weights: Any) -> dict[str, float]:
    if not isinstance(weights, dict):
        raise ValidationError("weights must be an object")
    if set(weights) != set(DEFAULT_WEIGHTS):
        expected = ", ".join(DEFAULT_WEIGHTS)
        raise ValidationError(f"weights must contain exactly: {expected}")
    clean = {key: _number(weights[key], f"weights.{key}") for key in DEFAULT_WEIGHTS}
    if not math.isclose(sum(clean.values()), 100.0, abs_tol=1e-9):
        raise ValidationError("weights must total 100")
    return clean


def derive_confidence(evidence: Any) -> str:
    if not isinstance(evidence, dict):
        evidence = {}
    primary = evidence.get("primary_sources", 0)
    independent = evidence.get("independent_sources", 0)
    missing = evidence.get("missing_critical", [])
    if not isinstance(primary, int) or primary < 0:
        raise ValidationError("evidence.primary_sources must be a non-negative integer")
    if not isinstance(independent, int) or independent < 0:
        raise ValidationError("evidence.independent_sources must be a non-negative integer")
    if not isinstance(missing, list) or not all(isinstance(item, str) for item in missing):
        raise ValidationError("evidence.missing_critical must be a list of strings")
    if primary >= 2 and independent >= 1 and not missing:
        return "High"
    if primary >= 1 and len(missing) <= 1:
        return "Medium"
    return "Low"


def classify(score: float, confidence: str, blockers: list[str]) -> str:
    if blockers or score < 50:
        return "Avoid"
    if score < 65:
        return "Watch"
    if score < 80 or confidence == "Low":
        return "Trial"
    return "Adopt"


def score_candidate(candidate: Any, weights: dict[str, float]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise ValidationError("each candidate must be an object")
    for field in ("name", "type", "url"):
        if not isinstance(candidate.get(field), str) or not candidate[field].strip():
            raise ValidationError(f"candidate.{field} must be a non-empty string")
    scores = candidate.get("scores")
    if not isinstance(scores, dict) or set(scores) != set(DEFAULT_WEIGHTS):
        expected = ", ".join(DEFAULT_WEIGHTS)
        raise ValidationError(f"candidate.scores must contain exactly: {expected}")
    clean_scores = {
        key: _number(scores[key], f"{candidate['name']}.scores.{key}")
        for key in DEFAULT_WEIGHTS
    }
    blockers = candidate.get("blockers", [])
    if not isinstance(blockers, list) or not all(isinstance(item, str) for item in blockers):
        raise ValidationError(f"{candidate['name']}.blockers must be a list of strings")
    confidence = derive_confidence(candidate.get("evidence", {}))
    total = round(sum(clean_scores[key] * weights[key] / 100 for key in weights), 1)
    result = dict(candidate)
    result["scores"] = clean_scores
    result["weighted_score"] = total
    result["confidence"] = confidence
    result["classification"] = classify(total, confidence, blockers)
    return result


def score_document(document: Any) -> dict[str, Any]:
    if isinstance(document, list):
        candidates = document
        weights = validate_weights(DEFAULT_WEIGHTS)
        metadata: dict[str, Any] = {}
    elif isinstance(document, dict):
        candidates = document.get("candidates")
        weights = validate_weights(document.get("weights", DEFAULT_WEIGHTS))
        metadata = {key: value for key, value in document.items() if key not in {"candidates", "weights"}}
    else:
        raise ValidationError("input must be a candidate list or an object with candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValidationError("candidates must be a non-empty list")
    results = [score_candidate(candidate, weights) for candidate in candidates]
    results.sort(
        key=lambda item: (
            CLASSIFICATION_ORDER[item["classification"]],
            -item["weighted_score"],
            item["name"].lower(),
        )
    )
    return {**metadata, "weights": weights, "candidates": results}


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(data: Any, output: str | None, pretty: bool) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2 if pretty else None, sort_keys=False)
    if output:
        Path(output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def self_test() -> None:
    fixture = {
        "as_of": "2026-01-01",
        "candidates": [
            {
                "name": "Strong",
                "type": "library",
                "url": "https://example.com/strong",
                "scores": {key: 90 for key in DEFAULT_WEIGHTS},
                "evidence": {"primary_sources": 2, "independent_sources": 1, "missing_critical": []},
            },
            {
                "name": "Blocked",
                "type": "product",
                "url": "https://example.com/blocked",
                "scores": {key: 95 for key in DEFAULT_WEIGHTS},
                "evidence": {"primary_sources": 2, "independent_sources": 1, "missing_critical": []},
                "blockers": ["Incompatible license"],
            },
        ],
    }
    result = score_document(fixture)
    assert result["candidates"][0]["name"] == "Strong"
    blocked = next(item for item in result["candidates"] if item["name"] == "Blocked")
    assert blocked["classification"] == "Avoid"
    strong = next(item for item in result["candidates"] if item["name"] == "Strong")
    assert strong["weighted_score"] == 90.0
    assert strong["confidence"] == "High"
    assert strong["classification"] == "Adopt"
    try:
        validate_weights({**DEFAULT_WEIGHTS, "fit": 24})
    except ValidationError:
        pass
    else:
        raise AssertionError("invalid weight total was accepted")
    print("self-test passed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    score = subparsers.add_parser("score", help="validate and score candidate JSON")
    score.add_argument("input", help="input JSON path or - for stdin")
    score.add_argument("--output", "-o", help="write JSON to this path")
    score.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    subparsers.add_parser("self-test", help="run deterministic built-in tests")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "self-test":
            self_test()
        else:
            write_json(score_document(load_json(args.input)), args.output, args.pretty)
    except (OSError, json.JSONDecodeError, ValidationError, AssertionError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
