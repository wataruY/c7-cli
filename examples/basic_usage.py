#!/usr/bin/env python3
"""
Basic usage examples for Context7 CLI Python API.

This demonstrates how to use the Context7Client programmatically
in your own Python scripts.
"""

import asyncio
from context7_cli.mcp_client import Context7Client


async def example_resolve_library():
    """Example: Resolve a library name to an ID."""
    print("=== Example 1: Resolve Library ===")

    async with Context7Client() as client:
        result = await client.resolve_library_id("react")
        print(f"Resolved 'react': {result}")


async def example_get_docs():
    """Example: Get documentation for a library."""
    print("\n=== Example 2: Get Documentation ===")

    async with Context7Client() as client:
        result = await client.get_library_docs(library_name="react")
        print(f"Documentation: {result}")


async def example_get_docs_with_query():
    """Example: Get documentation with a search query."""
    print("\n=== Example 3: Get Documentation with Query ===")

    async with Context7Client() as client:
        result = await client.get_library_docs(
            library_name="react",
            query="hooks"
        )
        print(f"Documentation (filtered): {result}")


async def example_list_tools():
    """Example: List available MCP tools."""
    print("\n=== Example 4: List Available Tools ===")

    async with Context7Client() as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


async def main():
    """Run all examples."""
    await example_resolve_library()
    await example_get_docs()
    await example_get_docs_with_query()
    await example_list_tools()


if __name__ == "__main__":
    asyncio.run(main())
