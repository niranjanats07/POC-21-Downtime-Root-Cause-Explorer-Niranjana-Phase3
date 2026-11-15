# Assistant Architecture — Post #5

## Modes

The Grounded Data Assistant supports two complementary modes:

- **Mode A — Deterministic Guided Assistant:** Classifies supported questions, retrieves approved Track A results, prepares evidence and produces the authoritative deterministic answer.
- **Mode B — Deterministic Retrieval + LLM Explanation:** Uses the Mode A response and its approved evidence package as bounded context for Gemini to generate a natural-language explanation.

Mode A remains authoritative. Gemini is an optional explanation layer and does not calculate, modify or replace approved analytical findings.

## Request flow

1. Receive the user's question.
2. Enforce input length and basic safety checks.
3. Check supported scope.
4. Classify an approved intent deterministically.
5. Validate required parameters, including direct entity references such as MCH-02.
6. Route to a fixed query function.
7. Load approved intelligence through the existing validated service.
8. Build a bounded evidence package from approved results.
9. Compose the deterministic answer and response metadata.
10. Validate grounding, limits, evidence and metadata.
11. Pass only the approved question, deterministic findings, supporting values and relevant limitations to Gemini when configured.
12. Validate the Gemini explanation against the approved context.
13. Return the deterministic answer, optional Gemini explanation, evidence references and limitations together.

## Mode B Gemini explanation layer

- Gemini is used only after deterministic classification, retrieval and response preparation.
- The Gemini request receives bounded, approved context rather than unrestricted application data.
- Gemini explains the meaning of retrieved findings in natural language.
- Gemini must not introduce unsupported numerical values, contradictory rankings, failure causes, predictions or maintenance recommendations.
- The deterministic answer, approved values, evidence references, versions and analytical limitations remain authoritative.
- A missing API key, API error, timeout or invalid Gemini explanation must not remove the deterministic answer or its evidence.
- If Gemini cannot provide an acceptable explanation, the response uses the appropriate fallback status and retains the deterministic result.

## Approved sources

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`

Use the existing intelligence loader and contract validation. Never read the canonical CSV directly from assistant query code. Do not regenerate or modify approved Track A outputs as part of the assistant integration.

## Workspace

- `assistant/config`: supported intents, query catalog and policy
- `assistant/core`: scope, intent, parameters, routing, evidence, composition and output validation
- `assistant/queries`: approved summary, result, comparison, evidence and supported Track A queries
- `assistant/prompts`: grounded Gemini explanation instructions and policy
- `assistant/logs`: runtime-only non-sensitive operational logs
- `assistant/core/gemini_explainer.py`: backend Gemini request, explanation validation and safe fallback handling
- `frontend/src/app/components/data-assistant`: assistant UI components

## Security

- Gemini API keys are read from backend environment configuration only.
- Never expose API keys through frontend code, browser responses, logs, screenshots or committed files.
- Do not place API keys in source code or request URLs.
- Do not provide Gemini with unrestricted file access, canonical CSV contents, arbitrary SQL, executable code, secrets or external retrieval capabilities.
- Keep server-side input, output and request limits.
- Treat Gemini output as untrusted until it passes the application's grounding and claim validation.

## Validation and limitations

- Deterministic values and evidence are validated independently of Gemini.
- Unsupported numerical claims, contradictory rankings and unsupported causal claims are rejected by the explanation validation layer.
- Automated tests cover successful explanations, invalid claims and safe fallback behavior.
- Live verification has demonstrated a successful Gemini explanation, missing-key fallback and API-error fallback.
- Actual quota exhaustion has not been separately demonstrated.
- Source incidents are synthetic. Findings are descriptive demonstration outputs and do not establish causation, prediction or actual industrial performance.
- Final Post #5 maintainer approval remains pending.
