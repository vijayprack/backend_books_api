#!/bin/bash

# Create venv folder inside project
python3 -m venv venv

# Activate the environment
. $(pwd)/venv/bin/activate

# install python packages
pip3 install flask-restful --no-cache-dir
pip3 install pymongo --no-cache-dir
pip3 install python-dotenv
