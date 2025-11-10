"""Pytest configuration and fixtures."""

import pytest
import os


@pytest.fixture
def api_key():
    """Get API key from environment or use None for free tier."""
    return os.getenv("CONTEXT7_API_KEY")


@pytest.fixture
def sample_libraries():
    """Sample libraries to test with."""
    return [
        {
            "name": "react",
            "expected_org": "facebook",
        },
        {
            "name": "next",
            "expected_org": "vercel",
        },
        {
            "name": "vue",
            "expected_org": "vuejs",
        },
    ]
