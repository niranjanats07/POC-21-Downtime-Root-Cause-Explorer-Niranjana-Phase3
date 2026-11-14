# Assistant Queries

This package contains deterministic query functions for the approved Track A intelligence outputs.

## Module

- `track_a_queries.py` — Retrieves and formats approved Track A result data for supported assistant intents.

## Data and calculation rules

- Use the finalized intelligence result and summary packages.
- Preserve approved result identifiers, rankings, values, and evidence.
- Do not calculate new rankings or analytical metrics.
- Do not use the canonical CSV as a browser-side calculation source.
- Reject unknown result identifiers and unavailable or invalid data.
- Respect data-version, method-version, and quality-status checks.

## Scope

Queries support descriptive explanations of approved intelligence results only. They do not provide predictions, causal conclusions, or unrestricted record exports.
