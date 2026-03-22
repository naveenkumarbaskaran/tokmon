"""CLI for tokmon — dashboard and reporting."""

from __future__ import annotations

import argparse
import sys

from tokmon.report import print_report
from tokmon.store import _global_store


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tokmon",
        description="LLM token & cost tracker",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Report command
    report_parser = subparsers.add_parser("report", help="Show cost report")
    report_parser.add_argument("--format", choices=["table", "json", "csv"], default="table")

    # Dashboard command
    subparsers.add_parser("dashboard", help="Live cost dashboard (requires rich)")

    # Budget command
    budget_parser = subparsers.add_parser("budget", help="Set budget alerts")
    budget_parser.add_argument("--daily", type=float, help="Daily budget in USD")

    args = parser.parse_args()

    if args.command == "report":
        print_report()
    elif args.command == "dashboard":
        _run_dashboard()
    elif args.command == "budget":
        print(f"Budget set: ${args.daily:.2f}/day" if args.daily else "No budget set")
    else:
        parser.print_help()


def _run_dashboard() -> None:
    """Run live dashboard (requires rich)."""
    try:
        from rich.console import Console  # type: ignore[import-untyped]
        from rich.table import Table  # type: ignore[import-untyped]

        console = Console()
        table = Table(title="tokmon — Cost Dashboard")
        table.add_column("Feature", style="cyan")
        table.add_column("Calls", justify="right")
        table.add_column("Tokens", justify="right")
        table.add_column("Cost", justify="right", style="green")

        for session in _global_store.get_all():
            table.add_row(
                session["feature"],
                str(session["calls"]),
                f"{session['total_tokens']:,}",
                f"${session['cost_usd']:.4f}",
            )

        console.print(table)
    except ImportError:
        print("Dashboard requires 'rich'. Install: pip install tokmon[rich]")
        sys.exit(1)


if __name__ == "__main__":
    main()
