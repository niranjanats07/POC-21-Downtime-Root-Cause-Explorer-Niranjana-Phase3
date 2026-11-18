# Grounded Data Assistant — Post #5 Reviewer Checklist

**Project:** POC-21 — Downtime Root Cause Explorer
**Review:** Phase 3 Post #5
**Checklist status:** Prepared for maintainer review
**Maintainer approval:** PENDING

---

## 1. Scope and architecture

- [x] Assistant is implemented as a separate feature on the Data Intelligence page.
- [x] Existing Post #4 Operational View is retained.
- [x] Deterministic Mode A Guided is active.
- [x] LLM explanation remains disabled.
- [x] Supported intent catalog is documented.
- [x] Query routing and parameter validation are implemented.
- [x] Approved Track A outputs are the source of assistant findings.
- [x] No frontend intelligence recalculation from the canonical CSV is introduced.

## 2. Grounding and response contract

- [x] Structured response contract is implemented.
- [x] Evidence references are validated against approved result IDs.
- [x] Invalid evidence references are rejected.
- [x] Data and method version checks are implemented.
- [x] Quality failure is handled as unavailable.
- [x] Approved ranking and numeric values are preserved in tested cases.
- [x] Synthetic-data and analytical limitations are communicated.
- [x] Evidence and follow-up response limits are enforced.

## 3. Safety and scope

- [x] Prompt disclosure request tested.
- [x] Secret and environment-variable disclosure request tested.
- [x] Instruction override request tested.
- [x] Embedded source-instruction case tested.
- [x] Broad record-export request tested.
- [x] Unsupported prediction request tested.
- [x] Ranking manipulation request tested.
- [x] Arbitr
