# Grounded Response Contract — Post #5

Every assistant response must contain:

- answer_id: unique response identifier
- status: answered, unsupported, unsafe, unavailable or error
- intent: approved intent identifier or null
- answer: concise user-facing answer
- evidence_references: at most 10 source result references
- key_values: values copied from approved results
- metadata: data_version, method_version, generated_at, quality_status
- limitation: source limitation or explicit unsupported explanation
- suggested_follow_ups: at most 3 supported questions

## Grounding requirements
- Do not invent or recalculate analytical values.
- Preserve source numeric precision and ranking.
- Every factual numeric claim must be supported by a result reference.
- Include the approved synthetic-data limitation.
- Include source versions and quality status.
- Never claim prediction, causation or generalization.
- Unsupported questions must not receive speculative answers.
