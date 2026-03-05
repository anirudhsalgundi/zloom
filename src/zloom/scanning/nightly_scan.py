import os
import shutil
import requests
import webbrowser
import argparse
from astropy.time import Time
from zloom.auth import get_boom_token
from zloom.filters import all_filters
from zloom.utils import get_logger, log_banner
from zloom.filters.choose_filter import choose_filter
from zloom.lsst.alert_count import get_alert_count as lsst_alert_count
from zloom.ztf.alert_count import get_alert_count as ztf_alert_count


logger = get_logger(__name__)
width = shutil.get_terminal_size().columns

def _setup(n_days: float) -> tuple:
    api_token = get_boom_token()
    print("-" * width)
    lsst_alert_count(n_days)
    ztf_alert_count(n_days)
    print("-" * width)
    return api_token


def _argument_parser() -> argparse.Namespace:
    """
    Parses command-line arguments for the BOOM alerts script.
    """

    parser = argparse.ArgumentParser(description="Play with BOOM alerts")
    parser.add_argument("--filter_name", required=False, help="Name of your filer that you saved in filters/all_filters.py (For eg. ). If you already know which exact filter you want to use, you can specify it here. Otherwise, the script will prompt you to choose from the available filters.")
    parser.add_argument("--n_tabs", required=False, default=3, type=int, help="Number of tabs to open at once when viewing Babamul pages. After opening each batch, the script will prompt you to continue or stop.")
    parser.add_argument("--n_days", required=False, default=1, type=float, help="Number of days to look back when counting alerts and filtering. Default is 1 day. [CANNOT BE MORE THAN 7 DAYS]")
    parser.add_argument("--survey", required=False, default="both", choices=["LSST", "ZTF", "both"], help="Survey to filter alerts from. Default is LSST.")

    return parser.parse_args()

def _filter_lsst_alerts(api_token: str, user_filter: list, n_days: float) -> dict:
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
        log_banner(logger, f"response text: {response.text}")
        filtered_alerts = None

    if response.status_code != 200:
        log_banner(logger, f"Error: {response.status_code}")
        log_banner(logger, response.text)
        return None


    log_banner(logger, f"Number of alerts that passed filter in LSST: {len(filtered_alerts)}")
    return filtered_alerts

def _filter_ztf_alerts(api_token: str, user_filter: list, n_days: float) -> dict:
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
                            "permissions": {"ZTF": [1,2]},
                            "sort_by": None,
                            "sort_order": "Ascending",
                            "start_jd": Time.now().jd - n_days,
                            "survey": "ZTF"}
                        )

    try:
        filtered_alerts = response.json()
    except Exception:
        log_banner(logger, "response text:", response.text)
        filtered_alerts = None

    if response.status_code != 200:
        log_banner(logger, f"Error: {response.status_code}")
        log_banner(logger, response.text)
        return None


    log_banner(logger, f"Number of alerts that passed filter in ZTF: {len(filtered_alerts)}")
    return filtered_alerts


def _filter_ztf_and_lsst_alerts(api_token: str, user_filter: list, n_days: float) -> dict:

    lsst_alerts = _filter_lsst_alerts(api_token, user_filter, n_days)
    ztf_alerts = _filter_ztf_alerts(api_token, user_filter, n_days)

    combined = {
        "LSST": _get_unique_object_ids(lsst_alerts) if lsst_alerts else [],
        "ZTF": _get_unique_object_ids(ztf_alerts) if ztf_alerts else []
    }

    log_banner(logger, f"Number of sources that passed the filter in LSST: {len(combined['LSST'])}")
    log_banner(logger, f"Number of sources that passed the filter in ZTF: {len(combined['ZTF'])}")
    return combined


def _get_unique_object_ids(filtered_alerts: dict) -> list:
    results = filtered_alerts["data"]["results"]

    object_ids = [i["objectId"] for i in results]
    unique_object_ids = list(set(object_ids))
   
    
    return unique_object_ids


# FIXME: when boom is ported to fritz, this function should move from babamul to fritz
def _view_babamul_page(survey: str, unique_object_ids: str, n_tabs) -> None:

    for start in range(0, len(unique_object_ids), n_tabs):
        chunk = unique_object_ids[start:start + n_tabs]
        for i in chunk:
            url = f"https://babamul.caltech.edu/objects/{survey}/{i}"
            webbrowser.open_new_tab(url)
        
        # Ask before continuing (skip prompt after last batch)
        if start + n_tabs < len(unique_object_ids):
            response = input(f"Opened {min(start + n_tabs, len(unique_object_ids))}/{len(unique_object_ids)}. Open next {n_tabs}? (y/n): ")
            if response.lower() != 'y':
                print(f"Cannot identify input {response}. Valid options are: 'y' or 'n'")
            if response.lower() == 'n':
                print("Stopping.")
                return
               

    print("Done!")


def scan():
    args = _argument_parser()
    api_token = _setup(args.n_days)

    if not args.filter_name:
        active_filter = choose_filter()
    else:
        active_filter = all_filters[args.filter_name]


    if args.survey == "LSST":
        filtered_alerts = _filter_lsst_alerts(api_token, active_filter, n_days=args.n_days)
    elif args.survey == "ZTF":
        filtered_alerts = _filter_ztf_alerts(api_token, active_filter, n_days=args.n_days)
    elif args.survey == "both":
        combined_alerts = _filter_ztf_and_lsst_alerts(api_token, active_filter, n_days=args.n_days)
        if len(combined_alerts["LSST"]) == 0 and len(combined_alerts["ZTF"]) == 0:
            log_banner(logger, "No alerts passed the filter in either survey. Exiting.")
            print("\n\n***** Scan complete! *****")
            return
        else: 
            for survey_name, ids in combined_alerts.items():
                log_banner(logger, f"\nOpening {survey_name} objects...")

                _view_babamul_page(survey_name, ids, args.n_tabs)
                print("\n\n***** Scan complete! *****")
        return

    unique_object_ids = _get_unique_object_ids(filtered_alerts)
    log_banner(logger, f"Unique object IDs from filtered alerts: {len(unique_object_ids)}")
    
    
    _view_babamul_page(args.survey, unique_object_ids, args.n_tabs)

    print("\n\n***** Scan complete! *****")
    return None



def main():
    scan()

if __name__ == "__main__":
    main()