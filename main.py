import argparse

from core.metars import collect_metars, insert_metars
from core.models import session
from core.stations import collect_stations, insert_stations


def main(args):
    if args.stations:
        station_list = collect_stations()
        insert_stations(session, station_list)

    if args.metars:
        metar_list = collect_metars()
        insert_metars(session, metar_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--stations", action="store_true", help="retrieve stations")
    parser.add_argument("--metars", action="store_true", help="retrieve metars")

    args = parser.parse_args()

    main(args)
