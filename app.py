import os
import re
import threading
import time
import logging
from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from plotly.subplots import make_subplots
import plotly.graph_objs as go

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
SPEEDTEST_DIR = os.path.join(RESULTS_DIR, 'speedtest')
PING_DIR = os.path.join(RESULTS_DIR, 'ping')

def parse_data_files(directory):
    data = {}
    pattern = r"results_(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})\.txt"
    for filename in os.listdir(directory):
        match = re.match(pattern, filename)
        if match:
            timestamp = match.group(1)
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    if len(lines) < 3:
                        logging.debug(f"Skipping file {filename} due to insufficient data")
                        continue
                    ping = float(re.findall(r"[-+]?\d*\.\d+|\d+", lines[0])[0])
                    download_speed = float(re.findall(r"[-+]?\d*\.\d+|\d+", lines[1])[0])
                    upload_speed = float(re.findall(r"[-+]?\d*\.\d+|\d+", lines[2])[0])
                    data[timestamp] = {"ping": ping, "download_speed": download_speed, "upload_speed": upload_speed}
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")
    return data

def get_latest_result(data):
    if not data:
        return None, None, None, None
    latest_timestamp = max(data.keys())
    latest_data = data[latest_timestamp]
    return latest_timestamp, latest_data["ping"], latest_data["download_speed"], latest_data["upload_speed"]

def get_last_disconnect(files, directory):
    failure_pattern = r"0% packet loss"
    oldest_file = None
    oldest_time = None
    last_disconnect = None
    for filename in files:
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                if len(lines) >= 3 and failure_pattern not in lines[-1]:
                    last_disconnect = filename
                timestamp_str = filename.replace('results_', '').replace('.txt', '')
                timestamp = datetime.strptime(timestamp_str, "%m-%d-%Y_%H-%M-%S")
                if oldest_time is None or timestamp < oldest_time:
                    oldest_time = timestamp
                    oldest_file = filename
        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")
    if last_disconnect:
        return last_disconnect.replace('results_', '').replace('.txt', '').replace('_', ' ')
    else:
        return oldest_file.replace('results_', '').replace('.txt', '').replace('_', ' ')

def ping_monitor():
    while True:
        try:
            files = os.listdir(PING_DIR)
            if files:
                latest_file = max(files)
                with open(os.path.join(PING_DIR, latest_file), "r") as file:
                    lines = file.readlines()
                    if len(lines) >= 2:
                        ping_result = lines[1].strip()
                        app.config["PING_RESULT"] = ping_result
                        app.config["PING_FULL_FILENAME"] = latest_file.replace('results_', '').replace('.txt', '').replace('_', ' ')
                        logging.info(f"Updated ping result: {ping_result}")
                last_disconnect = get_last_disconnect(files, PING_DIR)
                app.config["LAST_DISCONNECT"] = last_disconnect
                logging.info(f"Last disconnect: {last_disconnect}")
        except Exception as e:
            logging.error(f"Error in ping monitoring: {e}")
        finally:
            time.sleep(15)

@app.route('/')
def index():
    data = parse_data_files(SPEEDTEST_DIR)
    logging.debug(f"Parsed data: {data}")
    latest_timestamp, ping_status, download_speed, upload_speed = get_latest_result(data)
    logging.debug(f"Latest result: {latest_timestamp}, {ping_status}, {download_speed}, {upload_speed}")
    sorted_data = dict(sorted(data.items()))
    timestamps = list(sorted_data.keys())
    download_speeds = [sorted_data[timestamp]["download_speed"] for timestamp in timestamps]
    upload_speeds = [sorted_data[timestamp]["upload_speed"] for timestamp in timestamps]
    datetime_timestamps = [datetime.strptime(timestamp, "%m-%d-%Y_%H-%M-%S") for timestamp in timestamps]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Download Speed (Mbps)", "Upload Speed (Mbps)"))
    fig.add_trace(go.Scatter(x=datetime_timestamps, y=download_speeds, mode='lines', name='Download Speed (Mbps)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=datetime_timestamps, y=upload_speeds, mode='lines', name='Upload Speed (Mbps)'), row=2, col=1)
    fig.update_layout(title='Network Speed Over Time', xaxis_title='Date', yaxis_title='Speed (Mbps)', showlegend=False)
    graph_html = fig.to_html(full_html=False)
    status = app.config.get("STATUS", "No data available")
    uptime = app.config.get("UPTIME", "No data available")
    ping_result = app.config.get("PING_RESULT", "No data available")
    ping_full_filename = app.config.get("PING_FULL_FILENAME", "No data available")
    last_disconnect = app.config.get("LAST_DISCONNECT", "No data available")
    return render_template('index.html', file_name=latest_timestamp, ping_status=ping_status, download_speed=download_speed, upload_speed=upload_speed, graph_html=graph_html, status=status, uptime=uptime, ping_result=ping_result, ping_full_filename=ping_full_filename, last_disconnect=last_disconnect)

@app.route('/run_speed_test', methods=['GET'])
def run_speed_test():
    os.system(os.path.join(BASE_DIR, 'run_speedtest.sh'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    ping_thread = threading.Thread(target=ping_monitor)
    ping_thread.daemon = True
    ping_thread.start()
    app.run(host='0.0.0.0', port=5000)
