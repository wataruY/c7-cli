# c7-cli

Context7 MCP CLI tools project

## Features

- Python 3.12
- Package management with uv
- Code quality tools: ruff, mypy
- Testing with pytest and pytest-asyncio
- Pre-commit hooks with lefthook
- CI/CD with GitHub Actions

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://github.com/astral-sh/uv)
- [lefthook](https://github.com/evilmartians/lefthook)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/wataruY/c7-cli.git
cd c7-cli
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

See [CLAUDE.md](CLAUDE.md) for detailed development instructions.

## License

See [LICENSE](LICENSE) for details.
