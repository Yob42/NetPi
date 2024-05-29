#!/bin/bash

# Navigate to the project directory
cd /home/admin/projects/speedtest

# Execute the startup.sh script
./startup.sh

# Activate the virtual environment
source /home/admin/projects/speedtest/st_env/bin/activate

# Run the Python scripts using the Python interpreter from the virtual environment
nohup python app.py >/dev/null 2>&1 &
nohup python ping.py >/dev/null 2>&1 &
nohup sh -c "while true; do python speedtest.py; sleep 1800; done" >/dev/null 2>&1 &
