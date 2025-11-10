#!/usr/bin/env python3
"""
Example: Batch fetch documentation for multiple libraries.

This script demonstrates how to fetch documentation for multiple
libraries and save them to separate files.
"""

import asyncio
import os
from pathlib import Path
from context7_cli.mcp_client import Context7Client


async def fetch_docs_for_libraries(libraries: list[str], output_dir: str = "docs_output"):
    """
    Fetch documentation for multiple libraries and save to files.

    Args:
        libraries: List of library names
        output_dir: Directory to save documentation files
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    async with Context7Client() as client:
        for library in libraries:
            print(f"Fetching documentation for {library}...")

            try:
                # Resolve library ID
                resolve_result = await client.resolve_library_id(library)
                print(f"  Resolved: {resolve_result}")

                # Get documentation
                docs_result = await client.get_library_docs(library_name=library)

                # Save to file
                output_file = output_path / f"{library.replace('/', '_')}.txt"

                # Extract content
                if isinstance(docs_result, dict):
                    content = docs_result.get("content", str(docs_result))
                else:
                    content = str(docs_result)

                with open(output_file, "w") as f:
                    f.write(f"# Documentation for {library}\n\n")
                    f.write(content)

                print(f"  Saved to {output_file}")

            except Exception as e:
                print(f"  Error fetching {library}: {e}")

    print(f"\nAll documentation saved to {output_dir}/")


async def main():
    """Main function."""
    # List of libraries to fetch
    libraries = [
        "react",
        "vue",
        "express",
        "fastapi",
        "@upstash/redis",
    ]

    await fetch_docs_for_libraries(libraries)


if __name__ == "__main__":
    asyncio.run(main())
