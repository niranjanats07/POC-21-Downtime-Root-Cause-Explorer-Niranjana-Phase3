# Assistant Core

This directory contains the deterministic policy, validation, routing, evidence, and response-control modules for the Grounded Data Assistant.

## Modules

- `policy.py` — Defines assistant policy and operating constraints.
- `scope_guard.py` — Checks incoming questions against permitted scope and safety rules.
- `intent_classifier.py` — Classifies supported question intents.
- `parameter_validator.py` — Validates extracted query parameters.
- `query_router.py` — Routes validated requests to the appropriate deterministic query.
- `evidence_builder.py` — Builds evidence references from approved query results.
- `response_composer.py` — Composes structured assistant responses.
- `output_validator.py` — Validates response content and contract requirements.

## Operating principles

1. Use approved Track A intelligence outputs as the source of analytical results.
2. Do not recalculate analytical rankings or metrics in the frontend.
3. Do not invent findings, evidence, measurements, or result identifiers.
4. Reject unsupported, unsafe, invalid, or unavailable requests using the response contract.
5. Enforce configured limits and version and quality checks.
6. Keep optional LLM functionality disabled unless separately approved and validated.

## Scope

The assistant provides deterministic, evidence-grounded explanations of approved descriptive intelligence results. It does not provide predictions, causal claims, unrestricted data access, or operational instructions.
