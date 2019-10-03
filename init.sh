#!/bin/bash
python3.6 -m venv env
source env/bin/activate
cp config.example.py config.py
pip install -r requirements.txt
deactivate