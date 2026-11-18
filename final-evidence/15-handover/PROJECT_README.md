# POC-21 | Downtime Root Cause Explorer

**Infocreon Internship Project — Phase 3**

A web-based manufacturing analytics application for exploring machinery downtime, investigating potential root causes, analysing machine performance, and providing grounded data intelligence from validated analytical outputs.

---

## Project Overview

Downtime Root Cause Explorer helps operations and maintenance users examine downtime incidents, identify recurring patterns, compare machine performance, and investigate operational evidence.

The application includes:

- An Operational Dashboard for incident monitoring.
- A Data Intelligence page powered by approved Track A analytical outputs.
- A Grounded Data Assistant supporting deterministic and Gemini-assisted explanations.
- A reproducible Canonical Data Foundation.
- Automated testing and deployment validation.

The project uses synthetic downtime data. Results are descriptive demonstrations and must not be interpreted as verified real-world operational findings.

---

## Key Features

### Operational Dashboard

- Downtime analytics and KPI monitoring.
- Incident records and machine filtering.
- Interactive charts and visualisations.
- Root Cause Exploration through the Intelligence Panel.
- CSV and JSON data exports.
- Machine and shift performance views.

### Data Intelligence — Post #4

A separate Data Intelligence page presents finalized Track A analytical outputs.

Features include:

- Root-cause category rankings.
- Machine downtime comparisons.
- Shift comparisons.
- Evidence-backed analytical results.
- Methodology and validation information.
- Data freshness and quality metadata.
- Synthetic-data limitations.

### Grounded Data Assistant — Post #5

The Grounded Data Assistant provides a natural-language interface for supported questions about approved analytical results.

It supports eight approved intent categories:

1. `get_summary`
2. `list_priority_items`
3. `explain_result`
4. `compare_groups`
5. `describe_segment`
6. `explain_method`
7. `explain_limitation`
8. `get_data_freshness`

The assistant uses a two-mode architecture.

**Mode A — Deterministic Grounded Responses**

- Classifies supported questions.
- Retrieves information from approved analytical outputs.
- Validates parameters and evidence.
- Returns deterministic answers with evidence references and limitations.

**Mode B — Gemini Explanation Integration**

- Uses the deterministic assistant to prepare the approved answer and evidence first.
- Sends bounded, approved context to the Gemini API for a natural-language explanation.
- Displays the deterministic answer and Gemini explanation separately.
- Preserves evidence references and limitations.
- Rejects unsupported numerical claims, contradictory rankings and unsupported causal or predictive claims.
- Falls back to the deterministic response when Gemini is unavailable, fails, or returns an invalid explanation.

**Important:** Gemini is an optional explanation layer. It does not calculate, replace, or modify approved analytical results. The API key is configured on the backend and must never be exposed in frontend code or committed to the repository.

---

## Technology Stack

| Component | Technologies |
|:---|:---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, Pandas, DuckDB |
| Visualisation | Apache ECharts, Plotly, D3.js |
| Data Tables | TanStack Table |
| Data Processing | Python, CSV, JSON |
| AI Explanation | Google Gemini API |
| Containerisation | Docker, Docker Compose |
| Cloud Hosting | Render |
| Automated Testing | Pytest, Selenium WebDriver 4, Python, Google Chrome |
| Version Control | Git, GitHub |

---

## Project Setup

### Run Locally

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend:

`http://localhost:8000`

#### Frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

`http://localhost:3000`

### Gemini Backend Configuration

Gemini integration requires a valid API key configured as a backend environment variable.

Do not place the key in frontend environment variables, source files, documentation, screenshots, or Git commits.

The application must retain deterministic responses when Gemini is not configured or is unavailable.

### Run with Docker

Prerequisites: Docker Desktop and Docker Compose.

From the project root:

```bash
docker compose up --build -d
```

| Service | Local URL |
|:---|:---|
| Frontend | `http://localhost:3000` |
| Backend API | `http://localhost:8000` |
| Backend Health | `http://localhost:8000/health` |

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Stop containers:

```bash
docker compose down
```

---

## Live Deployment — Render

The application is deployed using Docker-based Render services.

### Application URLs

| Service | URL |
|:---|:---|
| Operational Dashboard | https://downtime-frontend-phase3.onrender.com/ |
| Data Intelligence | https://downtime-frontend-phase3.onrender.com/data-intelligence |
| Backend API | https://downtime-backend-phase3.onrender.com/ |
| Backend Health | https://downtime-backend-phase3.onrender.com/health |
| Intelligence Health | https://downtime-backend-phase3.onrender.com/api/intelligence/health |

### Deployment Configuration

| Setting | Configuration |
|:---|:---|
| Hosting Platform | Render |
| Deployment Method | Docker |
| Git Branch | `main` |
| Frontend Health Check | `/` |
| Backend Health Check | `/health` |

### Environment Variables

Frontend:

```env
NEXT_PUBLIC_API_URL=https://downtime-backend-phase3.onrender.com
```

Backend CORS configuration:

```env
FRONTEND_ORIGIN=https://downtime-frontend-phase3.onrender.com
```

The Gemini API key is a backend-only secret and must be configured through the hosting provider's environment settings when Gemini is enabled.

---

## Phase 3 — Canonical Data Foundation

Phase 3 establishes a reproducible Canonical Data Foundation for the Downtime Root Cause Explorer.

The supplied synthetic downtime incident data is standardised into a canonical measurement structure for consistent validation and publication.

### Data Pipeline

The pipeline is available under:

`scripts/data_pipeline/`

Run from the repository root:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
py scripts/data_pipeline/standardize_data.py
py scripts/data_pipeline/validate_data.py
py scripts/data_pipeline/publish_data.py
```

Validate the package:

```powershell
py scripts/data_pipeline/validate_data.py
```

### Canonical Dataset

| Item | Result |
|:---|---:|
| Package Version | 1.1.0 |
| Synthetic Source Incidents | 30 |
| Source Sample Records | 30 |
| Canonical Measurement Records | 60 |
| Canonical Columns | 22 |
| Measurements per Source Incident | 2 |

Each source incident produces two canonical measurement records:

- `downtime_minutes`
- `failure_frequency`

The canonical CSV is the source of truth. Published JSON is generated from the canonical CSV.

### Canonical Data Files

| File | Purpose |
|:---|:---|
| `data/synthetic/downtime_incidents.csv` | Original synthetic source dataset |
| `data/source-sample/source_sample.csv` | Retained source sample |
| `data/canonical/intelligence_data.csv` | Canonical source of truth |
| `data/published/intelligence_data.json` | Published JSON |
| `data/schema.json` | Canonical field definitions |
| `data/manifest.json` | Package metadata |
| `data/quality/data_profile.json` | Data profile |
| `data/quality/validation_report.json` | Validation results |

---

## Post #4 — Data Intelligence

The Data Intelligence page is available at:

https://downtime-frontend-phase3.onrender.com/data-intelligence

It consumes finalized approved Track A outputs rather than performing independent analytical calculations in the frontend.

### Approved Analytical Outputs

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`

The integration validates the output contract and checks the data and method versions before presenting results.

### Analytical Snapshot

| Metric | Value |
|:---|---:|
| Data Version | 1.1.0 |
| Method Version | 1.0.0 |
| Quality Status | PASS |
| Validated Results | 11 |
| Incidents | 30 |
| Observed Downtime | 2,795 minutes |

### Machine Comparison

| Machine | Observed Downtime | Rank |
|:---|---:|---:|
| MCH-02 | 850 minutes | 1 |
| MCH-04 | 700 minutes | 2 |
| MCH-01 | 635 minutes | 3 |
| MCH-03 | 610 minutes | 4 |

These are descriptive results from the approved synthetic analytical dataset, not verified operational performance measurements.

---

## Post #5 — Grounded Data Assistant

The Grounded Data Assistant is integrated into the Data Intelligence experience.

### API Endpoint

```http
POST /api/assistant/query
```

### Example Questions

- Give me an overall summary.
- Which machine has the highest observed downtime?
- Compare the downtime across machines.
- Which root-cause category ranks highest?
- Explain the analytical methodology.
- What limitations apply to these results?
- What is the current data freshness?
- Describe the results for MCH-02.

### Grounding and Safety

The assistant:

- Uses approved Track A output files.
- Restricts requests to supported intents and parameters.
- Retrieves deterministic analytical evidence.
- Validates response evidence.
- Includes source references and limitations.
- Avoids unsupported causal, predictive and statistical claims.
- Keeps Gemini explanations separate from deterministic results.
- Preserves deterministic answers and evidence during Gemini failures.

Individual incident-level evidence is not available in the approved Track A output package. The assistant therefore does not invent individual incident evidence.

### Gemini Mode B Live Verification

A successful live Gemini API execution was verified on 15 November 2026.

The test question was:

`Why is MCH-02 ranked first for downtime?`

The deterministic response identified:

- Machine: MCH-02
- Observed downtime: 850 minutes
- Machine ranking: 1
- Evidence reference: `RES-0005`

Gemini successfully generated a natural-language explanation using the approved evidence. The deterministic answer, evidence reference and limitations remained available independently.

Additional verification included:

- Missing API key fallback.
- Invalid API key / API error fallback.
- Simulated HTTP 429 quota-exhaustion fallback.
- Rejection of unsupported numerical claims.
- Rejection of contradictory rankings.
- Rejection of unsupported causal claims.
- Preservation of deterministic answers and evidence when Gemini fails.

Actual account quota exhaustion was not deliberately triggered.

### Assistant Selenium Evidence

The previously recorded assistant Selenium evidence suite completed with:

**5 passed, 0 failed.**

The evidence covers assistant loading, supported questions, machine ranking, evidence references, metadata and unsupported question handling.

---

## Automated Testing and Validation

### Full Backend Regression

Run from the repository root:

```powershell
py -m pytest .\backend\tests -v
```

Latest recorded result, 15 November 2026:

**44 passed, 0 failed.**

### Gemini Explanation Tests

```powershell
py -m pytest .\backend\tests\test_gemini_explainer.py -v
```

Latest recorded result:

**9 passed, 0 failed.**

Coverage includes successful explanations, safe fallback behaviour, invalid numerical claims, contradictory rankings, unsupported causal claims and preservation of deterministic evidence.

The HTTP 429 quota fallback test is simulated; actual account quota exhaustion was not deliberately triggered.

### Frontend TypeScript Validation

Run from the frontend directory:

```powershell
npx tsc --noEmit
```

Latest recorded result: **PASS**.

### Frontend Production Build

Run from the frontend directory:

```powershell
npm run build
```

Latest recorded result: **SUCCESS**.

The build generated the application routes, including `/data-intelligence`.

### Assistant Selenium Evidence Tests

From the repository root:

```powershell
py -m pytest tests/test_assistant_selenium.py -q
```

Previously recorded result:

**5 passed.**

### Existing Operational Selenium Tests

The original operational Selenium suite is retained:

```powershell
py -u tests/test_poc.py
```

Its previously recorded result was 8 passed and 0 failed on 3 November 2026.

Test results above refer to their recorded executions; they should not be interpreted as a guarantee that every environment or future deployment will produce identical results.

---

## Supporting Documentation

The `docs/` directory contains implementation, validation, architecture and submission evidence.

Important Post #5 documents:

- `docs/ASSISTANT_IMPLEMENTATION_LOG.md`
- `docs/ASSISTANT_ARCHITECTURE.md`
- `docs/ASSISTANT_UAT.md`
- `docs/ASSISTANT_GROUNDING_VALIDATION.md`
- `docs/ASSISTANT_SUBMISSION_PACKAGE.md`
- `docs/ASSISTANT_REVIEWER_CHECKLIST.md`
- `docs/POST5_ASSISTANT_SELENIUM_EVIDENCE.md`
- `docs/POST5_GEMINI_LIVE_VERIFICATION.md`
- `docs/POST5_GEMINI_REVIEWER_CHECKLIST.md`

Gemini screenshot evidence:

`docs/evidence/post5-gemini/mode-b-successful-gemini.png`

Post #4 Data Intelligence documentation and analytical reports are also retained in the repository.

---

## Known Limitations

- The supplied downtime dataset is synthetic.
- The source dataset contains only 30 synthetic incidents.
- Results should not be interpreted as representative of real-world manufacturing operations.
- The analysis is descriptive and does not establish causation.
- Predictive forecasts, statistical significance and anomaly detection are outside the approved Track A scope.
- Small group sizes may affect ranking stability.
- Individual incident-level evidence is not included in the approved Track A analytical outputs.
- Gemini explanations do not create or modify analytical results.
- Gemini availability depends on backend API configuration and provider availability.
- Deterministic assistant responses remain the fallback when Gemini is unavailable.
- Geographic coordinates are not available in the supplied source data.
- Some chart and table content may require horizontal scrolling on narrow screens.
- Post #5 maintainer review and final approval: Approved.

---

## Post #6 — Final Certification and Handover

Post #6 covers the final technical certification, deployment validation, regression testing, evidence consolidation and handover of the Phase 3 application.

### Certification Scope

The final certification plan contains 24 controlled steps covering:

- Pre-certification source snapshot and release identity.
- Clean-clone, canonical-data and analytical reproducibility checks.
- Intelligence output contract and frontend/backend build validation.
- Operational Dashboard and Data Intelligence regression.
- Grounded Assistant validation and automated tests.
- Final Selenium journey and technical user acceptance testing.
- Production deployment and local Docker container validation.
- Evidence-pack preparation, architecture, completion report and handover.
- Final source snapshot, release tag and GitHub submission, subject to authorization.

### Verified Test and Validation Results

- Consolidated automated suite: 64 passed, 0 failed, 1 warning.
- Frontend lint, TypeScript validation and production build: passed.
- Final Selenium journey: passed.
- Technical final UAT: passed, including mobile viewport, keyboard focus visibility, API error and retry, empty results and filter reset checks.
- Production deployment endpoint checks: HTTP 200 for the application and Data Intelligence routes; backend health reported healthy.
- Local Docker Compose build and runtime checks: passed; backend health and both frontend routes verified.
- Approved Track A output: 11 results, 30 source incidents and 2,795 observed downtime minutes.
- Data version: 1.1.0.
- Method version: 1.0.0.

The automated test warning and validation limitations are documented in the detailed reports. Technical verification does not establish independent confirmation of the deployed source commit or Render build identity.

### Evidence and Handover Documents

Key Post #6 documents:

- `docs/PHASE3_RELEASE_MANIFEST.md`
- `docs/PHASE3_CLEAN_CLONE_VALIDATION_REPORT.md`
- `docs/PHASE3_CANONICAL_DATA_VALIDATION_REPORT.md`
- `docs/PHASE3_DATA_READINESS_REVALIDATION_REPORT.md`
- `docs/PHASE3_ANALYTICAL_REGENERATION_REPORT.md`
- `docs/PHASE3_AUTOMATED_TEST_REPORT.md`
- `docs/PHASE3_FINAL_SELENIUM_REPORT.md`
- `docs/PHASE3_POST6_FINAL_UAT_REPORT.md`
- `docs/PHASE3_POST6_DEPLOYMENT_VALIDATION_REPORT.md`
- `docs/PHASE3_POST6_CONTAINER_VALIDATION_REPORT.md`
- `docs/PHASE3_FINAL_ARCHITECTURE.md`
- `docs/PHASE3_COMPLETION_REPORT.md`
- `docs/PHASE3_HANDOVER_GUIDE.md`
- `final-evidence/README.md`

The `final-evidence/` directory contains the prescribed 15-folder evidence structure, including release, clean-clone, data, analytical, regression, assistant, automated-test, Selenium, UAT, deployment, screenshot and handover evidence.

### Certification Status

**Technical validation is substantially complete; final certification is pending.**

The following release activities remain subject to completion and explicit authorization:

- Release-manifest reconciliation against the final certified commit and tag.
- Root README and final evidence-pack review.
- Final Repomix generation after authorized repository changes.
- Release tag `phase3-v1.0.0`.
- Final GitHub submission and reviewer signoff.

No final certification outcome is assigned in this README. The approved final outcomes are:

- `PHASE 3 COMPLETE — CERTIFIED`
- `PHASE 3 FINAL CHANGES REQUIRED`
- `PHASE 3 CERTIFICATION BLOCKED`

## Project Status

| Phase / Deliverable | Status |
|:---|:---|
| Phase 2 Operational Dashboard | Preserved |
| Phase 3 Canonical Data Foundation | Implemented |
| Post #4 Data Intelligence Page | Approved |
| Post #5 Deterministic Grounded Assistant | Implemented |
| Post #5 Gemini Mode B Integration | Implemented and live-verified |
| Post #5 Backend Regression | 44 tests passed |
| Post #5 Gemini Tests | 9 tests passed |
| Post #5 Frontend TypeScript and Build | Passed |
| Post #6 Automated Test Suite | 64 passed, 0 failed, 1 warning |
| Post #6 Final Selenium Journey | Passed |
| Post #6 Technical UAT | Passed; reviewer signoff pending |
| Post #6 Deployment Validation | Passed; deployed build identity not independently verified |
| Post #6 Container Validation | Passed locally |
| Post #6 Architecture, Completion and Handover Documents | Prepared |
| Post #6 Final Certification | Pending |
| Post #5 Maintainer Approval | Approved |

Implementation and verification completion do not constitute formal maintainer approval or production certification.

---

## Developer Information

| Detail | Information |
|:---|:---|
| Developer | Niranjana T Suresh |
| PoC ID | 21 |
| Organisation | Infocreon |
| Programme | Internship — Phase 3 |
| Batch | Batch 8 / MA College |
| GitHub | [@niranjanats07](https://github.com/niranjanats07) |

---

## Repository

**POC-21 — Downtime Root Cause Explorer | Phase 3**

GitHub Repository:

https://github.com/niranjanats07/POC-21-Downtime-Root-Cause-Explorer-Niranjana-Phase3

---

<p align="center">
  <strong>POC-21 | DOWNTIME ROOT CAUSE EXPLORER</strong><br/>
  <sub>Manufacturing Downtime Analytics, Data Intelligence &amp; Grounded Evidence</sub><br/>
  <sub>Infocreon Internship Programme — Phase 3</sub>
</p>
