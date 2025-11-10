# Context7 CLI

A Python CLI frontend for the [Context7 MCP server](https://github.com/upstash/context7) that provides up-to-date library documentation directly in your terminal.

## Features

- 🔍 **Resolve library names** to Context7-compatible library IDs
- 📚 **Fetch documentation** for any supported library
- 🎯 **Search within docs** using query filters
- 💾 **Save documentation** to files
- 🎨 **Rich terminal output** with beautiful formatting
- 🔑 **API key support** for premium features

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js and npm (for running the Context7 MCP server via npx)

### Install from source

```bash
git clone <repository-url>
cd c7-cli
pip install -e .
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Basic Usage (Free Tier)

Resolve a library name:

```bash
c7 resolve react
```

Get documentation:

```bash
c7 docs react
```

### 2. With API Key (Premium)

Set your API key as an environment variable:

```bash
export CONTEXT7_API_KEY="your-api-key-here"
```

Or pass it directly:

```bash
c7 --api-key "your-api-key-here" docs react
```

Get your API key at [context7.com/dashboard](https://context7.com/dashboard)

## Commands

### `c7 resolve <library_name>`

Resolve a library name to a Context7-compatible library ID.

**Examples:**

```bash
# Resolve React
c7 resolve react

# Resolve Upstash Redis
c7 resolve @upstash/redis

# Get JSON output
c7 resolve react --json
```

### `c7 docs [library_name]`

Get documentation for a library.

**Options:**
- `--library-id`: Specify library ID directly (format: `/org/project` or `/org/project/version`)
- `--query, -q`: Search query to filter documentation
- `--json`: Output as JSON
- `--output, -o`: Save output to file

**Examples:**

```bash
# Get React documentation
c7 docs react

# Get documentation for a specific version
c7 docs --library-id /facebook/react/18.0.0

# Search for specific topics
c7 docs react --query "hooks"

# Save documentation to file
c7 docs react --output react-docs.txt

# Get JSON output
c7 docs react --json
```

### `c7 tools`

List all available tools from the Context7 MCP server.

```bash
c7 tools
```

### `c7 version`

Show the version of Context7 CLI.

```bash
c7 version
```

## Configuration

### Environment Variables

- `CONTEXT7_API_KEY`: Your Context7 API key (optional, for premium features)

### Custom Server Command

You can specify a custom MCP server command:

```bash
c7 --server-command "node /path/to/custom/server.js" docs react
```

## Use Cases

### 1. Quick Reference

Get quick documentation for a library you're working with:

```bash
c7 docs express --query "middleware"
```

### 2. Offline Documentation

Save documentation for offline reading:

```bash
c7 docs fastapi --output fastapi-docs.md
```

### 3. Integration with Scripts

Use in shell scripts or automation:

```bash
#!/bin/bash
# Get docs for multiple libraries
for lib in react vue angular; do
    c7 docs $lib --output "${lib}-docs.txt"
done
```

### 4. IDE Integration

Pipe documentation to your favorite tools:

```bash
c7 docs pandas --query "DataFrame" | less
```

## Architecture

The Context7 CLI consists of three main components:

1. **MCP Client** (`mcp_client.py`): Handles communication with the Context7 MCP server using the FastMCP library
2. **CLI Interface** (`cli.py`): Provides the user-facing command-line interface using Click
3. **Context7 MCP Server**: The backend server (runs via npx) that fetches up-to-date documentation

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│             │         │              │         │                 │
│  c7 CLI     │────────▶│  FastMCP     │────────▶│  Context7 MCP   │
│  (Python)   │         │  Client      │         │  Server (npx)   │
│             │         │              │         │                 │
└─────────────┘         └──────────────┘         └─────────────────┘
```

## Development

### Project Structure

```
c7-cli/
├── context7_cli/
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # CLI interface
│   └── mcp_client.py     # MCP client implementation
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

### Running Tests

Install test dependencies:

```bash
pip install -e ".[dev]"
```

Run all tests:

```bash
pytest
```

Run specific test files:

```bash
# CLI tests (no network required)
pytest tests/test_cli.py -v

# Integration tests (requires Node.js and network)
pytest tests/test_integration.py -v
```

Run tests with coverage:

```bash
pytest --cov=context7_cli --cov-report=html
```

### Code Formatting

```bash
black context7_cli/
```

### Continuous Integration

This project uses GitHub Actions for CI/CD. On every push to `main` or pull request:

1. **Tests** run on Python 3.10, 3.11, and 3.12
2. **Linting** checks code formatting with Black
3. **Type checking** with mypy
4. **Build** creates distribution packages

See `.github/workflows/ci.yml` for details.

## Troubleshooting

### Issue: "npx command not found"

Make sure Node.js and npm are installed:

```bash
node --version
npm --version
```

### Issue: "Client not connected"

This usually means the MCP server failed to start. Check:
1. Node.js is properly installed
2. You have internet connectivity (for npx to download the server)
3. The `@upstash/context7-mcp` package is accessible

### Issue: Rate limiting

If you're hitting rate limits, consider getting an API key for premium access at [context7.com/dashboard](https://context7.com/dashboard)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Links

- [Context7 MCP Server](https://github.com/upstash/context7)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Context7 Dashboard](https://context7.com/dashboard)
- [Upstash Blog: Introducing Context7](https://upstash.com/blog/context7-llmtxt-cursor)

## Acknowledgments

- Built on top of the [Context7 MCP server](https://github.com/upstash/context7) by Upstash
- Uses [FastMCP](https://github.com/jlowin/fastmcp) for MCP client functionality
- CLI powered by [Click](https://click.palletsprojects.com/)
- Terminal UI by [Rich](https://github.com/Textualize/rich)
