"""Integration tests for the x8 API client.

These tests make actual API calls and should only be run when specifically requested.
To run these tests: pytest -m integration
"""

import os
from datetime import datetime
import pytest
import requests

from x8.api_client import APIClient
from x8.models import Article, Video
from x8.config import API_BASE_URL, SECRET_KEY


# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration

@pytest.fixture
def real_api_client():
    """Create an APIClient instance using real credentials from .env."""
    # Skip all integration tests if credentials aren't set
    if not API_BASE_URL or API_BASE_URL == 'http://localhost:8080' or not SECRET_KEY or SECRET_KEY == 'default_secret_key':
        pytest.skip("API credentials not configured. Set API_BASE_URL and SECRET_KEY in .env file.")
    
    client = APIClient()
    
    # Test connectivity to the API
    try:
        # Just make a simple request to verify connectivity
        requests.get(f"{API_BASE_URL}/health", timeout=5)
    except requests.RequestException:
        pytest.skip("Could not connect to the API. Integration tests skipped.")
    
    return client

@pytest.fixture
def sample_article_data():
    """Generate sample article data for testing."""
    return {
        "unique_id": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "url": "http://integration-test.x8.example.com/article",
        "title": "Integration Test Article",
        "keywords": "integration, test, article",
        "description": "This is a test article for integration tests",
        "text_content": "Content for integration test article.",
        "src": "integration_test",
        "published_date": datetime.now(),
        "content_url": "http://integration-test.x8.example.com/content",
        "video_made": False,
        "img_url": "http://integration-test.x8.example.com/image.jpg"
    }

def test_get_articles(real_api_client):
    """Test fetching articles from the API."""
    articles = real_api_client._read_articles(size=3)
    
    assert isinstance(articles, list)
    assert len(articles) <= 3  # Should respect the size parameter
    
    if articles:  # If any articles were returned
        assert isinstance(articles[0], Article)
        assert articles[0].unique_id  # Should have a unique ID
        assert articles[0].title      # Should have a title

def test_get_articles_not_made_video(real_api_client):
    """Test fetching articles that haven't been processed into videos."""
    articles = real_api_client.get_articles_not_made_video(age=30)
    
    assert isinstance(articles, list)
    
    if articles:
        assert isinstance(articles[0], Article)
        assert articles[0].video_made is False
        assert articles[0].has_img is True  # This is implied by the method

@pytest.mark.xfail(reason="This test creates a real video and may take a long time or fail due to API limitations")
def test_make_video(real_api_client):
    """Test creating a video from an article.
    
    This test is marked as xfail because it makes a real video processing request
    which could be expensive, slow, or fail due to API quotas/limitations.
    """
    # First get an article without a video
    articles = real_api_client.get_articles_not_made_video(age=7)
    
    if not articles:
        pytest.skip("No articles available for video creation")
    
    article = articles[0]
    
    # Create a video request
    video = Video(
        unique_id=article.unique_id,
        target_dir="/integration-test",
        article=article.unique_id,
        channel_name="Integration Test Channel",
        is_vertical=True
    )
    
    # Make the video - this might take a while and could fail for various reasons
    result = real_api_client.make_video(video)
    
    assert isinstance(result, Article)
    assert result.unique_id == article.unique_id
