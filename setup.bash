#!/bin/bash

/opt/rh/rh-python36/root/usr/bin/python3 -m virtualenv env

source ./env/bin/activate

pip install -r requirements.txt

echo "Use db(Example).json to create a db.json credential file"
