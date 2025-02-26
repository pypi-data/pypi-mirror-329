# x8-client

A Python client library for interacting with the x8 video processing API.

## Installation

```bash
pip install x8-client
```

## Basic Usage

```python
from x8 import APIClient

# Initialize the client
client = APIClient()

# Get articles without videos
articles = client.get_articles_not_made_video(age=7)

# Create a video for an article
from x8.models import Video
video = Video(
    unique_id=articles[0].unique_id,
    target_dir="/my-videos",
    channel_name="My Channel",
    is_vertical=True
)

result = client.make_video(video)
print(f"Video created: {result.video_url}")
```

## Configuration

Create a `.env` file in your project root:

```
API_BASE_URL=https://your-api-url.com
SECRET_KEY=your_secret_key
DEFAULT_TIMEOUT=30
DEFAULT_PAGE_SIZE=10
```

Alternatively, you can provide these values when initializing the client:

```python
client = APIClient(
    base_url="https://your-api-url.com",
    secret_key="your_secret_key"
)
```

## Testing

Run unit tests:
```bash
python run_tests.py
```

Run integration tests (requires API credentials):
```bash
python run_tests.py --integration
```

## License

[MIT](LICENSE)
