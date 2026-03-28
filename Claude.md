# Project: Document Extraction Pipeline

## Objective
Build a pipeline that accepts:
1. a PDF
2. a JSON Schema

and returns schema-valid extracted JSON using a local open-source model served through vLLM.

## Core rules
- Explore first, then plan, then code.
- Prefer small, reviewable changes.
- Run tests after meaningful edits.
- Keep modules separated by responsibility.
- Prefer explicit validation over ad-hoc parsing.
- Keep retry logic bounded and visible.

## Commands
- Run tests: `pytest -q`
- Run API: `uvicorn src.doc_extract.api:app --reload`
- Run CLI help: `python -m src.doc_extract.cli --help`
- Lint: `ruff check .`

## Architecture guardrails
- Keep PDF preprocessing separate from inference.
- Keep prompt construction separate from transport logic.
- Keep validation separate from aggregation.
- Every extraction response should include debug metadata.

## Definition of done
- Tests pass
- README updated if needed
- New failure paths are logged