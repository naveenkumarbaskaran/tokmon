"""Core tracker — decorator, budget, session context manager."""

from __future__ import annotations

import functools
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator

from tokmon.exceptions import BudgetExceeded
from tokmon.pricing import calculate_cost
from tokmon.store import _global_store


@dataclass
class CallRecord:
    """A single tracked LLM call."""

    feature: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class SessionReport:
    """Summary of a tracking session."""

    feature: str
    calls: list[CallRecord] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0

    @property
    def total_tokens(self) -> int:
        return sum(c.total_tokens for c in self.calls)

    @property
    def total_prompt_tokens(self) -> int:
        return sum(c.prompt_tokens for c in self.calls)

    @property
    def total_completion_tokens(self) -> int:
        return sum(c.completion_tokens for c in self.calls)

    @property
    def total_cost_usd(self) -> float:
        return sum(c.cost_usd for c in self.calls)

    @property
    def call_count(self) -> int:
        return len(self.calls)

    @property
    def cost_per_call_usd(self) -> float:
        return self.total_cost_usd / self.call_count if self.calls else 0.0

    @property
    def duration_s(self) -> float:
        return (self.end_time or time.time()) - self.start_time

    def summary(self) -> dict[str, Any]:
        return {
            "feature": self.feature,
            "calls": self.call_count,
            "total_tokens": self.total_tokens,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "cost_usd": round(self.total_cost_usd, 6),
            "cost_per_call_usd": round(self.cost_per_call_usd, 6),
            "duration_s": round(self.duration_s, 2),
        }


class TokenMonitor:
    """Central monitor that aggregates all tracking data."""

    def __init__(self) -> None:
        self._active_sessions: dict[str, SessionReport] = {}
        self._history: list[SessionReport] = []

    def start_session(self, feature: str) -> SessionReport:
        session = SessionReport(feature=feature)
        self._active_sessions[feature] = session
        return session

    def end_session(self, feature: str) -> SessionReport | None:
        session = self._active_sessions.pop(feature, None)
        if session:
            session.end_time = time.time()
            self._history.append(session)
            _global_store.store_session(session)
        return session

    def record_call(
        self,
        feature: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        duration_ms: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> CallRecord:
        cost = calculate_cost(model, prompt_tokens, completion_tokens)
        record = CallRecord(
            feature=feature,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )

        # Add to active session if exists
        if feature in self._active_sessions:
            self._active_sessions[feature].calls.append(record)

        return record

    @property
    def history(self) -> list[SessionReport]:
        return list(self._history)

    def total_cost(self) -> float:
        return sum(s.total_cost_usd for s in self._history)

    def reset(self) -> None:
        self._active_sessions.clear()
        self._history.clear()


# Global monitor instance
_monitor = TokenMonitor()


def track(feature: str) -> Callable[..., Any]:
    """Decorator: track all LLM calls within this function.

    Usage:
        @tokmon.track("my-feature")
        def my_function():
            ...
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _monitor.start_session(feature)
            try:
                result = func(*args, **kwargs)
            finally:
                _monitor.end_session(feature)
            return result
        return wrapper
    return decorator


def budget(
    feature: str,
    max_usd: float | None = None,
    max_tokens: int | None = None,
    hard: bool = True,
) -> Callable[..., Any]:
    """Decorator: track + enforce budget limits.

    Usage:
        @tokmon.budget("agent", max_usd=1.00)
        def expensive_agent():
            ...
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            session = _monitor.start_session(feature)
            try:
                result = func(*args, **kwargs)
            finally:
                _monitor.end_session(feature)

            # Check budget after execution
            if max_usd is not None and session.total_cost_usd > max_usd:
                if hard:
                    raise BudgetExceeded(feature, session.total_cost_usd, max_usd, "USD")

            if max_tokens is not None and session.total_tokens > max_tokens:
                if hard:
                    raise BudgetExceeded(
                        feature, float(session.total_tokens), float(max_tokens), "tokens"
                    )

            return result
        return wrapper
    return decorator


@contextmanager
def session(feature: str) -> Generator[SessionReport, None, None]:
    """Context manager: track a session.

    Usage:
        with tokmon.session("user-123") as s:
            agent.run("query")
        print(s.total_cost_usd)
    """
    report = _monitor.start_session(feature)
    try:
        yield report
    finally:
        _monitor.end_session(feature)
