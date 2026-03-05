from zloom.lsst.alert_count import get_alert_count as lsst_count
from zloom.ztf.alert_count import get_alert_count as ztf_count
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get LSST and ZTF alert counts")
    parser.add_argument("--n_days", required=False, default=1, type=float, help="Number of days to look back for alerts")
    args = parser.parse_args()

    if not args.n_days:
        args.n_days = 1
    lsst_count(args.n_days)
    ztf_count(args.n_days)

if __name__ == "__main__":
    main()