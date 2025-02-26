"""API client for interacting with the video processing service."""

import logging
from typing import Dict, List, Optional, Any

import requests
from requests.exceptions import RequestException

from .config import API_BASE_URL, SECRET_KEY, DEFAULT_TIMEOUT, DEFAULT_PAGE_SIZE
from .exceptions import APIError, VideoProcessingError
from .models import Article, Video

logger = logging.getLogger(__name__)

class APIClient:
    """Client for interacting with the video processing API."""

    def __init__(self, base_url: str = API_BASE_URL, secret_key: str = SECRET_KEY) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL for the API
            secret_key: Authentication secret key
        """
        if not base_url:
            raise ValueError("API_BASE_URL is not configured")
        if not secret_key:
            raise ValueError("SECRET_KEY is not configured")
            
        self.base_url = f'{base_url}/api'
        self.secret_key = secret_key

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.

        Returns:
            Dictionary containing authorization and content-type headers
        """
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def _read_articles(
        self,
        page: int = 0,
        size: int = DEFAULT_PAGE_SIZE,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        src: Optional[str] = None,
        video_made: Optional[bool] = None,
        has_img: Optional[bool] = None,
        has_video: Optional[bool] = None,
        age: int = 0
    ) -> List[Article]:
        """Fetch articles from the API based on given filters.

        Args:
            page: Page number for pagination
            size: Number of items per page
            category: Filter by category
            tags: Filter by tags
            src: Filter by source
            video_made: Filter by video status
            has_img: Filter by image presence
            has_video: Filter by video presence
            age: Filter by age in days

        Returns:
            List of Article objects

        Raises:
            APIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() 
                 if k not in ['self'] and v is not None}
        
        try:
            response = requests.get(
                f"{self.base_url}/articles",
                headers=self._get_headers(),
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            return [Article(**article) for article in response.json()['data']]
        except RequestException as e:
            logger.error(f"Failed to fetch articles: {str(e)}")
            raise APIError(f"Failed to fetch articles: {str(e)}") from e

    def get_articles_not_made_video(
        self,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        age: int = 0
    ) -> List[Article]:
        """Get articles that haven't been processed into videos yet.

        Args:
            category: Optional category filter
            tags: Optional tags filter
            age: Maximum age of articles in days

        Returns:
            List of Article objects
        """
        return self._read_articles(
            video_made=False,
            category=category,
            tags=tags,
            has_img=True,
            age=age
        )

    def make_video(self, video: Video, included_long_video: bool = False) -> Article:
        """Process an article into a video.

        Args:
            video: Video object containing processing details
            included_long_video: Whether to include long video version

        Returns:
            Processed Article object

        Raises:
            VideoProcessingError: If video processing fails
        """
        url = f"{self.base_url}/video/ve8"
        params = {'included_long_video': included_long_video} if included_long_video else {}

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=video.to_dict(),
                params=params,
                timeout=DEFAULT_TIMEOUT
            )
            logger.info(f"[x8] Video processing response status: {response.status_code}")
            response.raise_for_status()
            logger.info(f"[x8] Video processing response: {response.json()}")
            
            # Create and return an Article object from the response
            response_data = response.json()
            return Article(**response_data)
            
        except RequestException as e:
            error_msg = f"Error making video for article: {video.unique_id}"
            logger.error(f"[x8] {error_msg} - {str(e)}")
            raise VideoProcessingError(f"{error_msg}: {str(e)}") from e
