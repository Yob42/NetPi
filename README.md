# NetPi
This project sets up a Flask server on a Raspberry Pi to facilitate network connectivity tests using Python scripts. It runs speed tests and ping tests periodically, saves the results, and provides a web interface to view the results.

While this project is under development it works best if you can setup this project up in /home/admin/projects/speedtest 
You can install and run this anywhere if you change the paths to your desired structure. 
## Project Structure

speedtest/
│
├── app.py
├── install.sh
├── ping.py
├── requirements.txt
├── run.sh
├── speedtest.py
├── startup.sh

└── templates/
    └── index.html

├── results/
│   ├── ping/
│   └── speedtest/

app.py: Flask web application to display the test results.
install.sh: Script to install Python dependencies.
ping.py: Script to perform ping tests.
requirements.txt: Python dependencies.
run.sh: Script to run the application.
speedtest.py: Script to perform network speed tests.
startup.sh: Script to set up the project environment.
instance/: Flask instance folder.
results/: Folder to store test results.
templates/: Folder for HTML templates.

Prerequisites
Python 3
Git

Installation

Create your own directory for the project:

mkdir -p /foo/do/speedtest

Replace /foo/do/speedtest with the directory path where you want to install the project.

Navigate to your project directory:

cd /foo/do/speedtest

Clone the repository into your directory:

git clone https://github.com/Yob42/NetPi.git .

Make the scripts executable:

chmod +x run.sh install.sh startup.sh

Set up the cronjob to start the application on reboot:
Edit your crontab using:

crontab -e

@reboot /foo/do/speedtest/run.sh

Usage
You can also manually start it by running:

./run.sh

Web Interface
Once the server is running, you can access the web interface by navigating to http://<raspberry-pi-ip>:5000 in your web browser.

Network Speed Results: Displays the latest network speed test results.
Ping Results: Displays the latest ping results and the last disconnect time.

Running Tests Manually
You can manually trigger the speed test and ping test by running the respective scripts:

Speed Test:
source foo/do/speedtest/st_env/bin/activate
python speedtest.py

Ping Test:
source foo/do/speedtest/st_env/bin/activate
python ping.py


Contributing
This project is under development, please feel free to provide feedback. Contributions are welcome! Please create an issue or submit a pull request for any improvements or bug fixes.
