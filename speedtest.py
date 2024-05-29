#!/usr/bin/env python3
import subprocess
import datetime
import os
import time

def run_speedtest():
    try:
        result = subprocess.run(['speedtest-cli', '--simple'], capture_output=True, text=True)
        output = result.stdout.strip().split('\n')
        ping = output[0].split(': ')[1]
        download_speed = output[1].split(': ')[1]
        upload_speed = output[2].split(': ')[1]
        return ping, download_speed, upload_speed
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def save_results(directory, ping, download_speed, upload_speed):
    current_time = datetime.datetime.now()
    file_name = os.path.join(directory, f"results_{current_time.strftime('%m-%d-%Y_%H-%M-%S')}.txt")
    with open(file_name, "w") as f:
        f.write(f"Ping: {ping} ms\nDownload Speed: {download_speed} Mbit/s\nUpload Speed: {upload_speed} Mbit/s")
    print(f"Results saved to {file_name}")

def main():
    directory = "/home/admin/projects/speedtest/results/speedtest"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    while True:
        ping, download_speed, upload_speed = run_speedtest()
        if download_speed and upload_speed and ping:
            save_results(directory, ping, download_speed, upload_speed)
        else:
            with open("speedtest_log.txt", "a") as log_file:
                log_file.write(f"{datetime.datetime.now()} - Error running speedtest\n")
        time.sleep(1800)  # Wait for 30 minutes

if __name__ == "__main__":
    main()
