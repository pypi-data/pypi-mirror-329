"""
PyTest configuration file for YouTube Search SDK tests.
"""

import pytest
import os
import time
import requests
from typing import Generator

def is_api_ready(url: str, timeout: int = 1) -> bool:
    """Check if the API is ready to accept requests."""
    try:
        response = requests.get(f"{url}/", timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

@pytest.fixture(scope="session", autouse=True)
def ensure_api_is_running() -> Generator[None, None, None]:
    """
    Fixture to ensure the API is running before tests start.
    This will wait for up to 30 seconds for the API to become available.
    """
    api_url = os.getenv("YOUTUBE_SEARCH_API_URL", "http://localhost:8000")
    max_attempts = 30
    attempt = 0

    while attempt < max_attempts:
        if is_api_ready(api_url):
            break
        time.sleep(1)
        attempt += 1
    else:
        pytest.fail(
            f"API at {api_url} is not available after {max_attempts} seconds. "
            "Make sure the YouTube Search API is running."
        )

    yield 