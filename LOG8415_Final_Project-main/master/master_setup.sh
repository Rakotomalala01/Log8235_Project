#!/bin/bash

# The insructions was found in this link https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04?fbclid=IwAR1m4Y8lPYDZzlpCKiSmsi4b-0roZPSidVfw1yO9dXrJ6YVcHc7Q2MKsVHY


echo 'Preparing the environement'
apt-get update
apt-get install libncurses5 libaio1 libmecab2 sysbench -y

echo 'Download and install MySQL Clusters management'
cd /home/ubuntu/master_setup
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb


echo 'Setting up a MySQL Cluster configuration by creating a config.ini file'
sudo mkdir /var/lib/mysql-cluster
echo "
[ndbd default]
NoOfReplicas=3	

[ndb_mgmd]
hostname=ip-172-31-17-2.ec2.internal 
datadir=/var/lib/mysql-cluster 	

[ndbd]
hostname=ip-172-31-17-3.ec2.internal 
NodeId=2			
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-17-4.ec2.internal 
NodeId=3			
datadir=/usr/local/mysql/data

[ndbd]
hostname=ip-172-31-17-5.ec2.internal 
NodeId=4			
datadir=/usr/local/mysql/data

[mysqld]
hostname=ip-172-31-17-2.ec2.internal
" > /var/lib/mysql-cluster/config.ini

echo'creating a Systemd service unit file for the MySQL NDB Cluster Management Server to start, restart and stop ndb_mgmd'
echo "
[Unit]
Description=MySQL NDB Cluster Management Server
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndb_mgmd -f /var/lib/mysql-cluster/config.ini
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ndb_mgmd.service

echo 'Reloading the systemd manager'
systemctl daemon-reload

echo 'enabling and starting the ndb_mgmd'
systemctl enable ndb_mgmd
systemctl start ndb_mgmd

echo 'Downloading and extracting the MySQL Cluster bundle for installation'
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
sudo mkdir install
sudo tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

echo 'Installing MySQL Cluster components using the dpkg command'
dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb

echo 'Pre-configuring the root password for the MySQL Cluster Community Server installation'
debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/root-pass password root'
debconf-set-selections <<< 'mysql-cluster-community-server_7.6.6 mysql-cluster-community-server/re-root-pass password root'

echo 'Installing the MySQL Cluster Community Server and MySQL Server packages'
dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

echo 'Starting Configuring the client to connect to the master server'
echo "
[mysqld]
ndbcluster                   

[mysql_cluster]
ndb-connectstring=ip-172-31-17-2.ec2.internal 
" > /etc/mysql/my.cnf

echo 'Restarting and enabling the mysql server'
systemctl restart mysql
systemctl enable mysql