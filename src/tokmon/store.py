"""Storage backend — memory, JSON, SQLite."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tokmon.tracker import SessionReport


@dataclass
class Store:
    """Simple in-memory store with export capabilities."""

    sessions: list[dict[str, Any]] = field(default_factory=list)
    _backend: str = "memory"

    def store_session(self, session: SessionReport) -> None:
        """Store a completed session."""
        self.sessions.append(session.summary())

    def get_all(self) -> list[dict[str, Any]]:
        return list(self.sessions)

    def reset(self) -> None:
        self.sessions.clear()


# Global store
_global_store = Store()


def configure(storage: str = "memory") -> None:
    """Configure storage backend.

    Args:
        storage: "memory", "json:path.json", or "sqlite:///path.db"
    """
    _global_store._backend = storage


def export_json(path: str | Path) -> None:
    """Export all tracked data to JSON."""
    data = {
        "version": 1,
        "sessions": _global_store.get_all(),
    }
    Path(path).write_text(json.dumps(data, indent=2, default=str))


def export_csv(path: str | Path) -> None:
    """Export all tracked data to CSV."""
    sessions = _global_store.get_all()
    if not sessions:
        Path(path).write_text("")
        return

    fieldnames = ["feature", "calls", "total_tokens", "prompt_tokens",
                  "completion_tokens", "cost_usd", "cost_per_call_usd", "duration_s"]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for session in sessions:
        writer.writerow(session)

    Path(path).write_text(output.getvalue())
