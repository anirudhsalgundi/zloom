from astropy.time import Time
from zloom.auth import get_boom_token
import requests
import os


def __init__():
    api_token = get_boom_token()
    return api_token

def _get_alert_counts(api_token: str, n_days: float) -> str:

    response = requests.post(
                            "https://api.kaboom.caltech.edu/queries/count",
                            headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_token}"
                            },
                            json={
                            "catalog_name": "LSST_alerts",
                            "filter": {"candidate.jd": {"$gt": Time.now().jd - n_days}},
                            }
                        )

    if not response.status_code == 200:
        print(f"Error: {response.status_code}")
        print(response.text)

    n_alerts = response.json()["data"]
    return n_alerts

def get_alert_count(n_days: float) -> str:
    api_token = __init__()
    n_alerts = _get_alert_counts(api_token, n_days)
    if n_days == 1:
        print(f"Number of alerts in the last day: {n_alerts}")
    else:
        print(f"Number of alerts in the last {n_days} days: {n_alerts}")

    return None


def main(n_days: float = 1):
    get_alert_count(n_days)

if __name__ == "__main__":
    main(n_days)