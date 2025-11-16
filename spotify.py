from dotenv import load_dotenv
load_dotenv()

import os
import requests

class SpotifyClient:
    BASE_URL = "https://api.spotify.com/v1"
    AUTH_SERVER_URL = "http://127.0.0.1:5000"

    def __init__(self):
        self.auth_token = None

    def fetch_user_token(self):
        resp = requests.get(f"{self.AUTH_SERVER_URL}/user_token")
        resp.raise_for_status()
        token = resp.json().get("access_token")
        if not token:
            raise RuntimeError("No user token available. Did you visit /login and authorize?")
        self.auth_token = token

    def _get_headers(self):
        if not self.auth_token:
            self.fetch_user_token()
        return {"Authorization": f"Bearer {self.auth_token}"}

    def get_current_user(self):
        url = f"{self.BASE_URL}/me"
        headers = self._get_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_user_top_items(self):

        url = f"{self.BASE_URL}/me/top/artists"
        headers = self._get_headers()
        

        limit = 50
        params = {"limit": limit, "offset": 0, "time_range": "medium_term"}
        resp = requests.get(url, headers=headers, params=params)

        resp.raise_for_status()

        return [
            {
                "name": r.get("name"),
                "popularity": r.get("popularity")
            }
            for r in resp.json().get("items")
        ]


if __name__ == "__main__":
    client = SpotifyClient()
    me = client.get_current_user()
    top = client.get_user_top_items()
    print(top)
