# YouTube Search SDK

A Python SDK for interacting with the YouTube Search API. This SDK provides a simple and intuitive interface to search for YouTube videos with various parameters.

## Features

- Simple and intuitive API
- Type hints and documentation
- Pydantic models for response validation
- Context manager support for proper resource cleanup
- Configurable API endpoint

## Installation

```bash
pip install youtube-search-sdk
```

## Quick Start

```python
from youtube_search_sdk import YouTubeSearchClient

# Create a client
client = YouTubeSearchClient(base_url="http://your-api-url:8000")

# Basic search
results = client.search("Python programming")

# Search with parameters
results = client.search(
    query="Python programming",
    limit=10,  # results per page (1-50)
    pages=2    # number of pages (1-10)
)

# Using context manager (recommended)
with YouTubeSearchClient() as client:
    results = client.search("Python programming")
    for video in results:
        print(f"Title: {video.title}")
        print(f"Channel: {video.channel_name}")
        print(f"Link: {video.link}")
        print("---")
```

## Response Structure

Each search result includes:

```python
class VideoResult:
    title: str
    channel_name: str
    duration: str
    views: str
    publish_date: Optional[datetime]
    link: str
    description: Optional[str]
    keywords: Optional[List[str]]
    page_number: int
```

## Error Handling

The SDK provides clear error messages for common issues:

```python
try:
    results = client.search("", limit=100)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except httpx.HTTPError as e:
    print(f"API request failed: {e}")
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-search-sdk
cd youtube-search-sdk

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 