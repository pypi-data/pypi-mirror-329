"""Test fixtures for x8 client tests."""

import os
import sys
from pathlib import Path

# Add the project root to the path to make x8 importable
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from x8.api_client import APIClient

@pytest.fixture
def api_client():
    """Create an APIClient instance for testing."""
    return APIClient(
        base_url="http://test.example.com",
        secret_key="test_secret_key"
    )

@pytest.fixture
def mock_article_data():
    """Sample article data for testing."""
    return {
        "unique_id": "test123",
        "url": "http://example.com/article",
        "title": "Test Article",
        "keywords": "test, article",
        "description": "Test description",
        "text_content": "Test content",
        "src": "test_source",
        "published_date": "2023-01-01T00:00:00Z",
        "content_url": "http://example.com/content",
        "video_made": False
    }

@pytest.fixture
def mock_video_data():
    """Sample video data for testing."""
    return {
        "unique_id": "test123",
        "target_dir": "/test/dir",
        "article": "test_article",
        "channel_name": "test_channel",
        "is_vertical": False
    }
