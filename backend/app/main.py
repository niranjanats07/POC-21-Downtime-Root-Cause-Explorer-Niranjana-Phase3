import os
from io import StringIO

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.analytics.downtime import (
    calculate_dashboard_kpis,
    calculate_downtime_by_cause,
    calculate_downtime_by_machine,
    calculate_machine_shift_heatmap,
)
from app.data.loader import load_downtime_data
from app.intelligence.service import load_intelligence


app = FastAPI(
    title="Downtime Root Cause Explorer API",
    description="API for analysing downtime incidents, machines and root causes.",
    version="2.0.0",
)

# CORS configuration: allow local development and the deployed frontend.
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

frontend_origin = os.getenv("FRONTEND_ORIGIN")

if frontend_origin:
    allowed_origins.append(frontend_origin.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def filter_incidents(
    machine_id=None,
    shift=None,
    severity=None,
    root_cause=None,
    status=None,
):
    """Apply optional filters to incident records."""

    df = load_downtime_data()

    filters = {
        "machine_id": machine_id,
        "shift": shift,
        "severity": severity,
        "root_cause": root_cause,
        "status": status,
    }

    for column, value in filters.items():
        if value:
            df = df[
                df[column].astype(str).str.casefold()
                == value.casefold()
            ]

    return df


@app.get("/")
def home():
    return {
        "message": "Downtime Root Cause Explorer API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/dashboard/kpis")
def dashboard_kpis():
    return calculate_dashboard_kpis()


@app.get("/api/charts/pareto")
def pareto_chart():
    df = calculate_downtime_by_cause()
    return df.to_dict(orient="records")


@app.get("/api/charts/machine-downtime")
def machine_downtime():
    df = calculate_downtime_by_machine()
    return df.to_dict(orient="records")


@app.get("/api/charts/machine-shift-heatmap")
def machine_shift_heatmap():
    df = calculate_machine_shift_heatmap()
    return df.reset_index().to_dict(orient="records")


@app.get("/api/charts/frequency-duration")
def frequency_duration_chart():
    df = load_downtime_data()

    return df[
        [
            "incident_id",
            "machine_id",
            "failure_frequency",
            "downtime_minutes",
        ]
    ].to_dict(orient="records")


@app.get("/api/charts/root-cause-tree")
def root_cause_tree():
    df = load_downtime_data()

    result = (
        df.groupby(["root_cause", "sub_cause"])["downtime_minutes"]
        .sum()
        .reset_index()
    )

    return result.to_dict(orient="records")


@app.get("/api/incidents")
def get_all_incidents():
    return load_downtime_data().to_dict(orient="records")


@app.get("/api/incidents/filter")
def get_filtered_incidents(
    machine_id: str | None = None,
    shift: str | None = None,
    severity: str | None = None,
    root_cause: str | None = None,
    status: str | None = None,
):
    df = filter_incidents(
        machine_id=machine_id,
        shift=shift,
        severity=severity,
        root_cause=root_cause,
        status=status,
    )

    return df.to_dict(orient="records")


@app.get("/api/incidents/export/csv")
def export_incidents_csv(
    machine_id: str | None = None,
    shift: str | None = None,
    severity: str | None = None,
    root_cause: str | None = None,
    status: str | None = None,
):
    df = filter_incidents(
        machine_id=machine_id,
        shift=shift,
        severity=severity,
        root_cause=root_cause,
        status=status,
    )

    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=downtime_incidents.csv"
        },
    )


@app.get("/api/incidents/export/json")
def export_incidents_json(
    machine_id: str | None = None,
    shift: str | None = None,
    severity: str | None = None,
    root_cause: str | None = None,
    status: str | None = None,
):
    df = filter_incidents(
        machine_id=machine_id,
        shift=shift,
        severity=severity,
        root_cause=root_cause,
        status=status,
    )

    return df.to_dict(orient="records")


@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):
    df = load_downtime_data()

    incident = df[df["incident_id"] == incident_id]

    if incident.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Incident {incident_id} not found",
        )

    return incident.iloc[0].to_dict()


# -------------------------------------------------------------------
# Data Intelligence API
# -------------------------------------------------------------------

def _load_intelligence_or_http_error():
    try:
        return load_intelligence()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Data Intelligence data is unavailable or failed contract validation.",
        ) from exc

@app.get("/api/intelligence/summary")
def intelligence_summary():
    package = _load_intelligence_or_http_error()
    return package["summary"]


@app.get("/api/intelligence/results")
def intelligence_results():
    package = _load_intelligence_or_http_error()
    return package["results"]


@app.get("/api/intelligence/results/{result_id}")
def intelligence_result_detail(result_id: str):
    package = _load_intelligence_or_http_error()

    for result in package["results"]:
        if result.get("result_id") == result_id:
            return result

    raise HTTPException(
        status_code=404,
        detail="Intelligence result not found.",
    )

@app.get("/api/intelligence/metadata")
def intelligence_metadata():
    package = _load_intelligence_or_http_error()
    return package["metadata"]


@app.get("/api/intelligence/health")
def intelligence_health():
    package = _load_intelligence_or_http_error()

    return {
        "status": "healthy",
        "data_version": package["metadata"]["data_version"],
        "method_version": package["metadata"]["method_version"],
        "quality_status": package["metadata"]["quality_status"],
    }