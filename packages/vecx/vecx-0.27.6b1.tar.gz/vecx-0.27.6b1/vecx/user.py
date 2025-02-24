import requests
from typing import List, Optional, Dict
import json

class User:
    def __init__(self, base_url: str = "http://localhost:8080/api/v1", token: str|None = None):
        self.base_url = base_url.rstrip('/')
        self.token = token

    def set_token(self, token: str) -> None:
        self.token = token

    # Generate a root token. This can only be done once for the server.
    def generate_root_token(self) -> str:
        response = requests.post(f"{self.base_url}/root/token")
        return response.text

    # Create a new user using root credentials and return the user token.
    def create_user(self, username: str, root_token: str) -> str:
        headers = {"Authorization": root_token}
        data = {"username": username}
        response = requests.post(
            f"{self.base_url}/users",
            headers=headers,
            json=data
        )
        return response.text

    # Delete a user using root credentials. It deletes the user, his indexes and all associated tokens.
    def delete_user(self, username: str, root_token: str) -> None:
        headers = {"Authorization": root_token}
        response = requests.delete(
            f"{self.base_url}/api/v1/users/{username}",
            headers=headers
        )
        response.raise_for_status()

    # It return the user as not active and deletes all his tokens
    def deactivate_user(self, username: str, root_token: str) -> None:
        headers = {"Authorization": root_token}
        response = requests.post(
            f"{self.base_url}/api/v1/users/{username}/deactivate",
            headers=headers
        )
        response.raise_for_status()

    # Generate a new token for the authenticated user
    def generate_token(self, auth_token: str, name: str) -> str:
        if self.token is None:
            raise Exception("User token not set. Please set the user token using the set_token method.")
        headers = {"Authorization": auth_token}
        data = {"name": name}
        response = requests.post(
            f"{self.base_url}/api/v1/tokens",
            headers=headers,
            json=data
        )
        print(response.text)
        response.raise_for_status()
        return response.text

    # List all tokens for the authenticated user.
    def list_tokens(self) -> List[Dict]:
        if self.token is None:
            raise Exception("User token not set. Please set the user token using the set_token method.")
        headers = {"Authorization": self.token}
        response = requests.get(
            f"{self.base_url}/tokens",
            headers=headers
        )
        response.raise_for_status()
        return response.json()["tokens"]

    # Delete a specific token.
    def delete_token(self, auth_token: str, token_name: str) -> None:
        if self.token is None:
            raise Exception("User token not set. Please set the user token using the set_token method.")
        headers = {"Authorization": auth_token}
        response = requests.delete(
            f"{self.base_url}/api/v1/tokens/{token_name}",
            headers=headers
        )
        response.raise_for_status()

