"""Copy the application's synthetic CSV into a normalized source sample."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "synthetic" / "downtime_incidents.csv"
OUTPUT = ROOT / "data" / "source-sample" / "source_sample.csv"


def main():
    if not SOURCE.is_file():
        raise SystemExit(f"Source dataset not found: {SOURCE}")

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)

    if not fields or not rows:
        raise SystemExit("Source CSV must contain a header and data rows.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Extracted {len(rows)} source records to "
        f"{OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()