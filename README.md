# tokmon

[![PyPI version](https://img.shields.io/pypi/v/tokmon.svg)](https://pypi.org/project/tokmon/)
[![Python](https://img.shields.io/pypi/pyversions/tokmon.svg)](https://pypi.org/project/tokmon/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/naveenkumarbaskaran/tokmon/actions/workflows/ci.yml/badge.svg)](https://github.com/naveenkumarbaskaran/tokmon/actions)

**Know exactly what your LLM calls cost.** One decorator. Zero config.

```
pip install tokmon
```

## The Problem

You're building AI agents and you have **no idea** what they cost per request. Is it $0.01 or $0.50? Which tool call is the expensive one? You'll find out at the end of the month when the invoice arrives.

## The Solution

```python
import tokmon

@tokmon.track("search-agent")
def search_and_summarize(query: str) -> str:
    results = llm("Search for: " + query)         # tracked
    summary = llm("Summarize: " + results)         # tracked
    return summary

result = search_and_summarize("latest AI news")

# After the call:
print(tokmon.last_report())
# ┌─────────────────────────────────────────────────┐
# │ search-agent                                     │
# │ Calls: 2 | Tokens: 1,847 | Cost: $0.0042        │
# │ ├─ Call 1: 823 tok ($0.0018) — gpt-4o-mini      │
# │ └─ Call 2: 1024 tok ($0.0024) — gpt-4o-mini     │
# └─────────────────────────────────────────────────┘
```

That's it. One line added, full visibility.

## Features

### 🎯 Drop-in Decorator

```python
@tokmon.track("my-feature")
def any_function():
    # All LLM calls inside are automatically tracked
    ...
```

### 💰 Budget Alerts

```python
@tokmon.budget("expensive-agent", max_usd=1.00)
def expensive_agent(query):
    # Raises tokmon.BudgetExceeded if cost exceeds $1.00
    ...

# Or soft limit (warns but doesn't fail):
@tokmon.budget("agent", max_usd=0.50, hard=False)
def agent(query):
    ...
```

### 📊 Session Tracking

```python
# Track costs across an entire session
with tokmon.session("user-123") as s:
    agent.run("question 1")
    agent.run("question 2")
    agent.run("question 3")

print(s.total_cost_usd)     # $0.047
print(s.total_tokens)       # 12,483
print(s.call_count)         # 9
print(s.cost_per_call_usd)  # $0.0052
```

### 📈 Export & Reporting

```python
# JSON export for dashboards
tokmon.export_json("costs.json")

# CSV for spreadsheets
tokmon.export_csv("costs.csv")

# Print summary table
tokmon.print_report()
# ┌──────────────────┬───────┬──────────┬──────────┐
# │ Feature          │ Calls │ Tokens   │ Cost     │
# ├──────────────────┼───────┼──────────┼──────────┤
# │ search-agent     │ 142   │ 284,100  │ $0.89    │
# │ summarizer       │ 89    │ 156,200  │ $0.52    │
# │ classifier       │ 1,204 │ 120,400  │ $0.18    │
# └──────────────────┴───────┴──────────┴──────────┘
```

### 🖥️ CLI Dashboard

```bash
# Watch costs in real-time (requires: pip install tokmon[rich])
tokmon dashboard

# Show historical report
tokmon report --last 7d

# Set global budget alert
tokmon budget --daily 10.00 --alert slack
```

## Supported Providers

| Provider | Auto-Patch | Manual |
|----------|:----------:|:------:|
| OpenAI SDK | ✅ | ✅ |
| Anthropic SDK | ✅ | ✅ |
| LiteLLM | ✅ | ✅ |
| Any HTTP API | — | ✅ |

### Auto-patching (zero code changes)

```python
import tokmon
tokmon.auto_patch()  # Patches openai, anthropic, litellm automatically

# All subsequent LLM calls are tracked without any other changes
```

### Manual recording

```python
# If you use a custom client:
tokmon.record(
    feature="my-agent",
    model="gpt-4o",
    prompt_tokens=500,
    completion_tokens=200,
)
```

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                    Your Code                         │
│                                                     │
│   @tokmon.track("feature")                          │
│   def my_function():                                │
│       llm_call(...)  ←─── intercepted               │
│                                                     │
├─────────────────────────────────────────────────────┤
│                  tokmon Core                         │
│                                                     │
│   Interceptor → Counter → Store → Reporter          │
│       │              │        │         │           │
│   patches SDK    sums tokens  writes   formats      │
│                  + pricing    to log    output       │
└─────────────────────────────────────────────────────┘
```

## Configuration

```python
import tokmon

# Set custom pricing (override defaults)
tokmon.set_pricing("my-fine-tuned-model", prompt=5.00, completion=15.00)

# Set storage backend
tokmon.configure(storage="sqlite:///costs.db")  # or "memory", "json:costs.json"

# Set alert callback
tokmon.on_budget_exceeded(lambda report: slack.post(f"⚠️ {report}"))
```

## Zero Dependencies

Core `tokmon` has **zero dependencies**. Optional extras:
- `tokmon[rich]` — terminal dashboard with live updates
- `tokmon[openai]` — auto-patches OpenAI SDK
- `tokmon[litellm]` — auto-patches LiteLLM
- `tokmon[all]` — everything

## License

MIT
