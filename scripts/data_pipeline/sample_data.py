"""Apply deterministic, coverage-aware sampling only when the source exceeds limits."""
from pathlib import Path
import csv
import random
import tempfile
import os
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data" / "source-sample" / "source_sample.csv"
RANDOM_SEED = 42
MAX_ROWS = 10_000
STRATA = ["root_cause", "severity", "status", "shift"]

def main():
    if not SAMPLE.is_file():
        raise SystemExit("Source sample missing; run extract_data.py first.")
    with SAMPLE.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    if len(rows) <= MAX_ROWS:
        print(f"Retained all {len(rows)} records; no reduction required.")
        return

    usable = [field for field in STRATA if field in (fields or [])]
    if not usable:
        rng = random.Random(RANDOM_SEED)
        selected = rng.sample(rows, MAX_ROWS)
    else:
        groups = defaultdict(list)
        for row in rows:
            key = tuple((row.get(field) or "").strip().casefold() for field in usable)
            groups[key].append(row)
        rng = random.Random(RANDOM_SEED)
        keys = sorted(groups)
        # Allocate proportionally, initially preserving at least one row per stratum.
        if len(keys) > MAX_ROWS:
            raise SystemExit("More strata than the row limit; review sampling design.")
        quotas = {key: max(1, int(len(groups[key]) * MAX_ROWS / len(rows))) for key in keys}
        while sum(quotas.values()) > MAX_ROWS:
            candidates = [k for k in keys if quotas[k] > 1]
            if not candidates:
                break
            largest = max(candidates, key=lambda k: (quotas[k] - len(groups[k]) * MAX_ROWS / len(rows), quotas[k]))
            quotas[largest] -= 1
        while sum(quotas.values()) < MAX_ROWS:
            candidates = [k for k in keys if quotas[k] < len(groups[k])]
            if not candidates:
                break
            best = max(candidates, key=lambda k: (len(groups[k]) * MAX_ROWS / len(rows) - quotas[k], len(groups[k])))
            quotas[best] += 1
        selected = []
        for key in keys:
            selected.extend(rng.sample(groups[key], quotas[key]))
        rng.shuffle(selected)

    fd, temp_name = tempfile.mkstemp(prefix="source_sample_", suffix=".csv", dir=SAMPLE.parent)
    os.close(fd)
    try:
        with open(temp_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(selected)
        os.replace(temp_name, SAMPLE)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f"Sampled {len(selected)} of {len(rows)} records using seed {RANDOM_SEED}.")

if __name__ == "__main__":
    main()
