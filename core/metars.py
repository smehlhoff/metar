import csv
import gzip
from typing import Any, Dict, List, Union

import requests
from sqlalchemy.orm import Session

from core.models import Metar, Station


def convert_cardinal_direction(value: str) -> str:
    if value == "VRB":
        return value
    else:
        directions = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
            "N",
        ]

        return directions[round(float(value) / 22.5)]


def convert_kt_to_mph(value: str) -> float:
    return round(float(value) * 1.151)


def convert_c_to_f(value: str) -> float:
    return round((float(value) * 1.8) + 32, 2)


def convert_statute_mi(value: str) -> Union[str, None]:
    match value:
        case "":
            return None
        case "6+":
            return "6"
        case "10+":
            return "10"
        case _:
            return value


def collect_metars() -> List[Dict[str, Any]]:
    url = "https://aviationweather.gov/data/cache/metars.cache.csv.gz"

    metar_list = []

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with gzip.open(r.raw, "rt", encoding="utf-8") as f:
            metars = csv.reader(f)

            for _ in range(5):
                next(metars)

            for metar in metars:
                if metar[1].startswith("K"):
                    metar_obj = {
                        "raw_text": metar[0],
                        "station_code": metar[1],
                        "observation_time": metar[2],
                        "temp_c": None if metar[5] == "" else metar[5],
                        "temp_f": None if metar[5] == "" else convert_c_to_f(metar[5]),
                        "dewpoint_c": None if metar[6] == "" else metar[6],
                        "dewpoint_f": None if metar[6] == "" else convert_c_to_f(metar[6]),
                        "wind_dir_degrees": None if metar[7] == "" else metar[7],
                        "wind_dir_cardinal": None
                        if metar[7] == "" or metar[7] == "0"
                        else convert_cardinal_direction(metar[7]),
                        "wind_speed_kt": None if metar[8] == "" else metar[8],
                        "wind_speed_mph": None if metar[8] == "" else convert_kt_to_mph(metar[8]),
                        "wind_gust_kt": None if metar[9] == "" else metar[9],
                        "wind_gust_mph": None if metar[9] == "" else convert_kt_to_mph(metar[9]),
                        "visibility_statute_mi": convert_statute_mi(metar[10]),
                        "altim_in_hg": None
                        if metar[11] == "0.00" or metar[11] == ""
                        else metar[11],
                        "sea_level_pressure_mb": None
                        if metar[12] == "0" or metar[12] == ""
                        else metar[12],
                        "corrected": False if metar[13] == "" else True,
                        "auto": False if metar[14] == "" else True,
                        "auto_station": False if metar[15] == "" else True,
                        "maintenance_indicator_on": False if metar[16] == "" else True,
                        "no_signal": False if metar[17] == "" else True,
                        "lightning_sensor_off": False if metar[18] == "" else True,
                        "freezing_rain_sensor_off": False if metar[19] == "" else True,
                        "present_weather_sensor_off": False if metar[20] == "" else True,
                        "wx_string": None if metar[21] == "" else metar[21],
                        "sky_cover": None if metar[22] == "" else metar[22],
                        "cloud_base_ft_agl": None if metar[23] == "" else metar[23],
                        "sky_cover_1": None if metar[24] == "" else metar[24],
                        "cloud_base_ft_agl_2": None if metar[25] == "" else metar[25],
                        "sky_cover_3": None if metar[26] == "" else metar[26],
                        "cloud_base_ft_agl_4": None if metar[27] == "" else metar[27],
                        "sky_cover_5": None if metar[28] == "" else metar[28],
                        "cloud_base_ft_agl_6": None if metar[29] == "" else metar[29],
                        "flight_category": None if metar[30] == "" else metar[30],
                        "three_hr_pressure_tendency_mb": None if metar[31] == "" else metar[31],
                        "maxt_c": None if metar[32] == "" else metar[32],
                        "maxt_f": None if metar[32] == "" else convert_c_to_f(metar[32]),
                        "mint_c": None if metar[33] == "" else metar[33],
                        "mint_f": None if metar[33] == "" else convert_c_to_f(metar[33]),
                        "maxt24hr_c": None if metar[34] == "" else metar[34],
                        "maxt24hr_f": None if metar[34] == "" else convert_c_to_f(metar[34]),
                        "mint24hr_c": None if metar[35] == "" else metar[35],
                        "mint24hr_f": None if metar[35] == "" else convert_c_to_f(metar[35]),
                        "precip_in": None if metar[36] == "" else metar[36],
                        "pcp3hr_in": None if metar[37] == "" else metar[37],
                        "pcp6hr_in": None if metar[38] == "" else metar[38],
                        "pcp24hr_in": None if metar[39] == "" else metar[39],
                        "snow_in": None if metar[40] == "" else metar[40],
                        "vert_vis_ft": None if metar[41] == "" else metar[41],
                        "metar_type": None if metar[42] == "" else metar[42],
                    }
                    metar_list.append(metar_obj)

    return metar_list


def insert_metars(session: Session, metar_list: List[Dict[str, Any]]) -> None:
    station_codes = [metar["station_code"] for metar in metar_list]
    existing_stations = session.query(Station).filter(Station.station_code.in_(station_codes)).all()
    existing_stations = {station.station_code: station.id for station in existing_stations}

    metar_list_final = []

    for metar in metar_list:
        if metar["station_code"] in existing_stations.keys():
            existing_metar = (
                session.query(Metar)
                .filter_by(
                    station_code=metar["station_code"],
                    observation_time=metar["observation_time"],
                )
                .first()
            )

            if existing_metar is None:
                metar["station_id"] = existing_stations.get(metar["station_code"])
                metar_list_final.append(metar)

    try:
        session.bulk_insert_mappings(Metar, metar_list_final)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
