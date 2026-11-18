# Supported Question Catalog — Post #5

## Approved scope
Mode A — Deterministic Guided Assistant. Source: approved Track A intelligence results and summary only.

## Supported intents and example questions
| Intent | Example | Required parameter |
|---|---|---|
| get_summary | Summarise downtime intelligence | None |
| list_priority_items | Which machine ranks highest? | Optional dimension |
| explain_result | Explain the MCH-02 result | Result ID or entity |
| compare_groups | Compare machines by downtime | Dimension |
| describe_segment | Which shift ranks highest? | Dimension |
| explain_method | How were groups compared? | None |
| explain_limitation | What are the limitations? | None |
| get_data_freshness | Which data and method versions were used? | None |

## Approved dimensions
- Category / root-cause category
- Machine
- Shift

## Grounding rules
Use only existing approved result values, summary metadata, evidence and limitations. Preserve source ranks and numbers. Maximum 25 results and 10 evidence references.

## Unsupported questions
Predictions, failure probabilities, causal explanations, significance tests, trends, future forecasts, arbitrary incident searches and unsupported dimensions must not be answered as facts.

## Follow-up suggestions
Maximum 3. Suggestions must map to supported intents.
