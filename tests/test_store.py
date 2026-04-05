"""Tests for tokmon store and export."""

import json
from pathlib import Path

from tokmon.store import Store, export_json, export_csv, _global_store
from tokmon.tracker import TokenMonitor


def test_store_session(tmp_path: Path):
    monitor = TokenMonitor()
    s = monitor.start_session("store-test")
    monitor.record_call("store-test", "gpt-4o", 100, 50)
    monitor.end_session("store-test")

    store = Store()
    store.store_session(s)
    assert len(store.get_all()) == 1
    assert store.get_all()[0]["feature"] == "store-test"


def test_export_json(tmp_path: Path):
    _global_store.reset()
    monitor = TokenMonitor()
    s = monitor.start_session("json-test")
    monitor.record_call("json-test", "gpt-4o-mini", 200, 100)
    monitor.end_session("json-test")
    _global_store.store_session(s)

    path = tmp_path / "export.json"
    export_json(path)

    data = json.loads(path.read_text())
    assert data["version"] == 1
    assert len(data["sessions"]) >= 1


def test_export_csv(tmp_path: Path):
    _global_store.reset()
    monitor = TokenMonitor()
    s = monitor.start_session("csv-test")
    monitor.record_call("csv-test", "gpt-4o", 500, 250)
    monitor.end_session("csv-test")
    _global_store.store_session(s)

    path = tmp_path / "export.csv"
    export_csv(path)

    content = path.read_text()
    assert "feature" in content
    assert "csv-test" in content


def test_store_reset():
    store = Store()
    # Manually add data
    store.sessions.append({"feature": "x", "calls": 1})
    store.reset()
    assert len(store.get_all()) == 0
