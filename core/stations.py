import gzip
import json
from typing import Any, Dict, List

import requests
from sqlalchemy.orm import Session

from core.models import Station


def collect_stations() -> List[Dict[str, Any]]:
    url = "https://aviationweather.gov/data/cache/stations.cache.json.gz"

    station_list = []

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with gzip.open(r.raw, "rt", encoding="utf-8") as f:
            stations = json.load(f)

            for station in stations:
                if station["icaoId"].startswith("K") and station["country"] == "US":
                    station_list.append(station)

    return station_list


def insert_stations(session: Session, station_list: List[Dict[str, Any]]) -> None:
    station_codes = [station["icaoId"] for station in station_list]
    existing_stations = session.query(Station).filter(Station.station_code.in_(station_codes)).all()
    existing_stations = [station.station_code for station in existing_stations]

    station_list_final = []

    for station in station_list:
        if station["icaoId"] not in existing_stations:
            s = Station(
                station_code=station["icaoId"],
                lat=station["lat"],
                lon=station["lon"],
                elev=station["elev"],
                site=station["site"],
                state=station["state"],
                country=station["country"],
            )
            station_list_final.append(s)

    try:
        session.bulk_save_objects(station_list_final)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
