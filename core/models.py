import os

from sqlalchemy import (
    URL,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

conn = URL.create(
    "postgresql",
    username=os.getenv("POSTGRES_USER", "dev"),
    password=os.getenv("SERVER_PASSWORD", "dev"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port=os.getenv("POSTGRES_PORT", 5432),
    database=os.getenv("POSTGRES_DB", "dev"),
)


engine = create_engine(conn)
Base = declarative_base()


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)

    station_code = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    elev = Column(Integer)
    site = Column(String)
    state = Column(String)
    country = Column(String)

    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())

    metars = relationship("Metar", back_populates="station")


class Metar(Base):
    __tablename__ = "metars"

    id = Column(Integer, primary_key=True)

    station_id = Column(Integer, ForeignKey("stations.id"))
    station = relationship("Station", back_populates="metars")

    raw_text = Column(String)
    station_code = Column(String)

    observation_time = Column(String)

    temp_c = Column(Float, nullable=True)
    temp_f = Column(Float, nullable=True)
    dewpoint_c = Column(Float, nullable=True)
    dewpoint_f = Column(Float, nullable=True)

    wind_dir_degrees = Column(String, nullable=True)
    wind_dir_cardinal = Column(String, nullable=True)
    wind_speed_kt = Column(Integer, nullable=True)
    wind_speed_mph = Column(Integer, nullable=True)
    wind_gust_kt = Column(Integer, nullable=True)
    wind_gust_mph = Column(Integer, nullable=True)

    visibility_statute_mi = Column(Float, nullable=True)
    altim_in_hg = Column(Float, nullable=True)
    sea_level_pressure_mb = Column(Float, nullable=True)

    corrected = Column(Boolean)
    auto = Column(Boolean)
    auto_station = Column(Boolean)
    maintenance_indicator_on = Column(Boolean)
    no_signal = Column(Boolean)
    lightning_sensor_off = Column(Boolean)
    freezing_rain_sensor_off = Column(Boolean)
    present_weather_sensor_off = Column(Boolean)

    wx_string = Column(String, nullable=True)
    sky_cover = Column(String, nullable=True)
    cloud_base_ft_agl = Column(Integer, nullable=True)
    sky_cover_1 = Column(String, nullable=True)
    cloud_base_ft_agl_2 = Column(Integer, nullable=True)
    sky_cover_3 = Column(String, nullable=True)
    cloud_base_ft_agl_4 = Column(Integer, nullable=True)
    sky_cover_5 = Column(String, nullable=True)
    cloud_base_ft_agl_6 = Column(Integer, nullable=True)
    flight_category = Column(String, nullable=True)
    three_hr_pressure_tendency_mb = Column(Float, nullable=True)

    maxt_c = Column(Float, nullable=True)
    maxt_f = Column(Float, nullable=True)
    mint_c = Column(Float, nullable=True)
    mint_f = Column(Float, nullable=True)
    maxt24hr_c = Column(Float, nullable=True)
    maxt24hr_f = Column(Float, nullable=True)
    mint24hr_c = Column(Float, nullable=True)
    mint24hr_f = Column(Float, nullable=True)

    precip_in = Column(Float, nullable=True)
    pcp3hr_in = Column(Float, nullable=True)
    pcp6hr_in = Column(Float, nullable=True)
    pcp24hr_in = Column(Float, nullable=True)
    snow_in = Column(Float, nullable=True)

    vert_vis_ft = Column(Integer, nullable=True)

    metar_type = Column(String, nullable=True)

    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
