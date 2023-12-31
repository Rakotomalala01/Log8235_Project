#!/bin/bash

# Create ec2 instances
echo "Creating EC2 for MySQL Cluster and Sakila"
python3 ec2.py 

#Deploy flask app on orchestrator
echo "Deploying flask app on orchestrator"
python3 orchestrator.py 

# Create containers in the intances
echo "Creating containers in each instance"
python3 worker.py 

#Send_multiple request to the orchestrator
echo "Sending request to the orchestrator"
python3 send_requests.py 
