#!/bin/bash

scl enable rh-python36 bash

python3 -m virtualenv env

source ./env/bin/activate

pip install -r requirements.txt

echo "Use db(Example).json to create a db.json credential file"
