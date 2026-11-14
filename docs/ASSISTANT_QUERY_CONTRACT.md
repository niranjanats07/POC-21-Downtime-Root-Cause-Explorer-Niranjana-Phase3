# Assistant Query Contract — Post #5

## Request
POST /api/assistant/query

{
  "question": "Which machine ranks highest by downtime?"
}

Question must be a non-empty string of at most 500 characters.

## Scope statuses
SUPPORTED, MISSING_PARAMETER, AMBIGUOUS, OUT_OF_SCOPE, UNSAFE, UNAVAILABLE.

## Query rules
- Only approved intent identifiers are accepted.
- Only category, machine and shift comparisons are supported.
- Query functions read validated Track A result packages.
- No client-provided SQL, file path, result value or arbitrary filter expression is accepted.
- Maximum 25 returned results and 10 evidence references.

## Errors
Invalid input: HTTP 422.
Unavailable approved package: HTTP 503.
Unexpected internal failure: generic HTTP 500 without secrets or stack traces.

## Compatibility
Do not modify existing /api/intelligence routes or Post #4 operational endpoints.
