#!/bin/bash
python3.6 -m venv env
source env/bin/activate
cd mercure
cp config.example.py config.py
cp farm.example.py farm.py
pip install -r requirements.txt
deactivate
