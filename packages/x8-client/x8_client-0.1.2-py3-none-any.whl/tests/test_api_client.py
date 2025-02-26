"""Tests for the APIClient class."""

import pytest
import requests
from x8.api_client import APIClient
from x8.exceptions import APIError, VideoProcessingError
from x8.models import Article, Video

def test_api_client_initialization(api_client):
    """Test APIClient initialization."""
    assert api_client.base_url == "http://test.example.com/api"
    assert api_client.secret_key == "test_secret_key"

def test_api_client_initialization_with_empty_values():
    """Test APIClient initialization with empty values."""
    with pytest.raises(ValueError, match="API_BASE_URL is not configured"):
        _ = APIClient(base_url="", secret_key="test")
    
    with pytest.raises(ValueError, match="SECRET_KEY is not configured"):
        _ = APIClient(base_url="http://test.com", secret_key="")

def test_get_headers(api_client):
    """Test header generation."""
    headers = api_client._get_headers()
    assert headers["Authorization"] == "Bearer test_secret_key"
    assert headers["Content-Type"] == "application/json"

def test_read_articles(requests_mock, api_client, mock_article_data):
    """Test article fetching."""
    requests_mock.get(
        "http://test.example.com/api/articles",
        json={"data": [mock_article_data]}
    )
    
    articles = api_client._read_articles(page=0, size=10)
    assert len(articles) == 1
    assert isinstance(articles[0], Article)
    assert articles[0].unique_id == mock_article_data["unique_id"]

def test_read_articles_error(requests_mock, api_client):
    """Test article fetching error handling."""
    requests_mock.get(
        "http://test.example.com/api/articles",
        status_code=500
    )
    
    with pytest.raises(APIError, match="Failed to fetch articles"):
        api_client._read_articles()

def test_get_articles_not_made_video(requests_mock, api_client, mock_article_data):
    """Test fetching articles without videos."""
    requests_mock.get(
        "http://test.example.com/api/articles",
        json={"data": [mock_article_data]}
    )
    
    articles = api_client.get_articles_not_made_video(
        category="test",
        tags="tag1",
        age=1
    )
    
    assert len(articles) == 1
    assert isinstance(articles[0], Article)
    
    # Verify correct parameters were sent
    history = requests_mock.request_history[0]
    assert "video_made=False" in history.url  # Changed from lowercase 'false' to Python's 'False'
    assert "has_img=True" in history.url
    assert "category=test" in history.url
    assert "tags=tag1" in history.url
    assert "age=1" in history.url

def test_make_video(requests_mock, api_client, mock_video_data, mock_article_data):
    """Test video creation."""
    requests_mock.post(
        "http://test.example.com/api/video/ve8",
        json=mock_article_data
    )
    
    video = Video(**mock_video_data)
    result = api_client.make_video(video, included_long_video=True)
    
    assert isinstance(result, Article)
    
    # Verify request
    history = requests_mock.request_history[0]
    assert "/video/ve8" in history.url
    assert "included_long_video=True" in history.url
    
    # Check that all mock_video_data fields are in the request JSON with correct values
    request_json = history.json()
    for key, value in mock_video_data.items():
        assert key in request_json
        assert request_json[key] == value

def test_make_video_error(requests_mock, api_client, mock_video_data):
    """Test video creation error handling."""
    requests_mock.post(
        "http://test.example.com/api/video/ve8",
        status_code=500
    )
    
    video = Video(**mock_video_data)
    with pytest.raises(VideoProcessingError, match=f"Error making video for article: {video.unique_id}"):
        api_client.make_video(video)
