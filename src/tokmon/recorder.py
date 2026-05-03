"""Manual recording API for custom LLM clients."""

from __future__ import annotations

from typing import Any

from tokmon.tracker import CallRecord, _monitor


def record(
    feature: str = "_default",
    model: str = "gpt-4o-mini",
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    duration_ms: float = 0.0,
    metadata: dict[str, Any] | None = None,
) -> CallRecord:
    """Manually record an LLM call.

    Usage:
        tokmon.record(
            feature="my-agent",
            model="gpt-4o",
            prompt_tokens=500,
            completion_tokens=200,
        )
    """
    return _monitor.record_call(
        feature=feature,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        duration_ms=duration_ms,
        metadata=metadata,
    )
