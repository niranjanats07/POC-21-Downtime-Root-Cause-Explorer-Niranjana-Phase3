import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ASSISTANT_ROOT = PROJECT_ROOT / "assistant"
CONFIG_ROOT = ASSISTANT_ROOT / "config"


def _read_config(filename):
    path = CONFIG_ROOT / filename
    if not path.is_file():
        raise RuntimeError(f"Assistant configuration missing: {filename}")
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def get_policy():
    return _read_config("assistant_policy.json")


def get_supported_intents():
    return _read_config("supported_intents.json")


def get_query_catalog():
    return _read_config("query_catalog.json")
