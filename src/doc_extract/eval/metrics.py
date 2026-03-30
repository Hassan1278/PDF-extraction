"""
Metrics for the extraction eval harness.

Generative fields (those described as 'summary' in the schema) are excluded
from exact-match scoring since their output is non-deterministic.
"""
from __future__ import annotations


def _is_generative_field(field: str, schema: dict) -> bool:
    desc = schema.get("properties", {}).get(field, {}).get("description", "")
    return "summary" in desc.lower()


def field_exact_match(predicted: dict, expected: dict, schema: dict) -> dict[str, bool]:
    """Returns per-field exact match result, skipping generative fields."""
    results = {}
    for field, expected_value in expected.items():
        if _is_generative_field(field, schema):
            continue
        predicted_value = predicted.get(field, "")
        results[field] = str(predicted_value).strip() == str(expected_value).strip()
    return results


def overall_exact_match(field_results: dict[str, bool]) -> float:
    """Fraction of fields that matched exactly."""
    if not field_results:
        return 0.0
    return sum(field_results.values()) / len(field_results)


def schema_valid_rate(results: list[dict]) -> float:
    if not results:
        return 0.0
    return sum(1 for r in results if r["valid"]) / len(results)


def failure_taxonomy(results: list[dict]) -> dict[str, int]:
    taxonomy: dict[str, int] = {
        "schema_invalid": 0,
        "page_failed": 0,
        "partial_match": 0,
        "success": 0,
    }
    for r in results:
        if r["pages_failed"]:
            taxonomy["page_failed"] += 1
        elif not r["valid"]:
            taxonomy["schema_invalid"] += 1
        elif r["field_match_rate"] < 1.0:
            taxonomy["partial_match"] += 1
        else:
            taxonomy["success"] += 1
    return taxonomy


def summarise(results: list[dict]) -> dict:
    latencies = [r["latency_s"] for r in results]
    field_rates = [r["field_match_rate"] for r in results]

    return {
        "total": len(results),
        "schema_valid_rate": round(schema_valid_rate(results), 3),
        "avg_field_match_rate": round(sum(field_rates) / len(field_rates), 3) if field_rates else 0.0,
        "avg_latency_s": round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
        "failure_taxonomy": failure_taxonomy(results),
    }
