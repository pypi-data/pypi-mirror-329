from typing import List, Optional
from pydantic import BaseModel, Field
import httpx
from datetime import datetime

class VideoResult(BaseModel):
    """A single video result from the YouTube search."""
    title: str
    channel_name: str
    duration: str
    views: str
    publish_date: Optional[datetime] = None
    link: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    page_number: int

class YouTubeSearchClient:
    """Client for interacting with the YouTube Search API."""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
        retries: int = 3
    ):
        """
        Initialize the YouTube Search client.
        
        Args:
            base_url (str): The base URL of the YouTube Search API. Defaults to localhost:8000.
            timeout (float): Timeout in seconds for API requests. Defaults to 30 seconds.
            retries (int): Number of retries for failed requests. Defaults to 3.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retries = retries
        
        # Configure client with timeouts and retries
        transport = httpx.HTTPTransport(retries=retries)
        self._client = httpx.Client(
            timeout=timeout,
            transport=transport,
            follow_redirects=True
        )

    def search(
        self, 
        query: str, 
        limit: int = 5, 
        pages: int = 5
    ) -> List[VideoResult]:
        """
        Search for YouTube videos.
        
        Args:
            query (str): The search query.
            limit (int, optional): Number of results per page. Defaults to 5.
            pages (int, optional): Number of pages to fetch. Defaults to 5.
            
        Returns:
            List[VideoResult]: List of video results.
            
        Raises:
            httpx.TimeoutException: If the request times out.
            httpx.HTTPError: If the API request fails.
            ValueError: If the parameters are invalid.
        """
        if not query:
            raise ValueError("Query cannot be empty")
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        if pages < 1 or pages > 10:
            raise ValueError("Pages must be between 1 and 10")

        params = {
            "query": query,
            "limit": limit,
            "pages": pages
        }

        try:
            response = self._client.get(
                f"{self.base_url}/search/",
                params=params
            )
            response.raise_for_status()
            
            results = [VideoResult(**item) for item in response.json()]
            return results
            
        except httpx.TimeoutException as e:
            raise httpx.TimeoutException(
                f"Request timed out after {self.timeout} seconds. "
                f"Consider increasing the timeout or checking if the API at {self.base_url} is responding."
            ) from e
        except httpx.HTTPError as e:
            raise httpx.HTTPError(
                f"API request failed: {str(e)}. "
                f"Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}. "
                f"Make sure the API at {self.base_url} is running and accessible."
            ) from e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close() 