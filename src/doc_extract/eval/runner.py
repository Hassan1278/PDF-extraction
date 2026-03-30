"""
Evaluation runner.

Usage:
    python -m src.doc_extract.eval.runner
    python -m src.doc_extract.eval.runner --ground-truth eval/ground_truth.json
"""
from __future__ import annotations

import json
import time
import argparse
from pathlib import Path

from src.doc_extract.pipeline import run_pipeline
from src.doc_extract.eval.metrics import field_exact_match, overall_exact_match, summarise

ROOT = Path(__file__).parent.parent.parent.parent


def run_eval(ground_truth_path: Path) -> None:
    cases = json.loads(ground_truth_path.read_text())
    results = []

    for case in cases:
        pdf_path = ROOT / case["pdf"]
        schema_path = ROOT / case["schema"]
        schema = json.loads(schema_path.read_text())
        expected = case["expected"]

        note = f"  ({case['note']})" if "note" in case else ""
        print(f"\n[{case['id']}]{note} Running pipeline...")
        t0 = time.perf_counter()
        result = run_pipeline(pdf_path, schema)
        latency = round(time.perf_counter() - t0, 2)

        field_results = field_exact_match(result.data, expected, schema)
        match_rate = overall_exact_match(field_results)

        entry = {
            "id": case["id"],
            "valid": result.valid,
            "latency_s": latency,
            "field_matches": field_results,
            "field_match_rate": round(match_rate, 3),
            "pages_failed": result.pages_failed,
            "errors": result.errors,
            "predicted": result.data,
            "expected": expected,
        }
        results.append(entry)

        status = "PASS" if result.valid and match_rate == 1.0 else "FAIL"
        print(f"  Status:      {status}")
        print(f"  Valid:       {result.valid}")
        print(f"  Field match: {match_rate:.0%}  {field_results}")
        print(f"  Latency:     {latency}s")
        if result.errors:
            print(f"  Errors:      {result.errors}")

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    summary = summarise(results)
    print(f"  Total cases:        {summary['total']}")
    print(f"  Schema valid rate:  {summary['schema_valid_rate']:.0%}")
    print(f"  Avg field match:    {summary['avg_field_match_rate']:.0%}")
    print(f"  Avg latency:        {summary['avg_latency_s']}s")
    print(f"  Failure taxonomy:   {summary['failure_taxonomy']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run extraction evaluation")
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=ROOT / "eval" / "ground_truth.json",
        help="Path to ground truth JSON file",
    )
    args = parser.parse_args()
    run_eval(args.ground_truth)
