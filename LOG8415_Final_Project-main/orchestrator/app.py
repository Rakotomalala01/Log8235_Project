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

def handleQueue():
    while True:
        if len(requestQueue) > 0:
            handleRequest()
            requestQueue.pop(0)
            time.sleep(1)            
        else:
            time.sleep(1)
            
def getWorkersState():
    """
    Get the worker state of ech container
    """
    with open('worker_state.json', 'r') as f:
        return json.load(f)
    

def updateContainerStatus(containerID, newStatus):
    """
    Update the status of a container
    :param containerID: the ID of the container to update, newStatus = the new status given to this container
    
    """
    with lock:
        data = getWorkersState()
        if containerID in data:
            data[containerID]["status"] = newStatus    
            with open("worker_state.json", 'w') as file:
                json.dump(data, file)
            
            
def sendRequestToContainer(containerID, containerInfo):
    """
    Send a request tp a container
    :param containerID: the ID of the container to send the request, containerInfo: the Info of the container to send the request,    
    """
    print(f"Sending request to {containerID}")
    targetUrl = f"http://{containerInfo['ip']}:{containerInfo['port']}/run_model"    
    res = requests.get(targetUrl).text
    print(f"received response from {containerID}")
    return res 

def processRequest(freeContainer, freeContainerInfo):
    """
    Send request to a container and update it's status when sending the request and when the request is finished
    :param freeContainer: the ID of the container which is free, containerInfo: the Info of the container which is free,    
    """
    updateContainerStatus(freeContainer, "busy")
    res = sendRequestToContainer(freeContainer, freeContainerInfo)
    updateContainerStatus(freeContainer, "free")     
    return res

    
def getFreeContainer():
    """
    Get the first free container on all instances of workers
    """
    workerState = getWorkersState()    
    freeContainer = None
    freeContainerInfo = None
    
    for containerName, containerInfo in workerState.items():
        if containerInfo.get('status') == "free":
            freeContainer = containerName
            freeContainerInfo = containerInfo
            return freeContainer, freeContainerInfo
    
def handleRequest():
    """
    Get the first free containner and send a get request to it otherwise add it to the queue
    """
    freeContainer, freeContainerInfo = getFreeContainer()
    if freeContainer:
        return processRequest(freeContainer, freeContainerInfo)
    else : 
        requestQueue.append(0)
   
# route every requests to hello(), regardless of the path (equivalent to a wildcard)
@app.route('/', defaults={'path': ''})
def hello(path=None):
    return instance_id + 'is responding now'


@app.route('/new_request')
def new_request():
    res = handleRequest() 
    return res

if __name__ == '__main__':
    threading.Thread(target=handleQueue).start()
    app.run()