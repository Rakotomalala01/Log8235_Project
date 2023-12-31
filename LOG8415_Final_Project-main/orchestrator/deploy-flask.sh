#!/bin/bash

cd orchestrator

sudo apt-get update -y
sudo apt-get -y install python3-venv

python3 -m venv venv

source venv/bin/activate

pip install Flask
pip install gunicorn
pip install requests

sudo cp /home/ubuntu/orchestrator/flaskapp.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp

sudo apt-get -y install nginx
sudo systemctl start nginx
sudo systemctl enable nginx

sudo cp /home/ubuntu/orchestrator/default /etc/nginx/sites-available

sudo systemctl restart flaskapp
sudo systemctl restart nginx