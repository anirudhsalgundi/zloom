import sys
import os
from astropy.time import Time
from zloom.filters import all_filters
from zloom.lsst import get_alert_count
from zloom.auth import get_boom_token
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


def __init__():
    api_token = get_boom_token()
    return api_token


def argument_parser() -> argparse.Namespace:
    """
    Parses command-line arguments for the BOOM alerts script.
    """

    parser = argparse.ArgumentParser(description="Play with BOOM alerts")
    parser.add_argument("--creds", required=False, default=os.environ.get("BOOM_CREDS"))
    parser.add_argument("--filter_name", required=False, description="If you already know which exact filter you want to use, you can specify it here. Otherwise, the script will prompt you to choose from the available filters.")

    return parser.parse_args()


def get_available_filters() -> list:
    filters = [f for f in all_filters.keys()]
    print("Available filters:", filters)
    return filters


def choose_filter(filters) -> str:
    while True:
        choice = input("Enter the name of the filter you want to use: ")
        if choice in filters:
            print(f"Selected filter: {choice}")
            active_filter = choice
            return active_filter
        else:
            print("Invalid choice. Please try again.")





def main():
    get_alert_count()

    if not args.filter_name:
        filters = get_available_filters()
        active_filter = choose_filter(filters)

    

    return None

if __name__ == "__main__":
    main()





#     response = requests.post(
#         "https://api.kaboom.caltech.edu/queries/pipeline",
#         headers={
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_token}"
#         },
#         json={
#         "catalog_name": "LSST_alerts",
#         "max_time_ms": None,
#         "pipeline": {"jd": {"$gt": Time.now().jd - 1}}
#         }
#     )


# def filter_rubin_alerts(api_token: str) -> dict:
#     # filterr =[
#     #         {
#     #             "$match": {
#     #             "$and": [
#     #                 {
#     #                 "$or": [
#     #                     {
#     #                     "$and": [
#     #                         {
#     #                         "properties.photstats.r.fading.rate": {
#     #                             "$gt": 5
#     #                         }
#     #                         },
#     #                         {
#     #                         "properties.photstats.r.fading.red_chi2": {
#     #                             "$lte": 2
#     #                         }
#     #                         }
#     #                     ]
#     #                     },
#     #                     {
#     #                     "$and": [
#     #                         {
#     #                         "properties.photstats.g.fading.rate": {
#     #                             "$gt": 5
#     #                         }
#     #                         },
#     #                         {
#     #                         "properties.photstats.g.fading.red_chi2": {
#     #                             "$lte": 2
#     #                         }
#     #                         }
#     #                     ]
#     #                     },
#     #                     {
#     #                     "$and": [
#     #                         {
#     #                         "properties.photstats.r.rising.rate": {
#     #                             "$lte": -2
#     #                         }
#     #                         },
#     #                         {
#     #                         "properties.photstats.r.rising.red_chi2": {
#     #                             "$lte": 2
#     #                         }
#     #                         }
#     #                     ]
#     #                     },
#     #                     {
#     #                     "$and": [
#     #                         {
#     #                         "properties.photstats.g.rising.rate": {
#     #                             "$lte": -2
#     #                         }
#     #                         },
#     #                         {
#     #                         "properties.photstats.g.rising.red_chi2": {
#     #                             "$lte": 2
#     #                         }
#     #                         }
#     #                     ]
#     #                     }
#     #                 ]
#     #                 },
#     #                 {
#     #                 "properties.rock": {
#     #                     "$eq": False
#     #                 }
#     #                 },
#     #                 {
#     #                 "properties.star": {
#     #                     "$eq": False
#     #                 }
#     #                 },
#     #                 {
#     #                 "properties.near_brightstar": {
#     #                     "$eq": False
#     #                 }
#     #                 },
#     #                 {
#     #                 "candidate.isDipole": {
#     #                     "$eq": False
#     #                 }
#     #                 },
#     #                 {
#     #                 "candidate.isdiffpos": {
#     #                     "$eq": True
#     #                 }
#     #                 },
#     #                 {
#     #                 "candidate.reliability": {
#     #                     "$gte": 0.8
#     #                 }
#     #                 }
#     #             ]
#     #             }
#     #         },
#     #         {
#     #             "$project": {
#     #             "objectId": 1,
#     #             "candidate.jd": 1,
#     #             "properties.photstats.r.fading.rate": 1,
#     #             "properties.photstats.r.fading.red_chi2": 1,
#     #             "properties.photstats.g.fading.rate": 1,
#     #             "properties.photstats.g.fading.red_chi2": 1,
#     #             "properties.photstats.r.rising.rate": 1,
#     #             "properties.photstats.r.rising.red_chi2": 1,
#     #             "properties.photstats.g.rising.rate": 1,
#     #             "properties.photstats.g.rising.red_chi2": 1,
#     #             "properties.rock": 1,
#     #             "properties.star": 1,
#     #             "properties.near_brightstar": 1,
#     #             "candidate.isDipole": 1,
#     #             "candidate.isdiffpos": 1,
#     #             "candidate.reliability": 1,
#     #             "cross_matches.milliquas_v8": 1
#     #             }
#     #         },
#     #         {
#     #             "$addFields": {
#     #             "IsQuasar": {
#     #                 "$anyElementTrue": {
#     #                 "$map": {
#     #                     "input": {
#     #                     "$ifNull": [
#     #                         "$cross_matches.milliquas_v8",
#     #                         []
#     #                     ]
#     #                     },
#     #                     "in": {
#     #                     "$eq": [
#     #                         "$Descrip",
#     #                         "Q"
#     #                     ]
#     #                     }
#     #                 }
#     #                 }
#     #             }
#     #             }
#     #         },
#     #         {
#     #             "$match": {
#     #             "$and": [
#     #                 {
#     #                 "$expr": {
#     #                     "$lt": [
#     #                     {
#     #                         "$subtract": [
#     #                         "$cross_matches.AllWISE.w1mpro",
#     #                         "$cross_matches.AllWISE.w2mpro"
#     #                         ]
#     #                     },
#     #                     1
#     #                     ]
#     #                 }
#     #                 },
#     #                 {
#     #                 "IsQuasar": {
#     #                     "$eq": False
#     #                 }
#     #                 }
#     #             ]
#     #             }
#     #         },
#     #         {
#     #             "$project": {
#     #             "objectId": 1,
#     #             "candidate.jd": 1,
#     #             "properties.photstats.r.fading.rate": 1,
#     #             "properties.photstats.r.fading.red_chi2": 1,
#     #             "properties.photstats.g.fading.rate": 1,
#     #             "properties.photstats.g.fading.red_chi2": 1,
#     #             "properties.photstats.r.rising.rate": 1,
#     #             "properties.photstats.r.rising.red_chi2": 1,
#     #             "properties.photstats.g.rising.rate": 1,
#     #             "properties.photstats.g.rising.red_chi2": 1,
#     #             "properties.rock": 1,
#     #             "properties.star": 1,
#     #             "properties.near_brightstar": 1,
#     #             "candidate.isDipole": 1,
#     #             "candidate.isdiffpos": 1,
#     #             "candidate.reliability": 1,
#     #             "cross_matches.milliquas_v8": 1,
#     #             "IsQuasar": 1
#     #             }
#     #         }
#     #         ]

#     filterr = [
#                 {
#                     "$match": {
#                     "$and": [
#                         {
#                         "$or": [
#                             {
#                             "$and": [
#                                 {
#                                 "properties.photstats.r.fading.rate": {
#                                     "$gt": 10
#                                 }
#                                 },
#                                 {
#                                 "properties.photstats.r.fading.red_chi2": {
#                                     "$lte": 2
#                                 }
#                                 }
#                             ]
#                             },
#                             {
#                             "$and": [
#                                 {
#                                 "properties.photstats.g.fading.rate": {
#                                     "$gt": 10
#                                 }
#                                 },
#                                 {
#                                 "properties.photstats.g.fading.red_chi2": {
#                                     "$lte": 2
#                                 }
#                                 }
#                             ]
#                             },
#                             {
#                             "$and": [
#                                 {
#                                 "properties.photstats.r.rising.rate": {
#                                     "$lte": -10
#                                 }
#                                 },
#                                 {
#                                 "properties.photstats.r.rising.red_chi2": {
#                                     "$lte": 2
#                                 }
#                                 }
#                             ]
#                             },
#                             {
#                             "$and": [
#                                 {
#                                 "properties.photstats.g.rising.rate": {
#                                     "$lte": -10
#                                 }
#                                 },
#                                 {
#                                 "properties.photstats.g.rising.red_chi2": {
#                                     "$lte": 2
#                                 }
#                                 }
#                             ]
#                             }
#                         ]
#                         },
#                         {
#                         "properties.rock": {
#                             "$eq": False
#                         }
#                         },
#                         {
#                         "properties.star": {
#                             "$eq": False
#                         }
#                         },
#                         {
#                         "properties.near_brightstar": {
#                             "$eq": False
#                         }
#                         },
#                         {
#                         "candidate.isDipole": {
#                             "$eq": False
#                         }
#                         },
#                         {
#                         "candidate.isdiffpos": {
#                             "$eq": True
#                         }
#                         },
#                         {
#                         "candidate.reliability": {
#                             "$gte": 0.8
#                         }
#                         },
#                         {
#                         "candidate.extendedness": {
#                             "$lt": 1
#                         }
#                         }
#                     ]
#                     }
#                 },
#                 {
#                     "$project": {
#                     "objectId": 1,
#                     "candidate.jd": 1,
#                     "properties.photstats.r.fading.rate": 1,
#                     "properties.photstats.r.fading.red_chi2": 1,
#                     "properties.photstats.g.fading.rate": 1,
#                     "properties.photstats.g.fading.red_chi2": 1,
#                     "properties.photstats.r.rising.rate": 1,
#                     "properties.photstats.r.rising.red_chi2": 1,
#                     "properties.photstats.g.rising.rate": 1,
#                     "properties.photstats.g.rising.red_chi2": 1,
#                     "properties.rock": 1,
#                     "properties.star": 1,
#                     "properties.near_brightstar": 1,
#                     "candidate.isDipole": 1,
#                     "candidate.isdiffpos": 1,
#                     "candidate.reliability": 1,
#                     "candidate.extendedness": 1,
#                     "cross_matches.milliquas_v8": 1
#                     }
#                 },
#                 {
#                     "$addFields": {
#                     "IsQuasar": {
#                         "$anyElementTrue": {
#                         "$map": {
#                             "input": {
#                             "$ifNull": [
#                                 "$cross_matches.milliquas_v8",
#                                 []
#                             ]
#                             },
#                             "in": {
#                             "$eq": [
#                                 "$Descrip",
#                                 "Q"
#                             ]
#                             }
#                         }
#                         }
#                     }
#                     }
#                 },
#                 {
#                     "$match": {
#                     "$and": [
#                         {
#                         "$expr": {
#                             "$lt": [
#                             {
#                                 "$subtract": [
#                                 "$cross_matches.AllWISE.w1mpro",
#                                 "$cross_matches.AllWISE.w2mpro"
#                                 ]
#                             },
#                             1
#                             ]
#                         }
#                         },
#                         {
#                         "$and": [
#                             {
#                             "IsQuasar": {
#                                 "$eq": False
#                             }
#                             },
#                             {
#                             "$expr": {
#                                 "$lt": [
#                                 {
#                                     "$divide": [
#                                     "$cross_matches.Gaia_DR3.pm",
#                                     {
#                                         "$sqrt": {
#                                         "$add": [
#                                             {
#                                             "$pow": [
#                                                 "$cross_matches.Gaia_DR3.pmra_error",
#                                                 2
#                                             ]
#                                             },
#                                             {
#                                             "$pow": [
#                                                 "$cross_matches.Gaia_DR3.pmdec_error",
#                                                 2
#                                             ]
#                                             }
#                                         ]
#                                         }
#                                     }
#                                     ]
#                                 },
#                                 3
#                                 ]
#                             }
#                             }
#                         ]
#                         }
#                     ]
#                     }
#                 },
#                 {
#                     "$project": {
#                     "objectId": 1,
#                     "candidate.jd": 1,
#                     "properties.photstats.r.fading.rate": 1,
#                     "properties.photstats.r.fading.red_chi2": 1,
#                     "properties.photstats.g.fading.rate": 1,
#                     "properties.photstats.g.fading.red_chi2": 1,
#                     "properties.photstats.r.rising.rate": 1,
#                     "properties.photstats.r.rising.red_chi2": 1,
#                     "properties.photstats.g.rising.rate": 1,
#                     "properties.photstats.g.rising.red_chi2": 1,
#                     "properties.rock": 1,
#                     "properties.star": 1,
#                     "properties.near_brightstar": 1,
#                     "candidate.isDipole": 1,
#                     "candidate.isdiffpos": 1,
#                     "candidate.reliability": 1,
#                     "candidate.extendedness": 1,
#                     "cross_matches.milliquas_v8": 1,
#                     "IsQuasar": 1
#                     }
#                 }
#                 ]
#     response = requests.post(
#                             "https://api.kaboom.caltech.edu/filters/test",
#                             headers={
#                             "Content-Type": "application/json",
#                             "Authorization": f"Bearer {api_token}"
#                             },
#                             json={
#                             "end_jd": Time.now().jd,
#                             "limit": None,
#                             "pipeline": filterr,
#                             "permissions": {},
#                             "sort_by": None,
#                             "sort_order": "Ascending",
#                             "start_jd": Time.now().jd - 4,
#                             "survey": "LSST"}
#                         )

#     try:
#         filtered_alerts = response.json()
#     except Exception:
#         print("response text:", response.text)
#         filtered_alerts = None

#     if response.status_code != 200:
#         print(f"Error: {response.status_code}")
#         print(filtered_alerts.text)

#     return filtered_alerts


# def get_unique_object_ids(filtered_alerts: dict) -> list:
#     results = filtered_alerts["data"]["results"]

#     object_ids = [i["objectId"] for i in results]
#     unique_object_ids = list(set(object_ids))
#     # unique_object_ids = list(dict.fromkeys(object_ids))
    
#     return unique_object_ids

# def write_summary_to_csv(unique_object_ids: list, filtered_alerts: dict) -> None:
#     with open("query_summary.csv", "w") as file:
#         for i, g in enumerate(unique_object_ids):
#             print(f"{i+1}. https://babamul.caltech.edu/objects/LSST/{g}")
#             file.write(f"{i+1}, https://babamul.caltech.edu/objects/LSST/{g}\n")
#     return None

# def view_babamul_page(unique_object_ids: str) -> None:

#     # REQUIREMENTS: BRAVERY to change n_windows
#     n_windows = 20
#     for start in range(0, len(unique_object_ids), n_windows):
#         chunk = unique_object_ids[start:start + n_windows]
#         for i in chunk:
#             url = f"https://babamul.caltech.edu/objects/LSST/{i}"
#             webbrowser.open_new_tab(url)
        
#         # Ask before continuing (skip prompt after last batch)
#         if start + n_windows < len(unique_object_ids):
#             response = input(f"Opened {min(start + n_windows, len(unique_object_ids))}/{len(unique_object_ids)}. Open next 20? (y/n): ")
#             if response.lower() != 'y':
#                 print("Stopped.")
#                 break

#     print("Done!")


# def main():
#     api_token = authenticate_boom()
#     # filtering_pipeline = {} # FIXME: need to add the filtering pipeline for ztf alerts. also, may want to add a command line argument for the filtering pipeline.
#     n_alerts = get_alert_counts(api_token)
#     print(f"Number of alerts in the last 24 hours: {n_alerts}")
#     filtered_rubin_alerts = filter_rubin_alerts(api_token)
#     print(f"Number of alerts that passed the filter: {len(filtered_rubin_alerts['data']['results'])}")
#     sources = get_unique_object_ids(filtered_rubin_alerts)
#     print(f"Number of unique sources that passed the filter: {len(sources)}")
#     write_summary_to_csv(sources, filtered_rubin_alerts)
#     print("Summary written to query_summary.csv")
#     view_babamul_page(sources)


        

#     # print(response)

# if __name__ == "__main__":
#     main()