import requests
from typing import List, Optional, Union

class Cinnavo:
    def __init__(self, api_key: str, base_url: str = "https://api.cinnavo.com"):
        """
        Initialize the Cinnavo API client.

        :param api_key: Your API key for authentication.
        :param base_url: The base URL of the API.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def search(
        self,
        query: str,
        num_results: int = 10,
        date_range: Optional[str] = None,
        engine: Optional[Union[List[str], str]] = None,
        categories: Optional[str] = None,
        ai_response: bool = False,
        full_content: bool = False,
    ) -> dict:
        """
        Perform a search using the Cinnavo API.

        :param query: Search query string.
        :param num_results: Number of results to return (must be between 1 and 50).
        :param date_range: Optional date range filter (e.g., 'day', 'week', 'month', 'year').
        :param engine: Optional search engines to use (either a list of strings or a comma-separated string).
        :param categories: Optional categories filter (e.g., news, science, etc.).
        :param ai_response: If True, include an AI-generated response.
        :param full_content: If True, fetch full content from result URLs.
        :return: Dictionary containing the API response.
        """
        url = f"{self.base_url}/search"
        headers = {"api_key": self.api_key}
        params = {
            "query": query,
            "num_results": num_results,
            "date_range": date_range,
            "categories": categories,
            "ai_response": str(ai_response).lower(),
            "full_content": str(full_content).lower(),
        }
        if engine:
            # If a list is provided, join it into a comma-separated string.
            if isinstance(engine, list):
                params["engine"] = ",".join(engine)
            else:
                params["engine"] = engine

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
