from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "canonical"
    / "intelligence_data.csv"
)


def load_downtime_data():
    """Reconstruct legacy-compatible incidents from canonical measurements."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Canonical dataset not found: {DATA_FILE}"
        )

    canonical_df = pd.read_csv(DATA_FILE)

    required_columns = [
        "record_type",
        "source_record_id",
        "observed_at",
        "entity_id",
        "category",
        "subcategory",
        "status",
        "metric_name",
        "metric_value",
        "text_value",
        "shift",
        "severity",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in canonical_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Canonical dataset is missing columns: "
            + ", ".join(missing_columns)
        )

    measurements = canonical_df[
        canonical_df["record_type"].astype(str).str.lower()
        == "measurement"
    ].copy()

    if measurements.empty:
        raise ValueError(
            "Canonical dataset contains no measurement records."
        )

    measurements["metric_value"] = pd.to_numeric(
        measurements["metric_value"],
        errors="coerce",
    )

    metric_table = measurements.pivot_table(
        index="source_record_id",
        columns="metric_name",
        values="metric_value",
        aggfunc="first",
    ).reset_index()

    descriptive_columns = [
        "source_record_id",
        "entity_id",
        "observed_at",
        "shift",
        "category",
        "subcategory",
        "severity",
        "status",
        "text_value",
    ]

    descriptions = (
        measurements[descriptive_columns]
        .drop_duplicates(subset=["source_record_id"])
    )

    incidents = descriptions.merge(
        metric_table,
        on="source_record_id",
        how="left",
    )

    expected_metrics = [
        "downtime_minutes",
        "failure_frequency",
    ]

    missing_metrics = [
        metric for metric in expected_metrics
        if metric not in incidents.columns
    ]

    if missing_metrics:
        raise ValueError(
            "Canonical dataset is missing incident metrics: "
            + ", ".join(missing_metrics)
        )

    if incidents[expected_metrics].isna().any().any():
        raise ValueError(
            "One or more incidents are missing downtime or "
            "failure-frequency measurements."
        )

    incidents = incidents.rename(
        columns={
            "source_record_id": "incident_id",
            "entity_id": "machine_id",
            "observed_at": "incident_date",
            "category": "root_cause",
            "subcategory": "sub_cause",
            "text_value": "description",
        }
    )

    for column in [
        "shift",
        "root_cause",
        "sub_cause",
        "severity",
        "status",
    ]:
        incidents[column] = (
            incidents[column]
            .fillna("")
            .astype(str)
            .str.replace("_", " ", regex=False)
            .str.title()
        )

    incidents["incident_date"] = (
        pd.to_datetime(
            incidents["incident_date"],
            errors="coerce",
            utc=True,
        )
        .dt.strftime("%Y-%m-%d")
    )

    incidents["downtime_minutes"] = pd.to_numeric(
        incidents["downtime_minutes"],
        errors="coerce",
    ).fillna(0)

    incidents["failure_frequency"] = pd.to_numeric(
        incidents["failure_frequency"],
        errors="coerce",
    ).fillna(0)

    expected_columns = [
        "incident_id",
        "machine_id",
        "incident_date",
        "shift",
        "root_cause",
        "sub_cause",
        "downtime_minutes",
        "failure_frequency",
        "severity",
        "status",
        "description",
    ]

    incidents = incidents[expected_columns].copy()

    incidents = incidents.sort_values(
        by="incident_id"
    ).reset_index(drop=True)

    return incidents
