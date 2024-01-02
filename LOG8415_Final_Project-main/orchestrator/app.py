###
# flask application deployed on the instances
###
import time
import requests
from flask import Flask, jsonify
import json
import threading
from queue import Queue
import os

app = Flask(__name__)
lock = threading.Lock()
requestQueue = []

# get the name of the ec2 instance
instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
   
# route every requests to hello(), regardless of the path (equivalent to a wildcard)
@app.route('/', defaults={'path': ''})
def hello(path=None):
    return instance_id + 'is responding now'

if __name__ == '__main__':
    app.run()