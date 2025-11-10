"""Integration tests for Context7 CLI.

These tests verify that the CLI can successfully:
1. Resolve library names to IDs
2. Fetch documentation content

These tests require Node.js and npm to be installed.
"""

import pytest
from context7_cli.mcp_client import Context7Client


@pytest.mark.asyncio
async def test_resolve_nextjs(api_key):
    """Test resolving Next.js library name to ID."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.resolve_library_id("next")

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "libraryId" in result, "Result should contain libraryId"

        # Verify library ID format
        library_id = result["libraryId"]
        assert library_id.startswith("/"), "Library ID should start with /"
        assert "next" in library_id.lower(), "Library ID should contain 'next'"

        print(f"\n✓ Resolved Next.js: {library_id}")


@pytest.mark.asyncio
async def test_resolve_react(api_key):
    """Test resolving React library name to ID."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.resolve_library_id("react")

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "libraryId" in result, "Result should contain libraryId"

        # Verify library ID format
        library_id = result["libraryId"]
        assert library_id.startswith("/"), "Library ID should start with /"
        assert "react" in library_id.lower(), "Library ID should contain 'react'"

        print(f"\n✓ Resolved React: {library_id}")


@pytest.mark.asyncio
async def test_resolve_vue(api_key):
    """Test resolving Vue.js library name to ID."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.resolve_library_id("vue")

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "libraryId" in result, "Result should contain libraryId"

        # Verify library ID format
        library_id = result["libraryId"]
        assert library_id.startswith("/"), "Library ID should start with /"

        print(f"\n✓ Resolved Vue.js: {library_id}")


@pytest.mark.asyncio
async def test_get_docs_nextjs(api_key):
    """Test fetching Next.js documentation."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.get_library_docs(library_name="next")

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should contain content"

        # Verify content is not empty
        content = result["content"]
        assert len(content) > 0, "Content should not be empty"
        assert isinstance(content, str), "Content should be a string"

        # Verify it's actually Next.js documentation
        content_lower = content.lower()
        assert "next" in content_lower, "Content should mention 'next'"

        print(f"\n✓ Fetched Next.js docs: {len(content)} characters")


@pytest.mark.asyncio
async def test_get_docs_react(api_key):
    """Test fetching React documentation."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.get_library_docs(library_name="react")

        # Verify the result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should contain content"

        # Verify content is not empty
        content = result["content"]
        assert len(content) > 0, "Content should not be empty"
        assert isinstance(content, str), "Content should be a string"

        # Verify it's actually React documentation
        content_lower = content.lower()
        assert "react" in content_lower, "Content should mention 'react'"

        print(f"\n✓ Fetched React docs: {len(content)} characters")


@pytest.mark.asyncio
async def test_get_docs_with_library_id(api_key):
    """Test fetching documentation using library ID directly."""
    async with Context7Client(api_key=api_key) as client:
        # First resolve to get the library ID
        resolve_result = await client.resolve_library_id("react")
        library_id = resolve_result["libraryId"]

        # Now fetch docs using the library ID
        result = await client.get_library_docs(library_id=library_id)

        # Verify the result
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should contain content"
        assert len(result["content"]) > 0, "Content should not be empty"

        print(f"\n✓ Fetched docs by ID ({library_id}): {len(result['content'])} characters")


@pytest.mark.asyncio
async def test_get_docs_with_query(api_key):
    """Test fetching documentation with a search query."""
    async with Context7Client(api_key=api_key) as client:
        result = await client.get_library_docs(
            library_name="react",
            query="hooks"
        )

        # Verify the result
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "content" in result, "Result should contain content"

        content = result["content"]
        assert len(content) > 0, "Content should not be empty"

        # The content should be filtered by the query
        content_lower = content.lower()
        assert "hook" in content_lower, "Content should mention 'hook'"

        print(f"\n✓ Fetched React docs with query 'hooks': {len(content)} characters")


@pytest.mark.asyncio
async def test_list_tools(api_key):
    """Test listing available MCP tools."""
    async with Context7Client(api_key=api_key) as client:
        tools = await client.list_tools()

        # Verify the result
        assert isinstance(tools, list), "Tools should be a list"
        assert len(tools) > 0, "Should have at least one tool"

        # Check for expected tools
        tool_names = [
            tool.get("name") if isinstance(tool, dict) else str(tool)
            for tool in tools
        ]

        assert "resolve-library-id" in tool_names, "Should have resolve-library-id tool"
        assert "get-library-docs" in tool_names, "Should have get-library-docs tool"

        print(f"\n✓ Listed {len(tools)} tools: {', '.join(tool_names)}")


@pytest.mark.asyncio
async def test_multiple_libraries_sequential(api_key):
    """Test resolving and fetching docs for multiple libraries."""
    libraries = ["react", "next", "vue"]

    async with Context7Client(api_key=api_key) as client:
        for lib_name in libraries:
            # Resolve
            resolve_result = await client.resolve_library_id(lib_name)
            assert "libraryId" in resolve_result

            # Fetch docs
            docs_result = await client.get_library_docs(library_name=lib_name)
            assert "content" in docs_result
            assert len(docs_result["content"]) > 0

            print(f"\n✓ Successfully processed {lib_name}")
