"""Model pricing database — cost per 1M tokens."""

from __future__ import annotations

# Pricing per 1M tokens (USD)
MODEL_PRICING: dict[str, dict[str, float]] = {
    # OpenAI
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4-turbo": {"prompt": 10.00, "completion": 30.00},
    "gpt-4": {"prompt": 30.00, "completion": 60.00},
    "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50},
    "o1": {"prompt": 15.00, "completion": 60.00},
    "o1-mini": {"prompt": 3.00, "completion": 12.00},
    "o3-mini": {"prompt": 1.10, "completion": 4.40},
    # Anthropic
    "claude-opus-4": {"prompt": 15.00, "completion": 75.00},
    "claude-sonnet-4": {"prompt": 3.00, "completion": 15.00},
    "claude-3-5-sonnet": {"prompt": 3.00, "completion": 15.00},
    "claude-3-5-haiku": {"prompt": 0.80, "completion": 4.00},
    "claude-3-haiku": {"prompt": 0.25, "completion": 1.25},
    "claude-3-opus": {"prompt": 15.00, "completion": 75.00},
    # Google
    "gemini-1.5-pro": {"prompt": 1.25, "completion": 5.00},
    "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
    "gemini-2.0-flash": {"prompt": 0.10, "completion": 0.40},
    # Meta (via API providers)
    "llama-3.1-70b": {"prompt": 0.35, "completion": 0.40},
    "llama-3.1-8b": {"prompt": 0.05, "completion": 0.08},
    # Mistral
    "mistral-large": {"prompt": 2.00, "completion": 6.00},
    "mistral-small": {"prompt": 0.20, "completion": 0.60},
    # Default fallback
    "_default": {"prompt": 1.00, "completion": 3.00},
}


def get_pricing(model: str) -> dict[str, float]:
    """Get pricing for a model, with fuzzy matching."""
    # Exact match
    if model in MODEL_PRICING:
        return MODEL_PRICING[model]

    # Fuzzy: find the longest matching key (most specific wins)
    model_lower = model.lower()
    best_key: str | None = None
    best_len = 0
    for key in MODEL_PRICING:
        if key != "_default" and key in model_lower and len(key) > best_len:
            best_key = key
            best_len = len(key)

    if best_key is not None:
        return MODEL_PRICING[best_key]

    return MODEL_PRICING["_default"]


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate cost in USD for given token usage."""
    pricing = get_pricing(model)
    prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
    completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]
    return prompt_cost + completion_cost


def set_pricing(model: str, prompt: float, completion: float) -> None:
    """Set custom pricing for a model (per 1M tokens)."""
    MODEL_PRICING[model] = {"prompt": prompt, "completion": completion}
