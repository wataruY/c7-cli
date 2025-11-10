"""CLI interface for Context7 MCP client."""

import asyncio
import json
import os
import sys
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from .mcp_client import Context7Client


console = Console()


@click.group()
@click.option(
    "--api-key",
    envvar="CONTEXT7_API_KEY",
    help="Context7 API key (or set CONTEXT7_API_KEY env var)"
)
@click.option(
    "--server-command",
    help="Custom MCP server command"
)
@click.pass_context
def cli(ctx, api_key: Optional[str], server_command: Optional[str]):
    """
    Context7 CLI - Access up-to-date library documentation from your terminal.

    Get started by resolving a library or fetching docs:

        c7 resolve react

        c7 docs react

        c7 docs --library-id /facebook/react/18.0.0
    """
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = api_key
    ctx.obj["server_command"] = server_command


@cli.command()
@click.argument("library_name")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_context
def resolve(ctx, library_name: str, output_json: bool):
    """
    Resolve a library name to a Context7-compatible library ID.

    Example:

        c7 resolve react

        c7 resolve @upstash/redis
    """
    try:
        async def _resolve():
            async with Context7Client(
                api_key=ctx.obj["api_key"],
                server_command=ctx.obj["server_command"]
            ) as client:
                result = await client.resolve_library_id(library_name)

                if output_json:
                    console.print_json(data=result)
                else:
                    # Pretty print the result
                    if isinstance(result, dict):
                        table = Table(title=f"Resolved: {library_name}", show_header=True)
                        table.add_column("Field", style="cyan")
                        table.add_column("Value", style="green")

                        for key, value in result.items():
                            table.add_row(str(key), str(value))

                        console.print(table)
                    else:
                        console.print(result)

        asyncio.run(_resolve())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument("library_name", required=False)
@click.option("--library-id", help="Library ID in format '/org/project' or '/org/project/version'")
@click.option("--query", "-q", help="Search query to filter documentation")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--output", "-o", type=click.Path(), help="Save output to file")
@click.pass_context
def docs(
    ctx,
    library_name: Optional[str],
    library_id: Optional[str],
    query: Optional[str],
    output_json: bool,
    output: Optional[str]
):
    """
    Get documentation for a library.

    Examples:

        c7 docs react

        c7 docs --library-id /facebook/react/18.0.0

        c7 docs react --query "hooks"

        c7 docs react --output react-docs.txt
    """
    if not library_name and not library_id:
        console.print("[bold red]Error:[/bold red] Either LIBRARY_NAME or --library-id must be provided")
        sys.exit(1)

    try:
        async def _get_docs():
            async with Context7Client(
                api_key=ctx.obj["api_key"],
                server_command=ctx.obj["server_command"]
            ) as client:
                result = await client.get_library_docs(
                    library_id=library_id,
                    library_name=library_name,
                    query=query
                )

                # Format the output
                if output_json:
                    output_text = json.dumps(result, indent=2)
                else:
                    # Extract and format the documentation content
                    if isinstance(result, dict):
                        content = result.get("content", str(result))
                    else:
                        content = str(result)

                    output_text = content

                # Output to file or console
                if output:
                    with open(output, "w") as f:
                        f.write(output_text)
                    console.print(f"[green]Documentation saved to:[/green] {output}")
                else:
                    if output_json:
                        console.print_json(data=result)
                    else:
                        # Display with rich formatting
                        panel = Panel(
                            output_text,
                            title=f"📚 Documentation: {library_name or library_id}",
                            border_style="blue"
                        )
                        console.print(panel)

        asyncio.run(_get_docs())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def tools(ctx):
    """
    List all available tools from the Context7 MCP server.
    """
    try:
        async def _list_tools():
            async with Context7Client(
                api_key=ctx.obj["api_key"],
                server_command=ctx.obj["server_command"]
            ) as client:
                tools_list = await client.list_tools()

                table = Table(title="Available Context7 MCP Tools", show_header=True)
                table.add_column("Tool Name", style="cyan")
                table.add_column("Description", style="green")

                for tool in tools_list:
                    if isinstance(tool, dict):
                        name = tool.get("name", "Unknown")
                        description = tool.get("description", "No description")
                    else:
                        name = str(tool)
                        description = ""

                    table.add_row(name, description)

                console.print(table)

        asyncio.run(_list_tools())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@cli.command()
def version():
    """Show the version of Context7 CLI."""
    from . import __version__
    console.print(f"Context7 CLI version: [bold green]{__version__}[/bold green]")


def main():
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
