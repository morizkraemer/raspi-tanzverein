#!/bin/bash

# Change to the project directory
cd /home/morizkraemer/Desktop/raspi-tanzverein

# Start QLC+ in the background first
qlcplus -w -wp 3000 -k -o tanzverein.qxw &

# Wait a moment for QLC+ to start
sleep 2


# Start the Flask server in the foreground (so we can see its output)
source venv/bin/activate
python3 main.py
