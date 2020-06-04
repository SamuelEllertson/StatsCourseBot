#!/bin/bash

if [ ! -f "db.json" ]; then
    echo "First create an empty database and db.json credential file. db(EXAMPLE).json is provided."
    exit
fi

/opt/rh/rh-python36/root/usr/bin/python3 -m virtualenv env

source ./env/bin/activate

pip install -r requirements.txt

python3 main.py --init
