
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data/canonical/intelligence_data.csv"
OUTPUT_PATH = ROOT / "data-science/outputs/representativeness_assessment.json"


def parse_date(value):
    try:
        return datetime.fromisoformat(
            value.strip().replace("Z", "+00:00")
        )
    except (ValueError, TypeError, AttributeError):
        return None


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Canonical CSV not found: {CSV_PATH}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Canonical CSV is empty.")

    # Group measurement rows by source incident.
    incidents = {}
    for row in rows:
        source_id = row.get("source_record_id", "").strip()
        if source_id:
            incidents.setdefault(source_id, row)

    unique_incidents = list(incidents.values())

    def distribution(field):
        return dict(Counter(
            row.get(field, "").strip() or "(blank)"
            for row in unique_incidents
        ))

    synthetic_count = sum(
        row.get("is_synthetic", "").strip().lower() == "true"
        for row in unique_incidents
    )

    real_count = len(unique_incidents) - synthetic_count

    timestamps = [
        parsed
        for row in unique_incidents
        if (parsed := parse_date(row.get("observed_at", ""))) is not None
    ]

    observation_dates = sorted({
        timestamp.date().isoformat()
        for timestamp in timestamps
    })

    date_range = {
        "start": min(timestamps).isoformat() if timestamps else None,
        "end": max(timestamps).isoformat() if timestamps else None,
        "distinct_observation_dates": len(observation_dates),
        "observation_dates": observation_dates
    }

    machine_distribution = distribution("entity_id")
    category_distribution = distribution("category")
    shift_distribution = distribution("shift")
    severity_distribution = distribution("severity")
    status_distribution = distribution("status")

    geographic_pairs = set()
    for row in unique_incidents:
        latitude = row.get("latitude", "").strip()
        longitude = row.get("longitude", "").strip()

        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    geographic_pairs.add((lat, lon))
            except ValueError:
                pass

    all_closed = all(
        row.get("status", "").strip().lower() == "closed"
        for row in unique_incidents
    )

    all_synthetic = (
        len(unique_incidents) > 0
        and synthetic_count == len(unique_incidents)
    )

    blank_stage_count = sum(
        not row.get("stage", "").strip()
        for row in unique_incidents
    )

    blank_related_entity_count = sum(
        not row.get("related_entity_id", "").strip()
        for row in unique_incidents
    )

    # Sampling and population evidence
    sampling_assessment = {
        "sampling_method": "NOT_DOCUMENTED",
        "sampling_frame": "NOT_ESTABLISHED",
        "selection_procedure": "NOT_ESTABLISHED",
        "inclusion_probabilities": "NOT_AVAILABLE",
        "evidence": (
            "Canonical CSV and provenance fields identify source records "
            "but do not document a probability-sampling procedure or "
            "the method used to construct/select the synthetic incidents."
        )
    }

    population_assessment = {
        "source_population_size": "UNKNOWN",
        "eligible_machine_population": "UNKNOWN",
        "excluded_incident_count": "UNKNOWN",
        "population_coverage": "NOT_ESTABLISHED",
        "evidence": (
            "The available canonical dataset does not define the complete "
            "operational incident population or its sampling frame."
        )
    }

    # Coverage dimensions
    coverage_assessment = {
        "machine": {
            "observed_distribution": machine_distribution,
            "observed_machine_count": len(machine_distribution),
            "assessment": "LIMITED_SAMPLE_COVERAGE"
        },
        "category": {
            "observed_distribution": category_distribution,
            "assessment": "SAMPLE_DISTRIBUTION_ONLY"
        },
        "shift": {
            "observed_distribution": shift_distribution,
            "assessment": "SAMPLE_DISTRIBUTION_ONLY"
        },
        "severity": {
            "observed_distribution": severity_distribution,
            "assessment": "SAMPLE_DISTRIBUTION_ONLY"
        },
        "status": {
            "observed_distribution": status_distribution,
            "all_incidents_closed": all_closed,
            "assessment": (
                "CLOSED_ONLY"
                if all_closed else "OBSERVED_SAMPLE_ONLY"
            )
        },
        "temporal": {
            "date_range": date_range,
            "assessment": "SHORT_SYNTHETIC_OBSERVATION_PERIOD"
        },
        "geographic": {
            "valid_coordinate_pair_count": len(geographic_pairs),
            "assessment": (
                "NOT_ASSESSABLE"
                if not geographic_pairs else "LIMITED_SAMPLE_COVERAGE"
            )
        },
        "lifecycle_stage": {
            "blank_incident_count": blank_stage_count,
            "assessment": (
                "NOT_ASSESSABLE"
                if blank_stage_count == len(unique_incidents)
                else "LIMITED_SAMPLE_COVERAGE"
            )
        },
        "related_entity": {
            "blank_incident_count": blank_related_entity_count,
            "assessment": (
                "NOT_ASSESSABLE"
                if blank_related_entity_count == len(unique_incidents)
                else "LIMITED_SAMPLE_COVERAGE"
            )
        },
        "text": {
            "non_empty_text_incident_count": sum(
                bool(row.get("text_value", "").strip())
                for row in unique_incidents
            ),
            "assessment": "LIMITED_SYNTHETIC_TEXT_COVERAGE"
        }
    }

    underrepresented_areas = [
        {
            "area": "Real operational incidents",
            "evidence": f"{real_count} non-synthetic incidents.",
            "impact": "No real operational behaviour can be generalized."
        },
        {
            "area": "Source-population coverage",
            "evidence": "Population frame and sampling method are not established.",
            "impact": "Population representativeness cannot be measured."
        },
        {
            "area": "Machine population",
            "evidence": f"Only {len(machine_distribution)} observed machine identifiers.",
            "impact": "Coverage of the wider machine population is unknown."
        },
        {
            "area": "Geographic coverage",
            "evidence": f"{len(geographic_pairs)} valid coordinate pairs.",
            "impact": "Geographic comparisons are unavailable."
        },
        {
            "area": "Incident lifecycle",
            "evidence": (
                f"{blank_stage_count} incidents have no lifecycle stage; "
                f"{blank_related_entity_count} have no related entity."
            ),
            "impact": "Lifecycle and related-incident analysis are unsupported."
        },
        {
            "area": "Status coverage",
            "evidence": (
                "Only closed incidents are present."
                if all_closed else "Status distribution is limited to supplied records."
            ),
            "impact": "Open and in-progress status comparisons are unsupported."
        },
        {
            "area": "Long-term temporal behaviour",
            "evidence": (
                f"{len(observation_dates)} distinct observed dates."
            ),
            "impact": "Long-term trends and seasonality are unsupported."
        },
        {
            "area": "Rare and exceptional failures",
            "evidence": "Ten synthetic incidents; rare-event population coverage is unknown.",
            "impact": "Rare-event and anomaly conclusions are unreliable."
        },
        {
            "area": "Operational text diversity",
            "evidence": "Only the supplied synthetic incident descriptions are available.",
            "impact": "Text coverage of the wider operational vocabulary is unknown."
        }
    ]

    sampling_bias_risks = [
        {
            "risk": "Synthetic construction bias",
            "evidence": "All supplied incidents are synthetic.",
            "impact": "Synthetic distributions may not reflect real operations."
        },
        {
            "risk": "Selection bias",
            "evidence": "Sampling frame and selection method are not documented.",
            "impact": "Inclusion and exclusion effects cannot be evaluated."
        },
        {
            "risk": "Category and machine coverage imbalance",
            "evidence": "Only ten incidents and four observed machines.",
            "impact": "Observed distributions may not represent the wider population."
        },
        {
            "risk": "Temporal concentration",
            "evidence": "Observations cover a short January 2026 period.",
            "impact": "Seasonal and long-term behaviour may be missed."
        },
        {
            "risk": "Status restriction",
            "evidence": "All observed incidents are closed.",
            "impact": "Open and unresolved behaviour is absent."
        }
    ]

    mitigation = [
        "Obtain an authoritative source-population definition and sampling frame.",
        "Document the incident selection and synthetic-data construction method.",
        "Obtain authorized real operational records where available.",
        "Document machine-population and incident-category coverage.",
        "Extend temporal coverage across relevant operational cycles.",
        "Include relevant incident statuses and lifecycle stages.",
        "Collect valid geographic and relationship fields where meaningful and available.",
        "Assess rare and exceptional operating conditions.",
        "Reconcile canonical values against authoritative source samples.",
        "Do not fabricate missing canonical fields."
    ]

    limitations = [
        "All available incidents are synthetic.",
        "Only ten distinct source incidents are available.",
        "Two metric rows per incident are measurements, not independent incidents.",
        "Only four machine identifiers are represented.",
        "The sampling method and source population are not established.",
        "The dataset covers a short observation period.",
        "Only closed incidents are represented.",
        "No valid geographic coordinate pairs are available.",
        "Lifecycle-stage and related-entity coverage is absent.",
        "Category, shift and severity distributions describe this sample only.",
        "Source accuracy is not independently verified."
    ]

    result = {
        "source_file": "data/canonical/intelligence_data.csv",
        "canonical_measurement_rows": len(rows),
        "distinct_source_incidents": len(unique_incidents),
        "distinct_machines": len(machine_distribution),
        "date_range": date_range,
        "incident_distributions": {
            "machine": machine_distribution,
            "category": category_distribution,
            "shift": shift_distribution,
            "severity": severity_distribution,
            "status": status_distribution
        },
        "synthetic_incidents": synthetic_count,
        "real_incidents": real_count,
        "sampling_assessment": sampling_assessment,
        "source_population_assessment": population_assessment,
        "coverage_assessment": coverage_assessment,
        "underrepresented_areas": underrepresented_areas,
        "sampling_bias_assessment": {
            "status": "POTENTIAL_BIAS_RISKS_IDENTIFIED",
            "risks": sampling_bias_risks,
            "magnitude_and_direction": "NOT_ESTABLISHED"
        },
        "impact_on_analytical_use": [
            "Comparisons describe the supplied synthetic incidents only.",
            "Operational prevalence and performance estimates are unsupported.",
            "Trend and seasonality conclusions are unsupported.",
            "Geographic and lifecycle comparisons are unavailable.",
            "Predictive performance and causal conclusions are unsupported."
        ],
        "mitigation_and_required_improvements": mitigation,
        "limitations": limitations,
        "representativeness_status": (
            "INSUFFICIENT_FOR_OPERATIONAL_GENERALIZATION"
        ),
        "recommended_use": [
            "Pipeline and schema validation",
            "Synthetic-data analytical workflow testing",
            "Descriptive demonstration of recorded incident metrics"
        ],
        "not_supported": [
            "Claims about actual plant-wide incident prevalence",
            "Generalization to real machine failure patterns",
            "Seasonal or long-term trend conclusions",
            "Operational risk estimates",
            "Predictive modelling",
            "Causal root-cause conclusions",
            "Geographic intelligence"
        ]
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Representativeness assessment generated: {OUTPUT_PATH}")
    print(f"Measurement rows: {len(rows)}")
    print(f"Distinct incidents: {len(unique_incidents)}")
    print(f"Synthetic incidents: {synthetic_count}")
    print(f"Sampling method: {sampling_assessment['sampling_method']}")
    print(f"Valid coordinate pairs: {len(geographic_pairs)}")
    print(f"Underrepresented areas documented: {len(underrepresented_areas)}")
    print(f"Status: {result['representativeness_status']}")


if __name__ == "__main__":
    main()
