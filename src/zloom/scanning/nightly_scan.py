import sys
import os
from astropy.time import Time
from zloom.filters import all_filters
from zloom.lsst import get_alert_count
from zloom.auth import get_boom_token
from zloom.filters.choose_filter import choose_filter
import requests
from collections import defaultdict
import json
from astropy.time import Time
import webbrowser
import argparse


import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def setup(n_days: float = 1, credentials_file_path: str = None) -> tuple:
    api_token = get_boom_token()
    n_alerts = get_alert_count(n_days) #default to 1 day
    return api_token, n_alerts


def argument_parser() -> argparse.Namespace:
    """
    Parses command-line arguments for the BOOM alerts script.
    """

    parser = argparse.ArgumentParser(description="Play with BOOM alerts")
    parser.add_argument("--creds", required=False, default=os.environ.get("BOOM_CREDS"))
    parser.add_argument("--filter_name", required=False, help="If you already know which exact filter you want to use, you can specify it here. Otherwise, the script will prompt you to choose from the available filters.")
    parser.add_argument("--n_tabs", required=False, default=3, type=int, help="Number of tabs to open at once when viewing Babamul pages. After opening each batch, the script will prompt you to continue or stop.")
    parser.add_argument("--n_days", required=False, default=1, type=float, help="Number of days to look back when counting alerts and filtering. Default is 1 day.")

    return parser.parse_args()

def filter_rubin_alerts(api_token: str, user_filter: list, n_days: float) -> dict:
    # user_filter.replace("true", "True").replace("false", "False")
    response = requests.post(
                            "https://api.kaboom.caltech.edu/filters/test",
                            headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_token}"
                            },
                            json={
                            "end_jd": Time.now().jd,
                            "limit": None,
                            "pipeline": user_filter,
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
        print(response.text)


    print (f"Number of alerts returned by filter: {len(filtered_alerts)}")
    return filtered_alerts

def filter_ztf_alerts(api_token: str, user_filter: list, n_days: float) -> dict:
    response = requests.post(
                            "https://api.kaboom.caltech.edu/filters/test",
                            headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_token}"
                            },
                            json={
                            "end_jd": Time.now().jd,
                            "limit": None,
                            "pipeline": user_filter,
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
        print(response.text)


    print (f"Number of alerts returned by filter: {len(filtered_alerts)}")
    return filtered_alerts


def get_unique_object_ids(filtered_alerts: dict) -> list:
    results = filtered_alerts["data"]["results"]

    object_ids = [i["objectId"] for i in results]
    unique_object_ids = list(set(object_ids))
   
    
    return unique_object_ids


# FIXME: when boom is ported to fritz, this function should move from babamul to fritz
def view_babamul_page(unique_object_ids: str, n_tabs) -> None:

    for start in range(0, len(unique_object_ids), n_tabs):
        chunk = unique_object_ids[start:start + n_tabs]
        for i in chunk:
            url = f"https://babamul.caltech.edu/objects/LSST/{i}"
            webbrowser.open_new_tab(url)
        
        # Ask before continuing (skip prompt after last batch)
        if start + n_tabs < len(unique_object_ids):
            response = input(f"Opened {min(start + n_tabs, len(unique_object_ids))}/{len(unique_object_ids)}. Open next 20? (y/n): ")
            if response.lower() != 'y':
                print("Stopped.")
                break

    print("Done!")



def main():
    

    args = argument_parser()
    api_token, n_alerts = setup(n_days=args.n_days, credentials_file_path=args.creds)

    if not args.filter_name:
        # filters = get_available_filters()
        active_filter = choose_filter()

    else:
        active_filter = all_filters[args.filter_name]

    # logger.info(f"Using filter: {active_filter}")
    filtered_alerts = filter_rubin_alerts(api_token, active_filter, n_days=args.n_days)
    unique_object_ids = get_unique_object_ids(filtered_alerts)
    print(f"Unique object IDs from filtered alerts: {len(unique_object_ids)}")
    
    if not args.n_tabs:
        n_tabs = 3
    else:       
        n_tabs = args.n_tabs
    
    view_babamul_page(unique_object_ids, n_tabs)
    return None

if __name__ == "__main__":
    main()