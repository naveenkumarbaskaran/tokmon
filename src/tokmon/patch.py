"""Auto-patch LLM SDKs to track token usage transparently."""

from __future__ import annotations

import time
from typing import Any
from functools import wraps

from tokmon.tracker import _monitor


_patched = False


def auto_patch() -> None:
    """Monkey-patch supported LLM SDKs to auto-track token usage.

    Currently supports:
    - openai (ChatCompletion.create / client.chat.completions.create)
    - litellm (litellm.completion)
    """
    global _patched
    if _patched:
        return
    _patched = True

    _try_patch_openai()
    _try_patch_litellm()


def _try_patch_openai() -> None:
    """Attempt to patch the OpenAI SDK."""
    try:
        import openai  # type: ignore[import-untyped]

        original_create = openai.resources.chat.completions.Completions.create

        @wraps(original_create)
        def patched_create(self: Any, *args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = original_create(self, *args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            # Extract usage from response
            usage = getattr(result, "usage", None)
            if usage:
                model = getattr(result, "model", kwargs.get("model", "unknown"))
                _monitor.record_call(
                    feature="_auto",
                    model=model,
                    prompt_tokens=getattr(usage, "prompt_tokens", 0),
                    completion_tokens=getattr(usage, "completion_tokens", 0),
                    duration_ms=duration_ms,
                )

            return result

        openai.resources.chat.completions.Completions.create = patched_create  # type: ignore[assignment]
    except (ImportError, AttributeError):
        pass


def _try_patch_litellm() -> None:
    """Attempt to patch LiteLLM."""
    try:
        import litellm  # type: ignore[import-untyped]

        original_completion = litellm.completion

        @wraps(original_completion)
        def patched_completion(*args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = original_completion(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            # Extract usage
            usage = getattr(result, "usage", None)
            if usage:
                model = kwargs.get("model", args[0] if args else "unknown")
                _monitor.record_call(
                    feature="_auto",
                    model=str(model),
                    prompt_tokens=getattr(usage, "prompt_tokens", 0),
                    completion_tokens=getattr(usage, "completion_tokens", 0),
                    duration_ms=duration_ms,
                )

            return result

        litellm.completion = patched_completion  # type: ignore[assignment]
    except (ImportError, AttributeError):
        pass
