# Phase 3 — Deployment and Technical Handover Guide

**Project:** POC-21 — Downtime Root Cause Explorer  
**Repository:** POC-21-Downtime-Root-Cause-Explorer-Niranjana-Phase3  
**Branch:** main  
**Application version:** 0.1.0  
**Canonical data version:** 1.1.0  
**Analytical method version:** 1.0.0  
**Approved analytical track:** Track A  
**Status:** Technical handover draft — final certification pending  
**Guide date:** 18 November 2026

---

## 1. Purpose and Scope

This guide provides operating, validation, troubleshooting, and maintenance information for the Phase 3 application.

Phase 3 adds a separate Data Intelligence page and a grounded data assistant while preserving the existing Phase 2 Operational Dashboard.

This document describes the inspected application configuration and the verification activities recorded during Post #6 certification.

It does not authorize:
- Production deployment or redeployment.
- Git commits, pushes, tags, or releases.
- Changes to approved canonical data or analytical outputs.
- Changes to approved assistant safety boundaries.
- Use of synthetic findings as actual company performance evidence.

Final certification and reviewer approval remain pending.

## 2. Application Overview

The application contains three principal capabilities.

### 2.1 Operational Dashboard

The existing Phase 2 dashboard supports operational monitoring and incident investigation.

It includes:
- Operational KPIs.
- Downtime and incident information.
- Cause Pareto analysis.
- Frequency-versus-duration analysis.
- Machine and shift comparisons.
- Incident investigation details.

### 2.2 Data Intelligence

The separate Data Intelligence page presents approved Track A analytical outputs.

It includes:
- Summary metrics.
- Root-cause category, machine, and shift rankings.
- Comparison and contribution views.
- Evidence records.
- Methodology and validation information.
- Synthetic-data limitations.
- Data and method version information.

### 2.3 Grounded Data Assistant

The assistant provides deterministic answers using approved intelligence outputs. Optional Gemini explanations are bounded by the deterministic result and approved evidence.

The assistant must not invent measurements, rankings, causal explanations, or predictions.

### 2.4 Data-use boundary

The canonical dataset is synthetic. Findings are descriptive and must not be represented as actual operational company data.

## 3. Production URLs

| Service | URL |
|---|---|
| Frontend | https://downtime-frontend-phase3.onrender.com |
| Operational Dashboard | https://downtime-frontend-phase3.onrender.com/ |
| Data Intelligence | https://downtime-frontend-phase3.onrender.com/data-intelligence |
| Backend | https://downtime-backend-phase3.onrender.com |
| Backend health | https://downtime-backend-phase3.onrender.com/health |

These endpoints were observed during certification validation. Recheck availability before relying on them.

Production endpoint validation is documented in:

`docs/PHASE3_POST6_DEPLOYMENT_VALIDATION_REPORT.md`

Do not trigger a deployment as part of this handover procedure.

## 4. Render Deployment Configuration

The repository `render.yaml` defines two Docker web services in Singapore on the Free plan.

### Backend

- Service: `downtime-backend`
- Runtime: Docker
- Dockerfile: `backend/Dockerfile`
- Docker context: repository root
- Health check: `/health`

### Frontend

- Service: `downtime-frontend`
- Runtime: Docker
- Dockerfile: `frontend/Dockerfile`
- Docker context: repository root

The services are separate.

Before any authorized deployment change, verify the deployed frontend API configuration and backend URL in Render settings.

Never include API keys or other secrets in this guide, screenshots, logs, or evidence files.

## 5. Local Docker Compose Configuration

The repository contains:

`docker-compose.yml`

| Service | Container name | Host port | Container port |
|---|---|---:|---:|
| Backend | downtime-backend | 8000 | 8000 |
| Frontend | downtime-frontend | 3000 | 3000 |

The frontend Compose environment specifies:

`NEXT_PUBLIC_API_URL=http://localhost:8000`

The frontend service depends on the backend service.

### Dockerfiles

- Backend: `backend/Dockerfile`
- Frontend: `frontend/Dockerfile`

The backend container runs the FastAPI application using Uvicorn.

The frontend container runs the production Next.js application.

The repository `.dockerignore` excludes development dependencies, build outputs, Python caches, environment files, and Repomix output from the Docker build context.

## 6. Local Service Verification

Run PowerShell commands from the project root.

### 6.1 Docker Desktop prerequisite

Before running Docker Compose commands:

1. Start Docker Desktop from the Windows Start menu.
2. Wait until its Linux engine is ready.
3. Open PowerShell in the project root.
4. Confirm that the Docker client can communicate with the server:

```powershell
docker info
```

The output must include server information. A client-only response followed by a Docker API connection error means the engine is not yet available.

### 6.2 Inspect the Compose configuration

```powershell
docker compose config
```

### 6.3 Inspect existing services

```powershell
docker compose ps -a
```

Check the container inventory before starting services. Do not remove or replace unrelated project containers or preserved Phase 2 containers.

### 6.4 Build when a rebuild is required

```powershell
docker compose build
```

A rebuild is not necessary merely because Docker Desktop was stopped.

### 6.5 Start the Phase 3 services

```powershell
docker compose up -d
```

This command targets the services defined by the current project's Compose file.

### 6.6 Confirm service status

```powershell
docker compose ps
```

Both the backend and frontend should show a running status.

### 6.7 Verify backend health

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected response:

```text
status
------
healthy
```

### 6.8 Verify frontend routes

Operational Dashboard:

```powershell
(Invoke-WebRequest http://localhost:3000/ -UseBasicParsing).StatusCode
```

Data Intelligence:

```powershell
(Invoke-WebRequest http://localhost:3000/data-intelligence -UseBasicParsing).StatusCode
```

Expected HTTP status for both routes: `200`.

### 6.9 Local verification record — 18 November 2026

Docker Desktop initially had no reachable Linux engine. After Docker Desktop was started, the engine responded successfully.

The container inventory was inspected before restarting the POC-21 Phase 3 services.

The separate POC-2 Interchange Fee Calculator project was running on host ports 3001 and 8001. It did not conflict with POC-21 ports 3000 and 8000.

Only the POC-21 Phase 3 Compose services were restarted. The preserved POC-21 Phase 2 containers and POC-2 project containers were not modified.

Recorded verification:

| Check | Result |
|---|---|
| Docker engine | PASS — Docker 29.9.2 |
| Backend container | PASS — running on port 8000 |
| Frontend container | PASS — running on port 3000 |
| Backend health | PASS — `healthy` |
| Operational Dashboard | PASS — HTTP 200 |
| Data Intelligence | PASS — HTTP 200 |

This verifies local container startup and HTTP endpoint availability. It does not replace a full browser-based local UI test or production deployment validation.

## 7. Data Intelligence API

The Data Intelligence backend exposes the following GET endpoints:

| Endpoint | Purpose |
|---|---|
| `/api/intelligence/summary` | Approved analytical summary |
| `/api/intelligence/results` | Approved flat result collection |
| `/api/intelligence/results/{result_id}` | Individual result lookup |
| `/api/intelligence/metadata` | Version, timestamp, and quality metadata |
| `/api/intelligence/health` | Intelligence service health |

The frontend consumes the summary, results, and metadata endpoints.

The API uses the approved intelligence package and contract validation. It must not independently recalculate analytical results from the canonical CSV in the browser.

Expected response behavior includes successful responses for valid requests, not-found behavior for unknown result IDs, and service-unavailable behavior when the approved package cannot be loaded or validated.

Refer to:

- `docs/INTELLIGENCE_API_CONTRACT.md`
- `docs/INTELLIGENCE_OUTPUT_CONTRACT.md`
- `docs/INTELLIGENCE_INTEGRATION_MAPPING.md`

## 8. Approved Data and Analytical Outputs

### 8.1 Approved source outputs

The approved Track A package consists of:

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`

The canonical data and supporting metadata are maintained under:

- `data/canonical/intelligence_data.csv`
- `data/manifest.json`
- `data/schema.json`

### 8.2 Version information

| Item | Approved value |
|---|---|
| Application version | 0.1.0 |
| Canonical data version | 1.1.0 |
| Analytical method version | 1.0.0 |
| Analytical track | Track A |

The data and method versions must match across the approved outputs and application metadata.

### 8.3 Analytical boundaries

Track A provides descriptive group-level comparisons for:
- Root-cause categories.
- Machines.
- Shifts.

The minimum group-size rule is three observations.

The results are not predictive, causal, or proof of machine failure mechanisms.

Do not modify the approved output package during ordinary frontend maintenance.

## 9. Validated Findings Reference

The following values were observed in the approved Track A outputs during certification validation.

### 9.1 Overall summary

| Measure | Validated value |
|---|---:|
| Source incidents | 30 |
| Total observed downtime | 2,795 minutes |
| Average downtime per incident | 93.1667 minutes |
| Total failure frequency | 65 |
| Average failure frequency | 2.1667 |

### 9.2 Root-cause category comparison

| Category | Observed downtime |
|---|---:|
| Mechanical | 1,265 minutes |
| Electrical | 950 minutes |
| Maintenance | 360 minutes |
| Operational | 220 minutes |

### 9.3 Machine comparison

| Machine | Observed downtime |
|---|---:|
| MCH-02 | 850 minutes |
| MCH-04 | 700 minutes |
| MCH-01 | 635 minutes |
| MCH-03 | 610 minutes |

MCH-02 is the highest observed machine downtime group in this approved output.

Its validated result includes eight incidents and an average downtime of 106.25 minutes.

### 9.4 Shift comparison

| Shift | Observed downtime |
|---|---:|
| Morning | 1,060 minutes |
| Evening | 935 minutes |
| Night | 800 minutes |

These are observed descriptive comparisons within the synthetic dataset. They must not be generalized to other factories, machines, or operating environments.

## 10. Grounded Assistant Operation

The assistant supports deterministic responses based on approved analytical results.

### 10.1 Operating modes

- Mode A: deterministic guided answers.
- Mode B: deterministic retrieval with optional bounded Gemini natural-language explanation.

The deterministic result and its evidence remain authoritative.

### 10.2 Gemini configuration

The backend may use the following environment variables:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`

Configure secrets only through the authorized deployment or local environment settings.

Never paste API keys into source files, this guide, terminal screenshots, GitHub discussions, or evidence reports.

### 10.3 Assistant safety boundaries

The assistant must not:
- Recalculate approved rankings or scores.
- Invent numerical findings.
- Claim causal relationships or predictive certainty.
- Execute arbitrary SQL or user-supplied code.
- Read the canonical CSV directly as an unrestricted assistant data source.
- Expose secrets, internal prompts, or unrestricted records.
- Treat instructions embedded in evidence as trusted instructions.

When Gemini is unavailable, invalid, or times out, the deterministic answer remains authoritative and the approved fallback behavior applies.

Refer to:

- `docs/ASSISTANT_ARCHITECTURE.md`
- `docs/ASSISTANT_QUERY_CONTRACT.md`
- `docs/ASSISTANT_SAFETY_AND_SCOPE.md`
- `docs/PHASE3_LIVE_GEMINI_VERIFICATION_REPORT.md`

## 11. Validation and Test Reports

The following reports provide the recorded technical validation evidence.

| Report | Purpose |
|---|---|
| `docs/PHASE3_CLEAN_CLONE_VALIDATION_REPORT.md` | Independent clean-clone validation |
| `docs/PHASE3_CANONICAL_DATA_VALIDATION_REPORT.md` | Canonical dataset validation |
| `docs/PHASE3_DATA_READINESS_REVALIDATION_REPORT.md` | Data readiness and analytical eligibility |
| `docs/PHASE3_ANALYTICAL_REGENERATION_REPORT.md` | Analytical reproducibility and contract validation |
| `docs/PHASE3_AUTOMATED_TEST_REPORT.md` | Consolidated automated test results |
| `docs/PHASE3_FINAL_SELENIUM_REPORT.md` | Final Selenium journey |
| `docs/PHASE3_POST6_FINAL_UAT_REPORT.md` | Final technical UAT |
| `docs/PHASE3_POST6_DEPLOYMENT_VALIDATION_REPORT.md` | Production endpoint validation |
| `docs/PHASE3_POST6_CONTAINER_VALIDATION_REPORT.md` | Docker configuration and container validation |
| `docs/FINAL_OPERATIONAL_REGRESSION_REPORT.md` | Phase 2 operational regression |
| `docs/FINAL_DATA_INTELLIGENCE_VALIDATION.md` | Data Intelligence validation |
| `docs/PHASE3_LIVE_GEMINI_VERIFICATION_REPORT.md` | Live assistant verification |

### 11.1 Automated test result

The consolidated Post #6 automated suite recorded:

- 64 tests passed.
- 0 test failures.
- 1 warning.

The warning concerns the Starlette test-client use of `httpx` and its deprecation notice.

The historical `tests/test_poc.py` was inspected and excluded from the consolidated current suite because it contains outdated expectations and URLs.

Refer to `docs/PHASE3_AUTOMATED_TEST_REPORT.md` for exact scope and results.

### 11.2 Selenium and browser evidence

The final journey verifies navigation between:
- Operational Dashboard.
- Data Intelligence.
- Return to Operational Dashboard.

The UAT report records additional checks for filtering, empty results, error and retry behavior, mobile layout, and keyboard focus visibility.

A visible keyboard focus indicator was checked. This should not be interpreted as a complete independent accessibility audit.

## 12. Operational Troubleshooting

### 12.1 Docker API connection error

Example:

```text
failed to connect to the docker API
```

Possible cause: Docker Desktop is closed or its Linux engine is still starting.

Resolution:
1. Start Docker Desktop.
2. Wait for the engine to become ready.
3. Run `docker info`.
4. Inspect `docker compose ps -a`.
5. Start only the required project services after checking for port conflicts.

Do not interpret a stopped local Docker engine as a production outage.

### 12.2 Container exits unexpectedly

Inspect:

```powershell
docker compose ps -a
```

Inspect backend logs:

```powershell
docker compose logs --tail 100 backend
```

Inspect frontend logs:

```powershell
docker compose logs --tail 100 frontend
```

Review the error before changing configuration or rebuilding images.

### 12.3 Port conflict

Check running container port mappings:

```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Do not stop unrelated project containers without authorization.

### 12.4 Backend health failure

Check:
- Backend container status.
- Backend logs.
- Port 8000 mapping.
- Backend startup configuration.

Use `/health` to verify backend health.

### 12.5 Frontend route failure

Check:
- Frontend container status.
- Frontend logs.
- Port 3000 mapping.
- Frontend API configuration.
- Backend availability.

Test the root route and `/data-intelligence` separately.

### 12.6 Data Intelligence contract failure

Check:
- Approved JSON output files.
- Data and method versions.
- Metadata and quality status.
- Backend loader and contract validation logs.

Do not create replacement results manually or bypass contract validation.

### 12.7 Assistant fallback

If the assistant cannot provide an optional Gemini explanation:
- Preserve the deterministic result.
- Check authorized backend configuration.
- Check service availability and application logs.
- Do not expose secret values.
- Do not replace a deterministic result with an unsupported generated answer.

## 13. Evidence Pack

The final evidence pack uses the following required structure:

```text
final-evidence/
├── 01-release/
├── 02-clean-clone/
├── 03-data-foundation/
├── 04-data-readiness/
├── 05-analytical-validation/
├── 06-intelligence-contract/
├── 07-operational-regression/
├── 08-data-intelligence/
├── 09-assistant-or-skip/
├── 10-automated-tests/
├── 11-selenium/
├── 12-uat/
├── 13-deployment/
├── 14-screenshots/
└── 15-handover/
```

The evidence README is:

`final-evidence/README.md`

The evidence pack contains reports, test results, deployment and container evidence, and screenshots. Its final inventory and release identity must be reconciled before certification.

Do not describe the evidence pack as finally certified until the remaining release and reviewer activities are complete.

## 14. Security and Data Boundaries

The public demo uses synthetic data.

The inspected safety documentation identifies that existing incident endpoints and CSV/JSON exports are public and unpaginated. This is a known exposure consideration for any future use of real or restricted data.

Before introducing real operational data:
- Perform a separate security and privacy review.
- Review API access controls and pagination.
- Review data minimization and retention.
- Review logging and error responses.
- Reassess assistant retrieval and evidence boundaries.
- Ensure secrets remain server-side.
- Obtain the required organizational approval.

Do not upload confidential company records into this public synthetic demonstration.

## 15. Known Limitations

The following limitations must remain visible to reviewers and future maintainers:

1. The canonical dataset is synthetic.
2. Findings are descriptive and group-level.
3. Results do not establish causation or predict future failures.
4. Small group sizes limit generalization.
5. Gemini explanations are optional and cannot override deterministic results.
6. The approved output package has a recorded generation timestamp of `2026-11-07T09:53:54Z`; the stale-data warning is expected and must not be hidden.
7. The consolidated automated suite recorded one Starlette/httpx deprecation warning.
8. The legacy `tests/test_poc.py` contains outdated expectations and is not part of the current consolidated suite.
9. The local container verification establishes startup and HTTP route availability, not a full local browser interaction test.
10. A complete independent accessibility audit has not been established by the recorded keyboard focus check.
11. The deployed source commit and Render build identity were not independently verified in the deployment validation report.
12. Final GitHub submission and reviewer certification remain pending.

## 16. Maintenance and Change Management

Any future change to the application must preserve the approved Post #4 and Post #5 behavior unless a separately authorized change is approved.

Before changing analytical logic or source data:
1. Identify the approved source and contract.
2. Obtain the required review and authorization.
3. Update the relevant version metadata.
4. Regenerate outputs only through the approved analytical process.
5. Run independent validation.
6. Verify API and UI compatibility.
7. Update affected reports and evidence.
8. Reassess the release identity.

Do not edit approved output JSON manually to change a displayed finding.

Do not silently change the data version or method version.

Do not trigger a production deployment during routine handover.

## 17. Handover Checklist and Current Status

| Item | Status |
|---|---|
| Project and application overview documented | Recorded |
| Production URLs documented | Recorded |
| Render configuration documented | Recorded |
| Docker Compose configuration documented | Recorded |
| Local Docker engine recovery | PASS — 18 November 2026 |
| Phase 3 backend and frontend containers | PASS — running |
| Local backend health | PASS — healthy |
| Local Operational Dashboard route | PASS — HTTP 200 |
| Local Data Intelligence route | PASS — HTTP 200 |
| Approved data and method versions documented | Recorded |
| Assistant boundaries documented | Recorded |
| Test and validation report references documented | Recorded |
| Known limitations documented | Recorded |
| Evidence pack references documented | Recorded |
| Final release manifest reconciliation | Pending |
| Root README final update | Prepared — final consistency check pending |
| Final Repomix | Pending |
| Release tag | Pending authorization and release identity reconciliation |
| GitHub submission | Pending authorization |
| Reviewer signoff | Pending |

### Final handover status

**TECHNICAL HANDOVER GUIDE DRAFTED — FINAL CERTIFICATION PENDING**

The local Docker recovery and endpoint checks passed on 18 November 2026.

This result does not independently certify the full Phase 3 release. The remaining certification activities must be completed in the prescribed Post #6 sequence, and final approval must be recorded by the authorized reviewer.

The final certification result must be one of the approved outcomes:

- `PHASE 3 COMPLETE — CERTIFIED`
- `PHASE 3 FINAL CHANGES REQUIRED`
- `PHASE 3 CERTIFICATION BLOCKED`

No final outcome is assigned by this draft guide.

---

**Document:** `docs/PHASE3_HANDOVER_GUIDE.md`  
**Project:** POC-21 — Downtime Root Cause Explorer  
**Purpose:** Technical handover and final certification reference