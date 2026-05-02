# Contributing to tokmon

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/naveenkumarbaskaran/tokmon.git
cd tokmon
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check .
ruff format .
```

## Making Changes

1. Fork the repo and create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Add or update tests for any new functionality
4. Ensure all tests pass and linting is clean
5. Open a pull request against `main`

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add Anthropic pricing model`
- `fix: handle missing usage field in response`
- `test: add budget overflow edge case`
- `docs: update CLI examples`

## Adding New Features

- **New model pricing** → add to `MODEL_PRICING` dict in `pricing.py`
- **New SDK patches** → add patch function in `patch.py`
- **New export formats** → extend `Store` class in `store.py`
- **New CLI commands** → add subparser in `cli.py`

## Updating Model Pricing

When adding or updating model prices:

1. Use official pricing from the provider's website
2. Prices are in USD per 1M tokens (`input_per_m`, `output_per_m`)
3. Add a comment with the source URL and date verified

## Reporting Issues

- Use GitHub Issues with a clear title and reproduction steps
- Include your Python version and SDK versions (openai, litellm)
- Attach minimal code that reproduces the problem

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
