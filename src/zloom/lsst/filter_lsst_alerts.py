from zloom.auth import get_boom_token
from astropy.time import Time



def __init__():
    api_token = get_boom_token()
    return api_token


def filter_rubin_alerts(api_token: str, n_days) -> dict:
    response = requests.post(
                            "https://api.kaboom.caltech.edu/filters/test",
                            headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_token}"
                            },
                            json={
                            "end_jd": Time.now().jd,
                            "limit": None,
                            "pipeline": filterr,
                            "permissions": {},
                            "sort_by": None,
                            "sort_order": "Ascending",
                            "start_jd": Time.now().jd - n_days,
                            "survey": "LSST"}
                        )

    try:
        filtered_alerts = response.json()
    except Exception:
        print("response text:", response.text)
        filtered_alerts = None

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(filtered_alerts.text)

    return filtered_alerts