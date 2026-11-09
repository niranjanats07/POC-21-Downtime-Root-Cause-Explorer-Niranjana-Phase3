import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


# Make the backend application importable when pytest runs from the project root.
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import main
from app.intelligence import service


OUTPUT_DIR = PROJECT_ROOT / "data-science" / "outputs"
APPROVED_RESULTS = OUTPUT_DIR / "intelligence_results.json"
APPROVED_SUMMARY = OUTPUT_DIR / "intelligence_summary.json"


def write_test_package(tmp_path):
    """Copy approved outputs into a temporary test directory."""
    results = json.loads(
        APPROVED_RESULTS.read_text(encoding="utf-8")
    )
    summary = json.loads(
        APPROVED_SUMMARY.read_text(encoding="utf-8")
    )

    results_file = tmp_path / "intelligence_results.json"
    summary_file = tmp_path / "intelligence_summary.json"

    results_file.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )
    summary_file.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    return results_file, summary_file, results, summary


@pytest.fixture
def valid_package():
    """Load the approved package without modifying its source files."""
    return service.load_intelligence()


@pytest.fixture
def api_client(monkeypatch, valid_package):
    """Provide an API client using the approved intelligence package."""
    monkeypatch.setattr(
        main,
        "load_intelligence",
        lambda: valid_package,
    )

    return TestClient(main.app)


# ---------------------------------------------------------
# Contract and loader tests
# ---------------------------------------------------------

def test_loader_accepts_approved_package():
    package = service.load_intelligence()

    assert package["metadata"]["data_version"] == "1.1.0"
    assert package["metadata"]["method_version"] == "1.0.0"
    assert package["metadata"]["quality_status"] == "PASS"
    assert len(package["results"]) == 11


def test_loader_rejects_missing_results_file(tmp_path, monkeypatch):
    _, summary_file, _, _ = write_test_package(tmp_path)

    monkeypatch.setattr(
        service,
        "RESULTS_FILE",
        tmp_path / "missing_results.json",
    )
    monkeypatch.setattr(
        service,
        "SUMMARY_FILE",
        summary_file,
    )

    with pytest.raises(OSError):
        service.load_intelligence()


def test_loader_rejects_invalid_json(tmp_path, monkeypatch):
    results_file, summary_file, _, _ = write_test_package(tmp_path)

    results_file.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    monkeypatch.setattr(service, "RESULTS_FILE", results_file)
    monkeypatch.setattr(service, "SUMMARY_FILE", summary_file)

    with pytest.raises(ValueError):
        service.load_intelligence()


def test_loader_rejects_mismatched_data_versions(
    tmp_path,
    monkeypatch,
):
    results_file, summary_file, _, summary = write_test_package(
        tmp_path
    )

    summary["data_version"] = "999.0.0"

    summary_file.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(service, "RESULTS_FILE", results_file)
    monkeypatch.setattr(service, "SUMMARY_FILE", summary_file)

    with pytest.raises(ValueError):
        service.load_intelligence()


def test_loader_rejects_negative_result_value(
    tmp_path,
    monkeypatch,
):
    results_file, summary_file, results, _ = write_test_package(
        tmp_path
    )

    results[0]["result_value"] = -10

    results_file.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(service, "RESULTS_FILE", results_file)
    monkeypatch.setattr(service, "SUMMARY_FILE", summary_file)

    with pytest.raises(ValueError):
        service.load_intelligence()


def test_loader_rejects_duplicate_result_ids(
    tmp_path,
    monkeypatch,
):
    results_file, summary_file, results, _ = write_test_package(
        tmp_path
    )

    results[1]["result_id"] = results[0]["result_id"]

    results_file.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(service, "RESULTS_FILE", results_file)
    monkeypatch.setattr(service, "SUMMARY_FILE", summary_file)

    with pytest.raises(ValueError):
        service.load_intelligence()


def test_loader_rejects_summary_result_count_mismatch(
    tmp_path,
    monkeypatch,
):
    results_file, summary_file, _, summary = write_test_package(
        tmp_path
    )

    summary["total_result_count"] = 999

    summary_file.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr(service, "RESULTS_FILE", results_file)
    monkeypatch.setattr(service, "SUMMARY_FILE", summary_file)

    with pytest.raises(ValueError):
        service.load_intelligence()


# ---------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------

def test_intelligence_summary_endpoint(api_client):
    response = api_client.get("/api/intelligence/summary")

    assert response.status_code == 200
    assert response.json()["total_result_count"] == 11


def test_intelligence_results_endpoint(api_client):
    response = api_client.get("/api/intelligence/results")

    assert response.status_code == 200
    assert len(response.json()) == 11


def test_intelligence_metadata_endpoint(api_client):
    response = api_client.get("/api/intelligence/metadata")

    assert response.status_code == 200

    metadata = response.json()

    assert metadata["data_version"] == "1.1.0"
    assert metadata["method_version"] == "1.0.0"
    assert metadata["quality_status"] == "PASS"


def test_intelligence_health_endpoint(api_client):
    response = api_client.get("/api/intelligence/health")

    assert response.status_code == 200

    health = response.json()

    assert health["status"] == "healthy"
    assert health["data_version"] == "1.1.0"
    assert health["method_version"] == "1.0.0"
    assert health["quality_status"] == "PASS"


def test_intelligence_result_detail_endpoint(api_client):
    response = api_client.get(
        "/api/intelligence/results/RES-0001"
    )

    assert response.status_code == 200
    assert response.json()["result_id"] == "RES-0001"


def test_unknown_intelligence_result_returns_404(api_client):
    response = api_client.get(
        "/api/intelligence/results/UNKNOWN-RESULT"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Intelligence result not found."
    )


def test_invalid_intelligence_package_returns_503(monkeypatch):
    def raise_invalid_package():
        raise ValueError("Test contract validation failure")

    monkeypatch.setattr(
        main,
        "load_intelligence",
        raise_invalid_package,
    )

    with TestClient(main.app) as client:
        response = client.get("/api/intelligence/health")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Data Intelligence data is unavailable or failed contract validation."
    )