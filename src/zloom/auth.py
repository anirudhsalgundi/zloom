import json
import requests
import os

def _load_boom_credentials(credentials_file_path: str = None):
    
    if credentials_file_path is None:
        credentials_file_path = os.environ.get("BOOM_CREDENTIALS")
    
    if credentials_file_path is None:
        raise ValueError(
            "No credentials file provided. Either pass it as an argument "
            "or set the BOOM_CREDENTIALS environment variable."
        )
    
    with open(credentials_file_path, "r") as file:
        boom_config = json.load(file)
    return boom_config["username"], boom_config["password"]


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
    print(f"Authenticated successfully!!")

    return api_token

def main():
    get_boom_token()

if __name__ == "__main__":
    main()