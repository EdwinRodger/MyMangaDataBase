#!/bin/bash

# Create Python 3 virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install packages from requirements.txt
pip3 install -r requirements.txt

# Open http://127.0.0.1:6070 in a new browser window
xdg-open "http://127.0.0.1:6070" &

# Run app.py using Python 3
python3 app.py

# This is chapgpt generated code. If there is an error, help me fix it.