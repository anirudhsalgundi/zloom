import json
import requests
import os

def _load_boom_credentials() -> str:
    
    username, password = os.getenv("BOOM_USERNAME"), os.getenv("BOOM_PASSWORD")
    if username and password:
        return username, password
    else:
        raise RuntimeError("Boom credentials not found in environment variables.")
    


def _authenticate_boom(username: str, password: str) -> str:
    auth_response = requests.post(
        "https://api.kaboom.caltech.edu/auth",
        data={"username": username, "password": password},
        headers={'Content-Type': "application/x-www-form-urlencoded"}
    )
    if auth_response.status_code == 200:
        return auth_response.json().get("access_token")
    else:
        raise RuntimeError(f"Login failed: {auth_response.status_code}")

def get_boom_token(credentials_file_path: str = None) -> None:
    username, password = _load_boom_credentials()
    api_token = _authenticate_boom(username, password)

    return api_token

def main():
    get_boom_token()

if __name__ == "__main__":
    main()