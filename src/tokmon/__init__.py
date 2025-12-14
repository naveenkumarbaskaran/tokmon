"""tokmon — Lightweight LLM token & cost tracker."""

from tokmon.tracker import TokenMonitor, track, budget, session
from tokmon.recorder import record
from tokmon.pricing import set_pricing, MODEL_PRICING
from tokmon.store import configure, export_json, export_csv
from tokmon.report import print_report, last_report
from tokmon.patch import auto_patch
from tokmon.exceptions import BudgetExceeded

__version__ = "0.1.0"
__all__ = [
    "track",
    "budget",
    "session",
    "record",
    "set_pricing",
    "MODEL_PRICING",
    "configure",
    "export_json",
    "export_csv",
    "print_report",
    "last_report",
    "auto_patch",
    "BudgetExceeded",
    "TokenMonitor",
]
