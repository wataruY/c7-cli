# c7-cli

Context7 MCP CLI tools project

## Development Environment

- Python: 3.12
- Package Manager: uv

## Setup

### Prerequisites

- Python 3.12
- uv package manager
- lefthook (for git hooks)

### Installation

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv sync
```

3. Install git hooks:
```bash
lefthook install
```

## Development

### Code Quality Tools

- **Format**: ruff
- **Lint**: ruff, mypy
- **Test**: pytest, pytest-asyncio

### Running Tools Manually

Format code:
```bash
uv run ruff format .
```

Lint code:
```bash
uv run ruff check .
uv run mypy .
```

Run tests:
```bash
uv run pytest
```

### Pre-commit Hooks

Pre-commit hooks are automatically run via lefthook when committing:
- Code formatting (ruff format)
- Linting (ruff check, mypy)

## CI/CD

GitHub Actions workflow runs on every push and pull request:
- Code formatting check
- Linting
- Type checking
- Tests

## Project Structure

```
c7-cli/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── c7_cli/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .gitignore
├── CLAUDE.md
├── lefthook.yml
├── pyproject.toml
└── README.md
```
