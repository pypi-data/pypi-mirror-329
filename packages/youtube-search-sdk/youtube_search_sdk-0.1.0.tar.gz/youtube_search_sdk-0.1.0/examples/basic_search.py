"""
Basic example of using the YouTube Search SDK.
"""

import httpx
from youtube_search_sdk import YouTubeSearchClient

def main():
    # Using context manager for proper cleanup, with custom timeout
    try:
        with YouTubeSearchClient(timeout=60.0, retries=3) as client:
            # Basic search
            print("Basic search:")
            try:
                results = client.search("Python programming")
                for video in results:
                    print(f"\nTitle: {video.title}")
                    print(f"Channel: {video.channel_name}")
                    print(f"Duration: {video.duration}")
                    print(f"Views: {video.views}")
                    print(f"Link: {video.link}")
                    if video.description:
                        print(f"Description: {video.description}")

                # Search with parameters
                print("\nSearch with custom parameters:")
                results = client.search(
                    query="Machine Learning tutorial",
                    limit=10,
                    pages=2
                )
                print(f"\nFound {len(results)} videos across {results[-1].page_number} pages")

            except httpx.TimeoutException as e:
                print(f"Error: Request timed out - {e}")
                print("Try increasing the timeout value or check if the API is responding")
            except httpx.HTTPError as e:
                print(f"Error: HTTP request failed - {e}")
                print("Make sure the API is running and accessible")
            except ValueError as e:
                print(f"Error: Invalid parameters - {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 