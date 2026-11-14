# Grounded Data Assistant

## Approved implementation mode
Mode A - Deterministic Guided Assistant. No LLM is used.

## Purpose
Help maintenance and operations supervisors navigate approved Track A
comparative intelligence results and their evidence.

## Approved source
The assistant must obtain data through the backend validated intelligence
service, which validates the approved intelligence results and summary.

It must not read or query the canonical CSV directly.

## Supported dimensions
- Root-cause category
- Machine
- Shift

## Supported capabilities
- Summary and priority results
- Explain an approved result by result ID
- Compare approved groups
- Explain methodology and limitations
- Show data freshness and validation status

## Limits
See `config/assistant_policy.json`. All limits must be enforced server-side.

## Workspace
- `config/`: supported intents, query catalog and policy
- `core/`: scope, intent, parameter, routing, evidence and response modules
- `queries/`: fixed deterministic query functions
- `prompts/`: reserved documentation only; no LLM prompt execution in Mode A
- `logs/`: runtime-only, non-sensitive logs

## Important limitations
All approved source incidents are synthetic. Results are descriptive
demonstration outputs and do not establish causation, prediction or actual
industrial performance.

## Security
Never expose secrets, environment variables, arbitrary SQL, unrestricted
canonical data, or unapproved external content.
