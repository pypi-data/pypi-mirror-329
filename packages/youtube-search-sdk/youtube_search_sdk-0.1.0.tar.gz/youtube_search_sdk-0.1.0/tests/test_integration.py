"""
Integration tests for the YouTube Search SDK.
These tests require a running instance of the YouTube Search API.
"""

import os
import pytest
from datetime import datetime
from youtube_search_sdk import YouTubeSearchClient, VideoResult

# Get API URL from environment variable or use default
API_URL = os.getenv("YOUTUBE_SEARCH_API_URL", "http://localhost:8000")

@pytest.fixture
def client():
    """Fixture to create a client instance."""
    with YouTubeSearchClient(base_url=API_URL) as client:
        yield client

def test_basic_search(client):
    """Test basic search functionality."""
    results = client.search("Python programming")
    
    # Check if we got results
    assert len(results) > 0
    
    # Check the first result structure
    first_result = results[0]
    assert isinstance(first_result, VideoResult)
    assert isinstance(first_result.title, str)
    assert isinstance(first_result.channel_name, str)
    assert isinstance(first_result.duration, str)
    assert isinstance(first_result.views, str)
    assert isinstance(first_result.link, str)
    assert first_result.link.startswith("https://")
    
    # If publish_date exists, it should be a datetime
    if first_result.publish_date:
        assert isinstance(first_result.publish_date, datetime)

def test_search_with_parameters(client):
    """Test search with custom parameters."""
    limit = 10
    pages = 2
    results = client.search("Machine Learning", limit=limit, pages=pages)
    
    # Check if we got the expected number of results
    assert len(results) <= limit * pages
    
    # Check if page numbers are correct
    page_numbers = {result.page_number for result in results}
    assert max(page_numbers) <= pages
    assert min(page_numbers) == 1

def test_invalid_parameters(client):
    """Test error handling for invalid parameters."""
    # Test empty query
    with pytest.raises(ValueError, match="Query cannot be empty"):
        client.search("")
    
    # Test invalid limit
    with pytest.raises(ValueError, match="Limit must be between 1 and 50"):
        client.search("test", limit=51)
    
    # Test invalid pages
    with pytest.raises(ValueError, match="Pages must be between 1 and 10"):
        client.search("test", pages=11)

if __name__ == "__main__":
    # This allows running the tests directly with python
    pytest.main([__file__, "-v"]) 