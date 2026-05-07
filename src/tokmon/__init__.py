"""tokmon — Lightweight LLM token & cost tracker."""

from tokmon.exceptions import BudgetExceededError
from tokmon.patch import auto_patch
from tokmon.pricing import MODEL_PRICING, set_pricing
from tokmon.recorder import record
from tokmon.report import last_report, print_report
from tokmon.store import configure, export_csv, export_json
from tokmon.tracker import TokenMonitor, budget, session, track

# Backward compatibility alias
BudgetExceeded = BudgetExceededError

__version__ = "2.0.0"
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
    "BudgetExceededError",
    "BudgetExceeded",  # backward compat
    "TokenMonitor",
]
