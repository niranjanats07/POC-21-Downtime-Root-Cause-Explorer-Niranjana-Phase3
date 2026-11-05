# POC-21 | Downtime Root Cause Explorer

**Infocreon Internship Project — Phase 3**

An interactive analytics project for exploring machinery downtime, investigating potential root causes, analysing machine performance, and establishing a reproducible Canonical Data Foundation.

---

## Project Overview

Downtime Root Cause Explorer is a web-based analytics application designed to help users analyse manufacturing downtime incidents and understand machine performance.

The project combines incident records, key performance indicators, interactive visualisations, filtering capabilities, and a reproducible canonical data pipeline to provide a structured view of downtime patterns and potential root causes.

---

## Key Features

- **Downtime Analytics:** View incident records and key performance indicators.
- **Machine Filtering:** Filter incident records by machine.
- **Interactive Visualisations:** Explore downtime patterns and machine performance through charts.
- **Root Cause Exploration:** Investigate incident details using the Intelligence Panel.
- **Data Export:** Export filtered incident data in CSV and JSON formats.
- **Canonical Data Foundation:** Standardise synthetic downtime incidents into a reproducible canonical dataset.
- **Data Validation:** Validate the canonical package, schema, records, and generated outputs.
- **Project Information:** View project and developer details.

---

## Technology Stack

| Component | Technologies |
|:---|:---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, Pandas, DuckDB |
| Visualisation | Apache ECharts, Plotly, D3.js |
| Data Tables | TanStack Table |
| Data Processing | Python, CSV, JSON |
| Containerisation | Docker, Docker Compose |
| Cloud Hosting | Render |
| Automated Testing | Selenium WebDriver 4, Python, Google Chrome |

---

# Project Setup

## Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend:

`http://localhost:8000`

### Frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

`http://localhost:3000`

---

## Run with Docker

**Prerequisites:** Docker Desktop and Docker Compose.

Build and start the application from the project root:

```bash
docker compose up --build -d
```

### Application Endpoints

| Service | Local URL |
|:---|:---|
| Frontend | `http://localhost:3000` |
| Backend API | `http://localhost:8000` |
| Backend Health Check | `http://localhost:8000/health` |

### Check Container Status

```bash
docker compose ps
```

### View Container Logs

```bash
docker compose logs
```

### Stop Containers

```bash
docker compose down
```

### Docker Validation

Local Docker validation covered application startup, API communication, dashboard loading, incident data, machine filters, charts, exports, and container restart behaviour.

---

# Live Deployment — Render

The application is hosted on Render using Docker-based deployment.

## Application URLs

| Service | Link |
|:---|:---|
| Frontend Dashboard | https://downtime-frontend.onrender.com/ |
| Backend API | https://downtime-backend.onrender.com/ |
| Backend Health Check | https://downtime-backend.onrender.com/health |

## Deployment Configuration

| Setting | Configuration |
|:---|:---|
| Hosting Platform | Render |
| Deployment Method | Docker |
| Git Branch | `main` |
| Region | Singapore |
| Frontend Health Check | `/` |
| Backend Health Check | `/health` |

Frontend and backend deployment, API communication, dashboard data loading, and service restart validation were completed successfully.

## Environment Variables

### Frontend

```env
NEXT_PUBLIC_API_URL=https://downtime-backend.onrender.com
```

### Backend

```env
FRONTEND_ORIGIN=https://downtime-frontend.onrender.com
```

---

# Selenium End-to-End Testing

Automated browser testing was performed against the live Render application using Selenium WebDriver 4, Python, and Google Chrome.

## Test Environment

| Configuration | Details |
|:---|:---|
| Framework | Selenium WebDriver 4 |
| Language | Python |
| Browser | Google Chrome |
| Test Script | `tests/test_poc.py` |
| Dependencies | `requirements-test.txt` |
| Test Target | Live Render deployment |

## Live URLs Tested

- **Frontend:** https://downtime-frontend.onrender.com/
- **Backend:** https://downtime-backend.onrender.com/
- **Health Endpoint:** https://downtime-backend.onrender.com/health

## Install Dependencies

Run from the repository root:

```bash
py -m pip install -r requirements-test.txt
```

## Execute Tests

```bash
py -u tests/test_poc.py
```

Run Chrome in visible browser mode using PowerShell:

```powershell
$env:HEADLESS="false"
py -u tests/test_poc.py
```

## Automated Test Coverage

The Selenium test suite validates:

1. Live application page loading.
2. Incident data retrieval and chart rendering.
3. Frontend-to-backend API communication.
4. Machine filtering and reset functionality.
5. Intelligence Panel interaction.
6. Project information and developer signature.
7. Responsive page-width validation at a 390px viewport.
8. Desktop and mobile screenshot capture.

## Latest Test Results

**Test Status: PASS — 8 Passed, 0 Failed**

| Metric | Result |
|:---|:---|
| Execution Date | 03 November 2026 |
| Execution Time | 05:37:43 UTC |
| Browser | Google Chrome |
| Tests Passed | 8 |
| Tests Failed | 0 |
| Backend API Status | HTTP 200 |
| Incident Records Retrieved | 10 |
| Mobile Viewport | 390px |

The responsive validation confirmed that the document and page widths remained within the 390px viewport. Some internal chart and table content may extend beyond the viewport.

---

# Phase 3 — Canonical Data Foundation

Phase 3 establishes a reproducible Canonical Data Foundation for the Downtime Root Cause Explorer.

The supplied source dataset is synthetic and is standardised into a canonical measurement structure for consistent validation and publication.

## Data Pipeline

The reproducible pipeline is available under:

`scripts/data_pipeline/`

Run the pipeline from the repository root:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
py scripts/data_pipeline/standardize_data.py
py scripts/data_pipeline/validate_data.py
py scripts/data_pipeline/publish_data.py
```

After publishing, validate the package again:

```powershell
python scripts/data_pipeline/validate_data.py
```

## Canonical Dataset

The Phase 3 dataset uses synthetic downtime incident data.

| Item | Result |
|:---|:---|
| Package Version | 1.1.0 |
| Synthetic Source Incidents | 30 |
| Source Sample Records | 30 |
| Canonical Measurement Records | 60 |
| Canonical Columns | 22 |
| Measurements per Source Incident | 2 |

Each source incident produces two canonical measurement records:

1. `downtime_minutes`
2. `failure_frequency`

The first 20 columns follow the mandatory canonical column order.

The additional domain-specific columns are:

- `shift`
- `severity`

## Canonical Data Files

| File | Purpose |
|:---|:---|
| `data/synthetic/downtime_incidents.csv` | Original synthetic source dataset |
| `data/source-sample/source_sample.csv` | Retained source sample |
| `data/canonical/intelligence_data.csv` | Canonical source of truth |
| `data/published/intelligence_data.json` | Published JSON generated from the canonical CSV |
| `data/schema.json` | Canonical field definitions |
| `data/manifest.json` | Package metadata |
| `data/quality/data_profile.json` | Canonical data profile |
| `data/quality/validation_report.json` | Canonical validation results |

## Sampling and Retention

The source dataset contains 30 synthetic incidents.

The complete source dataset was retained because the dataset was small enough to preserve without record reduction.

- Original records: **30**
- Records retained: **30**
- Records removed: **0**
- Original columns: **11**
- Source sample columns: **11**
- Sampling method: **Full-source retention**

No random or stratified sampling was required.

## Canonical Standardisation

The canonical standardisation process transforms each source incident into two measurement records.

The resulting canonical dataset contains:

- **60 canonical records**
- **22 canonical columns**
- `downtime_minutes` measurements
- `failure_frequency` measurements

The canonical CSV is the source of truth.

The published JSON is generated from the canonical CSV.

## Validation

Validate the canonical package using:

```powershell
python .\scripts\data_pipeline\validate_data.py
```

Current validation result:

```text
Canonical package validation PASSED.
Package version: 1.1.0
Canonical records: 60
Canonical columns: 22
```

The schema can also be checked with:

```powershell
python -m json.tool .\data\schema.json
```

## Phase 3 Documentation

Supporting documentation is available in:

- `docs/SAMPLING_AND_REDUCTION_REPORT.md`
- `docs/CANONICAL_DATA_PROFILE.md`
- `docs/DATA_ARCHETYPE_CONFIRMATION.md`
- `docs/DATA_QUALITY_ASSESSMENT.md`
- `docs/REPRESENTATIVENESS_ASSESSMENT.md`

These documents describe the canonical data structure, data archetype, sampling approach, data quality assessment, and representativeness considerations.

---

# Known Limitations

- The application and Phase 3 canonical dataset currently use synthetic downtime incident data.
- The dataset contains only 30 supplied synthetic source incidents and should not be interpreted as representative of real-world operational activity.
- Geographic coordinates are not available in the supplied source data.
- Render is used for cloud hosting.
- Selenium validation was performed against the live Render deployment.
- Some chart and table content may require horizontal scrolling on narrow screens.
- Manual reviewer confirmation of data classification and formal approval of the Canonical Data Foundation may still be required.

---

# Developer Information

| Detail | Information |
|:---|:---|
| Developer | Niranjana T Suresh |
| PoC ID | 21 |
| Organisation | Infocreon |
| Programme | Internship — Phase 3 |
| Batch | Batch 8 / MA College |
| GitHub | @niranjanats07 |

---

# Repository

**POC-21 — Downtime Root Cause Explorer | Phase 3**

---

<p align="center">
  <strong>POC-21 | DOWNTIME ROOT CAUSE EXPLORER</strong><br/>
  <sub>Manufacturing Downtime Analytics &amp; Root Cause Exploration</sub><br/>
  <sub>Infocreon Internship Programme — Phase 3</sub>
</p>