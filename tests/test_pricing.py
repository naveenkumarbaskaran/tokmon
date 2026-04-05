"""Tests for tokmon pricing."""

from tokmon.pricing import calculate_cost, get_pricing, set_pricing


def test_known_model_pricing():
    pricing = get_pricing("gpt-4o")
    assert pricing["prompt"] == 2.50
    assert pricing["completion"] == 10.00


def test_unknown_model_fallback():
    pricing = get_pricing("totally-unknown-model")
    assert pricing == {"prompt": 1.0, "completion": 3.0}


def test_fuzzy_matching():
    pricing = get_pricing("openai/gpt-4o-mini-2024-07")
    assert pricing["prompt"] == 0.15


def test_calculate_cost():
    cost = calculate_cost("gpt-4o", prompt_tokens=1_000_000, completion_tokens=0)
    assert abs(cost - 2.50) < 0.01


def test_calculate_cost_completion():
    cost = calculate_cost("gpt-4o", prompt_tokens=0, completion_tokens=1_000_000)
    assert abs(cost - 10.00) < 0.01


def test_set_custom_pricing():
    set_pricing("my-model", prompt=5.0, completion=20.0)
    pricing = get_pricing("my-model")
    assert pricing["prompt"] == 5.0
    assert pricing["completion"] == 20.0


def test_cost_small_usage():
    cost = calculate_cost("gpt-4o-mini", prompt_tokens=100, completion_tokens=50)
    # 100/1M * 0.15 + 50/1M * 0.60 = 0.000015 + 0.00003 = 0.000045
    assert cost < 0.001
    assert cost > 0
