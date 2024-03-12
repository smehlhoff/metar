#!/bin/bash

usermod -s /bin/bash dev

git clone https://github.com/smehlhoff/metar.git /home/dev/metar

cd /home/dev/metar

python3.11 -m venv venv

source venv/bin/activate

pip install psycopg2-binary
pip install requests
pip install sqlalchemy

python main.py --stations

deactivate
