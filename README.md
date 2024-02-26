# metar

Retrieves latest METARs from NOAA Aviation Weather Center and inserts data into a Postgres database. You can read more [here](https://aviationweather.gov/data/api/).

Do not use this script for real-world navigation.

## Install

Configure Postgres connection in `core/models.py`. For example,

`engine = create_engine("postgresql://postgres:dev@localhost:5432/postgres")`

Next, ensure you have the right dependencies installed.

    $ pip install -r requirements.txt

## Usage

    $ python main.py --stations --metars    # retrieve stations + metars

## Limitations

This script retrieves U.S. METARs only (e.g., KSFO, KJFK).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://github.com/smehlhoff/metar/blob/master/LICENSE)
