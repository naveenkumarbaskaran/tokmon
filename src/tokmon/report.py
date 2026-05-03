"""Reporting — formatted output for terminal."""

from __future__ import annotations

from tokmon.store import _global_store


def last_report() -> str:
    """Get the last session report as formatted string."""
    sessions = _global_store.get_all()
    if not sessions:
        return "No tracked sessions yet."

    last = sessions[-1]
    cost_str = f"${last['cost_usd']:.4f}"
    lines = [
        f"┌{'─' * 50}┐",
        f"│ {last['feature']:<48} │",
        f"│ Calls: {last['calls']} | Tokens: {last['total_tokens']:,} | "
        f"Cost: {cost_str}{' ' * max(0, 20 - len(cost_str))}│",
        f"└{'─' * 50}┘",
    ]
    return "\n".join(lines)


def print_report() -> None:
    """Print a summary table of all tracked features."""
    sessions = _global_store.get_all()
    if not sessions:
        print("No tracked sessions yet.")
        return

    # Aggregate by feature
    by_feature: dict[str, dict] = {}
    for s in sessions:
        feat = s["feature"]
        if feat not in by_feature:
            by_feature[feat] = {"calls": 0, "tokens": 0, "cost": 0.0}
        by_feature[feat]["calls"] += s["calls"]
        by_feature[feat]["tokens"] += s["total_tokens"]
        by_feature[feat]["cost"] += s["cost_usd"]

    # Print table
    header = f"{'Feature':<20} {'Calls':>6} {'Tokens':>10} {'Cost':>10}"

    print(f"┌{'─' * 52}┐")
    print(f"│ {header} │")
    print(f"├{'─' * 52}┤")
    for feat, data in sorted(by_feature.items()):
        row = f"│ {feat:<20} {data['calls']:>6} {data['tokens']:>10,} ${data['cost']:>8.4f} │"
        print(row)
    print(f"└{'─' * 52}┘")

    total_cost = sum(d["cost"] for d in by_feature.values())
    print(f"  Total: ${total_cost:.4f}")
