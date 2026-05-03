"""Tests for tokmon tracker."""

from tokmon.tracker import TokenMonitor, budget, session, track


def test_monitor_session_lifecycle():
    monitor = TokenMonitor()
    s = monitor.start_session("test-feature")
    monitor.record_call("test-feature", "gpt-4o", 100, 50)
    monitor.end_session("test-feature")

    assert s.call_count == 1
    assert s.total_tokens == 150
    assert s.total_cost_usd > 0


def test_monitor_multiple_calls():
    monitor = TokenMonitor()
    monitor.start_session("multi")
    monitor.record_call("multi", "gpt-4o-mini", 200, 100)
    monitor.record_call("multi", "gpt-4o-mini", 300, 150)
    monitor.end_session("multi")

    history = monitor.history
    assert len(history) == 1
    assert history[0].call_count == 2
    assert history[0].total_tokens == 750


def test_track_decorator():
    @track("test-tracked")
    def my_func():
        return 42

    result = my_func()
    assert result == 42


def test_budget_decorator_passes():
    @budget("cheap", max_usd=10.0)
    def cheap_func():
        return "ok"

    assert cheap_func() == "ok"


def test_session_context_manager():
    with session("ctx-test") as s:
        pass  # No LLM calls in test

    assert s.call_count == 0
    assert s.total_cost_usd == 0.0


def test_session_report_summary():
    monitor = TokenMonitor()
    s = monitor.start_session("summary-test")
    monitor.record_call("summary-test", "gpt-4o", 500, 200)
    monitor.end_session("summary-test")

    summary = s.summary()
    assert summary["feature"] == "summary-test"
    assert summary["calls"] == 1
    assert summary["total_tokens"] == 700
    assert "cost_usd" in summary


def test_monitor_reset():
    monitor = TokenMonitor()
    monitor.start_session("x")
    monitor.end_session("x")
    assert len(monitor.history) == 1
    monitor.reset()
    assert len(monitor.history) == 0
