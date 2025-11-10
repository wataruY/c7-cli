"""MCP client for Context7 server."""

import os
from typing import Any, Dict, Optional
from fastmcp import FastMCP


class Context7Client:
    """Client for interacting with Context7 MCP server."""

    def __init__(self, api_key: Optional[str] = None, server_command: Optional[str] = None):
        """
        Initialize Context7 MCP client.

        Args:
            api_key: Context7 API key (optional, can also use CONTEXT7_API_KEY env var)
            server_command: Custom server command (default: npx -y @upstash/context7-mcp)
        """
        self.api_key = api_key or os.getenv("CONTEXT7_API_KEY")

        # Default server command
        if server_command is None:
            server_command = "npx -y @upstash/context7-mcp"
            if self.api_key:
                server_command += f" --api-key {self.api_key}"

        self.server_command = server_command
        self.client: Optional[FastMCP] = None

    async def __aenter__(self):
        """Async context manager entry."""
        # Connect to the MCP server using stdio transport
        self.client = FastMCP(self.server_command)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def resolve_library_id(self, library_name: str) -> Dict[str, Any]:
        """
        Resolve a library name to a Context7-compatible library ID.

        Args:
            library_name: The name of the library/package to resolve

        Returns:
            Dictionary containing the resolution result
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use async context manager.")

        result = await self.client.call_tool(
            "resolve-library-id",
            {"libraryName": library_name}
        )
        return result

    async def get_library_docs(
        self,
        library_id: Optional[str] = None,
        library_name: Optional[str] = None,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get documentation for a library.

        Args:
            library_id: Library ID in format '/org/project' or '/org/project/version'
            library_name: Library name (will be resolved to ID first)
            query: Optional search query to filter documentation

        Returns:
            Dictionary containing the library documentation
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use async context manager.")

        # If library_name is provided but not library_id, resolve it first
        if library_name and not library_id:
            resolve_result = await self.resolve_library_id(library_name)
            # Extract library ID from resolution result
            if isinstance(resolve_result, dict) and "libraryId" in resolve_result:
                library_id = resolve_result["libraryId"]
            else:
                raise ValueError(f"Could not resolve library name: {library_name}")

        if not library_id:
            raise ValueError("Either library_id or library_name must be provided")

        params: Dict[str, Any] = {"libraryId": library_id}
        if query:
            params["query"] = query

        result = await self.client.call_tool("get-library-docs", params)
        return result

    async def list_tools(self) -> list:
        """
        List all available tools from the Context7 MCP server.

        Returns:
            List of available tools
        """
        if not self.client:
            raise RuntimeError("Client not connected. Use async context manager.")

        return await self.client.list_tools()
