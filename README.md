# Lightfeather Kanban Project
A simple kanban board project

## Features
SQLite database
Encrypted text backup (configuable in config.json)
Python FLASK RESTful API endpoints hosted on port: 23456
Drag and drop functionality
Add, Update, Delete, and organize cards across the board
Unlimited cards = unlimited potential!

## Installation
```sh
git clone https://github.com/Afkupuz/lightfeather.git
cd lightfeather
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 ./run.py
```

Note:
Press CTRL+C to terminate the server.  
use `deactive` to quit the virtual environment.
Python 3 is recommend, but this project is compatible with python 2.

### Run with Docker

You can run this project with docker by running the following commands:
```sh
docker build -t lightfeather:latest .

docker run -ti -v `pwd`:/app -p 23456:23456 lightfeather:latest
```

Note:
The `-v` in the run command above syncs local files with those in the container.