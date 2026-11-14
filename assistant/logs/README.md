# Assistant Logging Policy

## Current implementation

The assistant does not use persistent conversation memory. This document defines safe logging requirements and does not claim that production logging or retention controls are configured.

## Permitted operational metadata

If logging is enabled, record only necessary operational metadata:
- Request identifier
- Timestamp and processing duration
- Validated intent and response status
- Data and method versions
- Non-sensitive error category

## Prohibited log content

Do not log:
- API keys, credentials, tokens, passwords, or environment variables
- System prompts or internal configuration
- Unnecessary raw user questions or complete answers
- Personal, confidential, or restricted source data
- Unrestricted canonical datasets

## Deployment review

Before production use, review access permissions, retention period, log storage, monitoring, and deletion procedures. Do not introduce persistent conversation memory without separate approval.
