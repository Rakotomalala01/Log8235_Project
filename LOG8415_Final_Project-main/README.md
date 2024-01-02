Demo : https://www.youtube.com/watch?v=Wd_fusG8-GI 

Before everything add your AWS CLI credentials to the .aws/credentials file

# Creating the Infrastructure 

To create the necessary infrastuctures for this solution, you have to run the EC2.py to create the necessary instances for the gatekeeper, proxy, cluster, standalone

# Standalone Benchmarking

Copy the standalone_benchmark.sh to the standalone server using this command 
'scp -i "vockey.pem" standalone_benchmark.sh ubuntu@"replace with the standalones public IP":/home/ubuntu'
Deploy the standalone_benchmark by running the standalone file
To do the benchamrk on MySQL Standalone server, connect to the server "Standalone" as a root and follows the instructions:

`cd /home/ubuntu`
`chmod +x standalone_benchmark.sh`
`./standalone_benchmark.sh`
`cat standalone_results.txt`

# Cluster Benchmarking

deploy the master_setup folder by calling cluster.py file and follows the instructions:
`cd /home/ubuntu/master`
`chmod +x master_setup.sh`
`chmod +x mysql_cluster_benchmark.sh`
`./master_setup.sh`

deploy the slave_setup folder by calling slave1.py, slave2.py, slave3.py

for each slave follows the instructions:

`cd /home/ubuntu` 
`chmod +x slave_setup.sh`
`./slave_setup.sh`

After on the master server: 

`cd /home/ubuntu/master` 
`./mysql_cluster_benchmark.sh`
`cat cluster_results.txt`

# Proxy 
deploy the proxy_setup folder by calling proxy.py file and follows the instructions:

1. connect to master:
`mysql -u root -p` 
`CREATE USER 'root'@'ip-172-31-17-6.ec2.internal' IDENTIFIED BY 'root';`
`GRANT ALL PRIVILEGES ON *.* TO 'root'@'ip-172-31-17-6.ec2.internal';`
`FLUSH PRIVILEGES;`

2. connect to the proxy:
`cd /home/ubuntu/proxy_setup` 
`chmod +x proxy_setup.sh`
`./proxy_setup.sh`
`python3 proxy.py`.  

# Gatekeeper 

copy the gatekeeper_setup folder to the gatekeeper server using this command 
`scp -i "vockey.pem" -r gatekeeper_setup ubuntu@"replace with the gatekeepers public IP":/home/ubuntu`

1. connect to the gatekeeper server as root:
2. run `cd /home/ubuntu/gatekeeper_setup` 
3. run `chmod +x gatekeeper_setup.sh`
4. run `./gatekeeper_setup.sh`
5. Run `python3 gatekeeper.py`. 