#!/bin/bash
# The insructions was found in this link https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04?fbclid=IwAR1m4Y8lPYDZzlpCKiSmsi4b-0roZPSidVfw1yO9dXrJ6YVcHc7Q2MKsVHY

echo 'Preparing the environement'
apt-get update
apt-get install libncurses5 libclass-methodmaker-perl -y 

echo 'Download and install MySQL Cluster data node'
cd /home/ubuntu
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

echo 'Specifing the primary node as the master'
echo "
[mysql_cluster]
ndb-connectstring=ip-172-31-17-2.ec2.internal
" > /etc/my.cnf

echo 'creating a Systemd service unit file for the MySQL NDB Cluster node to start, restart and stop ndb_mgmd'
mkdir -p /usr/local/mysql/data
echo "
[Unit]
Description=MySQL NDB Data Node Daemon
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndbd
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ndbd.service

echo 'Reloading the systemd manager, enabling and starting the ndb_mgmd'
systemctl daemon-reload
systemctl enable ndbd
systemctl start ndbd
