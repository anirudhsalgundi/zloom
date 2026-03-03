from astropy.time import Time
from zloom.auth import get_boom_token
import requests
import os


def __init__():
    api_token = get_boom_token()
    return api_token

def get_alert_counts(api_token: str) -> str:

    response = requests.post(
                            "https://api.kaboom.caltech.edu/queries/count",
                            headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_token}"
                            },
                            json={
                            "catalog_name": "LSST_alerts",
                            "filter": {"candidate.jd": {"$gt": Time.now().jd - 5}},
                            }
                        )

    if not response.status_code == 200:
        print(f"Error: {response.status_code}")
        print(response.text)

    n_alerts = response.json()["data"]
    return n_alerts

def get_alert_count():
    api_token = __init__()
    n_alerts = get_alert_counts(api_token)
    print(f"Number of alerts in the last 24 hours: {n_alerts}")

    return None


def main():
    n_alerts_last_night()

if __name__ == "__main__":
    main()