# Context7 CLI Usage Guide

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd c7-cli

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Quick Start

### 1. Resolve a library name

```bash
c7 resolve react
```

Output:
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field     ┃ Value                ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ libraryId │ /facebook/react      │
│ version   │ 18.3.1               │
└───────────┴──────────────────────┘
```

### 2. Get documentation

```bash
c7 docs react
```

### 3. Search within documentation

```bash
c7 docs react --query "hooks"
```

### 4. Save documentation to file

```bash
c7 docs react --output react-docs.txt
```

## Advanced Usage

### Using API Key

For premium features and higher rate limits, set your API key:

```bash
export CONTEXT7_API_KEY="your-api-key"
c7 docs react
```

Or pass it as a flag:

```bash
c7 --api-key "your-api-key" docs react
```

### Get JSON output

```bash
c7 resolve react --json
c7 docs react --json
```

### Specify library version

```bash
c7 docs --library-id /facebook/react/18.0.0
```

## Python API Usage

You can also use Context7Client directly in your Python code:

```python
import asyncio
from context7_cli.mcp_client import Context7Client

async def main():
    async with Context7Client() as client:
        # Resolve library
        result = await client.resolve_library_id("react")
        print(result)

        # Get docs
        docs = await client.get_library_docs(library_name="react")
        print(docs)

asyncio.run(main())
```

## Examples

See the `examples/` directory for more usage examples:

- `basic_usage.py`: Basic API usage examples
- `batch_fetch.py`: Batch fetch documentation for multiple libraries

## Troubleshooting

### Command not found: c7

Make sure you've installed the package:

```bash
pip install -e .
```

### Connection errors

Ensure you have Node.js and npm installed:

```bash
node --version
npm --version
```

### Rate limiting

If you're hitting rate limits, get an API key at [context7.com/dashboard](https://context7.com/dashboard)

## Tips

1. **Pipe to tools**: Combine with other CLI tools
   ```bash
   c7 docs react | grep -i "hook"
   c7 docs pandas --json | jq '.content'
   ```

2. **Shell aliases**: Create shortcuts for frequently used commands
   ```bash
   alias c7d='c7 docs'
   alias c7r='c7 resolve'
   ```

3. **Batch operations**: Use in scripts
   ```bash
   for lib in react vue angular; do
       c7 docs $lib --output "${lib}-docs.txt"
   done
   ```

## Available Commands

| Command | Description |
|---------|-------------|
| `c7 resolve <library>` | Resolve library name to ID |
| `c7 docs <library>` | Get library documentation |
| `c7 tools` | List available MCP tools |
| `c7 version` | Show CLI version |

## Options

Global options (use before command):
- `--api-key TEXT`: Context7 API key
- `--server-command TEXT`: Custom MCP server command
- `--help`: Show help message

Command-specific options:
- `--json`: Output as JSON
- `--output, -o PATH`: Save to file
- `--query, -q TEXT`: Search query (for docs command)
- `--library-id TEXT`: Specify library ID directly
