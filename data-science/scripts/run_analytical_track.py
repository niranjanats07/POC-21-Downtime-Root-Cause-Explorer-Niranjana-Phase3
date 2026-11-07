from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]

COMPARATIVE_SCRIPT = (
    ROOT
    / "data-science"
    / "scripts"
    / "run_comparative_intelligence.py"
)


def main():
    if not COMPARATIVE_SCRIPT.exists():
        raise FileNotFoundError(
            "Comparative intelligence script not found: "
            f"{COMPARATIVE_SCRIPT}"
        )

    print("POC-21 Analytical Track Runner")
    print("Track A - Comparative Intelligence")
    print()

    result = subprocess.run(
        [sys.executable, str(COMPARATIVE_SCRIPT)],
        cwd=str(ROOT),
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(result.returncode)

    print()
    print("Analytical Track A execution completed successfully.")


if __name__ == "__main__":
    main()