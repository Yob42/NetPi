import subprocess
import time
import os

def send_ping(destination, results_dir):
    while True:
        try:
            # Run ping command
            ping_process = subprocess.Popen(['ping', '-c', '1', destination], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ping_output, _ = ping_process.communicate()

            # Parse ping output
            ping_result = ping_output.decode('utf-8')

            # Save ping result to file
            timestamp = time.strftime('%d-%m-%Y_%H-%M-%S')
            file_name = f"results_{timestamp}.txt"
            file_path = os.path.join(results_dir, file_name)
            with open(file_path, "w") as f:
                f.write(ping_result)

            print(f"Ping successful. Saved result to {file_path}")
        except Exception as e:
            # Log errors
            with open("ping_log.txt", "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {e}\n")
                print(f"Error: {e}")
        time.sleep(15)

if __name__ == "__main__":
    results_directory = "/home/admin/projects/speedtest/results/ping"
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    send_ping("1.1.1.1", results_directory)
