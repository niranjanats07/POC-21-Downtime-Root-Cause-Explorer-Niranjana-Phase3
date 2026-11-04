"""Copy the application's current synthetic CSV into the controlled source sample."""
from pathlib import Path
import csv
import shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "synthetic" / "downtime_incidents.csv"
OUTPUT = ROOT / "data" / "source-sample" / "source_sample.csv"

def main():
    if not SOURCE.is_file():
        raise SystemExit(f"Source dataset not found: {SOURCE}")
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("Source CSV has no header.")
        rows = list(reader)
    if not rows:
        raise SystemExit("Source CSV contains no data rows.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"Extracted {len(rows)} source records to {OUTPUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
