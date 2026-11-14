# Assistant Architecture — Post #5

## Mode
Mode A — Deterministic Guided Assistant. No LLM and no external data retrieval.

## Request flow
1. Receive question.
2. Enforce input length and basic safety checks.
3. Check supported scope.
4. Classify an approved intent deterministically.
5. Validate required parameters.
6. Route to a fixed query function.
7. Load approved intelligence through the existing validated service.
8. Build a bounded evidence package.
9. Compose a deterministic response.
10. Validate grounding, limits and metadata.
11. Return the response contract.

## Approved sources
- data-science/outputs/intelligence_results.json
- data-science/outputs/intelligence_summary.json
- data-science/outputs/validation_metrics.json

Use the existing intelligence loader and contract validation. Never read the canonical CSV directly from assistant query code.

## Workspace
- assistant/config: supported intents, query catalog, policy
- assistant/core: scope, intent, parameters, routing, evidence, composition, output validation
- assistant/queries: summary, result, comparison, trend, evidence and Track A queries
- assistant/prompts: grounded explanation policy (reference only; no LLM execution)
- assistant/logs: runtime-only non-sensitive operational logs
- frontend/src/app/components/data-assistant: UI components

## Security
No arbitrary SQL, code execution, external URLs, secrets access, unrestricted file access or persistent conversation memory. Server-side limits are mandatory.
