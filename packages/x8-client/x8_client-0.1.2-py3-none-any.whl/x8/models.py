"""Models for article and video processing.

This module contains the data models used for handling articles and videos
in the content processing pipeline.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional, List, Any, Dict


@dataclass
class Article:
    """Represents an article with its metadata and processing status."""
    
    unique_id: str
    url: str
    title: str
    keywords: str
    description: str
    text_content: str
    src: str
    published_date: datetime
    content_url: str
    ai_category: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_category2: Optional[str] = None
    img_url: Optional[str] = None
    video_made: bool = False
    video_url: Optional[str] = None
    video_by: Optional[str] = None
    hl: Optional[str] = field(default=None)
    fb_posted: Optional[bool] = None
    related_articles: Optional[List[Any]] = None
    message: Optional[str] = None
    has_img: Optional[bool] = None  # Added missing field
    has_video: Optional[bool] = None  # Adding this for completeness
    
    def __post_init__(self):
        """Perform post-initialization processing."""
        # If img_url is set but has_img is not, set has_img based on img_url
        if self.has_img is None:
            self.has_img = bool(self.img_url)
            
        # If video_url is set but has_video is not, set has_video based on video_url
        if self.has_video is None:
            self.has_video = bool(self.video_url)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the article instance to a dictionary."""
        return asdict(self)


@dataclass
class Video:
    """Represents a video with its processing metadata."""

    unique_id: str
    target_dir: Optional[str] = None
    article: Optional[str] = None
    channel_name: Optional[str] = None
    channel_id: Optional[str] = None
    is_vertical: bool = False
    ads: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the video instance to a dictionary."""
        return asdict(self)