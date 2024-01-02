#!/bin/bash

echo 'Downloading and extract the Sakila database'
cd /home/ubuntu/master_setup
wget https://downloads.mysql.com/docs/sakila-db.tar.gz -O /home/ubuntu/sakila-db.tar.gz
tar -xvf /home/ubuntu/sakila-db.tar.gz -C /home/ubuntu/

echo 'Importing the Sakila database schema and data into MySQL'
mysql -u root -proot -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
mysql -u root -proot -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

echo 'Preparing the database for the benchmark:'
sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --mysql-user=root --mysql-password=root prepare

echo 'Running the OLTP benchmark:'
sysbench oltp_read_write --table-size=100000 --threads=6 --time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root --mysql-password=root run > /home/ubuntu/master_setup/cluster_results.txt

echo 'Clean up the database after the benchmark:'
sysbench oltp_read_write --mysql-db=sakila --mysql-user=root --mysql-password=root cleanup