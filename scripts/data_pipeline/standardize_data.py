"""Transform the approved source sample into the universal canonical schema."""
from pathlib import Path
import csv
import re
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT = ROOT / "data" / "canonical" / "intelligence_data.csv"
DATA_VERSION = "1.0.0"

MANDATORY_COLUMNS = [
    "record_id", "record_type", "observed_at", "entity_id",
    "related_entity_id", "entity_name", "category", "subcategory",
    "status", "stage", "metric_name", "metric_value", "metric_unit",
    "text_value", "latitude", "longitude", "source_name",
    "source_record_id", "is_synthetic", "data_version",
]
DOMAIN_COLUMNS = ["shift", "severity"]
COLUMNS = MANDATORY_COLUMNS + DOMAIN_COLUMNS

def normalize(value):
    return re.sub(r"\s+", "_", (value or "").strip().casefold())

def main():
    if not INPUT.is_file():
        raise SystemExit("Source sample missing; run extract_data.py first.")
    with INPUT.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        source_fields = reader.fieldnames or []
        source_rows = list(reader)

    required = [
        "incident_id", "machine_id", "incident_date", "shift", "root_cause",
        "sub_cause", "downtime_minutes", "failure_frequency", "severity",
        "status", "description",
    ]
    missing = [field for field in required if field not in source_fields]
    if missing:
        raise SystemExit("Source sample missing required fields: " + ", ".join(missing))

    output_rows = []
    seen_ids = set()
    for row in source_rows:
        incident_id = row["incident_id"].strip()
        if not incident_id:
            raise SystemExit("Empty incident_id found.")
        try:
            observed_at = date.fromisoformat(row["incident_date"].strip()).isoformat() + "T00:00:00Z"
        except ValueError as exc:
            raise SystemExit(f"Invalid incident_date for {incident_id}: {exc}")
        machine_id = row["machine_id"].strip()
        for metric_name, raw_value, unit, suffix in (
            ("downtime_minutes", row["downtime_minutes"], "minutes", "DOWNTIME"),
            ("failure_frequency", row["failure_frequency"], "count", "FREQUENCY"),
        ):
            try:
                number = float(raw_value)
            except (TypeError, ValueError):
                raise SystemExit(f"Non-numeric {metric_name} for {incident_id}: {raw_value!r}")
            if not number.is_integer():
                metric_value = str(number)
            else:
                metric_value = str(int(number))
            record_id = f"POC21-{incident_id}-{suffix}"
            if record_id in seen_ids:
                raise SystemExit(f"Duplicate canonical record_id: {record_id}")
            seen_ids.add(record_id)
            output_rows.append({
                "record_id": record_id,
                "record_type": "measurement",
                "observed_at": observed_at,
                "entity_id": machine_id,
                "related_entity_id": "",
                "entity_name": f"Machine {machine_id}",
                "category": normalize(row["root_cause"]),
                "subcategory": normalize(row["sub_cause"]),
                "status": normalize(row["status"]),
                "stage": "",
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_unit": unit,
                "text_value": (row["description"] or "").strip()[:500],
                "latitude": "",
                "longitude": "",
                "source_name": "synthetic_downtime_incidents_csv",
                "source_record_id": incident_id,
                "is_synthetic": "true",
                "data_version": DATA_VERSION,
                "shift": normalize(row["shift"]),
                "severity": normalize(row["severity"]),
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Standardized {len(source_rows)} incidents into {len(output_rows)} measurement rows.")

if __name__ == "__main__":
    main()
