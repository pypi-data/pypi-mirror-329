# netdots/api_client.py
import requests

DEFAULT_BASE_URL = "http://127.0.0.1:8000"  # Change this to your production URL as needed.

class Netdots:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError("An API key must be provided.")
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def _headers(self):
        return {"x-api-key": self.api_key}

    def run_agent(self, payload: dict):
        url = f"{self.base_url}/agent"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def upload_document(self, payload: dict):
        url = f"{self.base_url}/upload_document"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_functions(self):
        url = f"{self.base_url}/functions"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
