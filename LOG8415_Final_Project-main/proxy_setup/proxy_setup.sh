#!/bin/bash

echo 'Preparing the environement'
apt-get update
apt-get install python3 python3-pip git -y
pip install sshtunnel pythonping pymysql pandas argparse flask

