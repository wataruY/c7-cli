"""Tests for CLI commands.

These tests verify the CLI interface works correctly.
"""

import pytest
from click.testing import CliRunner
from context7_cli.cli import cli


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


def test_version_command(runner):
    """Test the version command."""
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "Context7 CLI version" in result.output


def test_resolve_command_missing_argument(runner):
    """Test resolve command without library name."""
    result = runner.invoke(cli, ["resolve"])
    assert result.exit_code != 0  # Should fail


def test_docs_command_missing_argument(runner):
    """Test docs command without library name or ID."""
    result = runner.invoke(cli, ["docs"])
    assert result.exit_code != 0  # Should fail
    assert "Error" in result.output


def test_tools_command_help(runner):
    """Test tools command help text."""
    result = runner.invoke(cli, ["tools", "--help"])
    assert result.exit_code == 0
    assert "List all available tools" in result.output


def test_resolve_command_help(runner):
    """Test resolve command help text."""
    result = runner.invoke(cli, ["resolve", "--help"])
    assert result.exit_code == 0
    assert "Resolve a library name" in result.output


def test_docs_command_help(runner):
    """Test docs command help text."""
    result = runner.invoke(cli, ["docs", "--help"])
    assert result.exit_code == 0
    assert "Get documentation" in result.output


def test_cli_help(runner):
    """Test main CLI help."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Context7 CLI" in result.output
    assert "resolve" in result.output
    assert "docs" in result.output
    assert "tools" in result.output
    assert "version" in result.output
