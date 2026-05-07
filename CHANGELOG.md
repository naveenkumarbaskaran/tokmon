# Changelog

## [2.0.0] - 2025-05-07

### Breaking Changes
- Development status upgraded to Production/Stable
- `litellm` optional dep bumped to >=1.40
- `pytest` dev dep bumped to >=8.0

### Added
- Async-compatible tracking with `pytest-asyncio` in dev
- Latest model pricing: GPT-4.1 family, o3, o4-mini, Gemini 2.5, Llama 4, DeepSeek v3/R1
- `Typing :: Typed` classifier
- `async` keyword for discoverability

### Improved
- Bumped `rich` optional to >=13.7 for better dashboard rendering
- Bumped `ruff` to >=0.5 for latest lint rules
- Expanded pricing database with 12 new models
- Better fuzzy model matching in pricing lookups

### Fixed
- `BudgetExceededError` message formatting for token-based budgets
- Edge case in `SessionReport.cost_per_call_usd` when session has zero calls

---

## [1.0.0] - 2025-03-01

### Added
- Stable core API: `track`, `budget`, `session` decorators/context managers
- Auto-patching for OpenAI and LiteLLM clients
- CSV and JSON export
- CLI with `tokmon report` and `tokmon dashboard`
- Rich terminal dashboard

### Improved
- Thread-safe session tracking
- Reduced memory overhead for long-running sessions

---

## [0.1.0] - 2025-01-10

### Added
- Initial release
- Decorator-based tracking (`@tokmon.track`)
- Budget enforcement (`@tokmon.budget`)
- In-memory store with export capabilities
- Model pricing database (OpenAI, Anthropic, Google, Meta, Mistral)
