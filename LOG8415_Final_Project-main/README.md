For demenstration : https://www.youtube.com/watch?v=Wd_fusG8-GI 

# Prerequisites

1. `git clone https://github.com/ridaghoul/LOG8415_Final_Project.git`
2. Ensure your AWS CLI credentials are added to the `~/.aws/credentials file`
3. In the `main.py` file, replace the `default_subnet_id` with the subnet that has ip range of '172.31.16.0/20' 
4. Replace the content of the `vockey.pem` with your private key, make sure to leave the name as `vockey.pem`. in the main folder and inside the proxy_setup folder

# Creating the Infrastructure 

To create the necessary infrastuctures for this solution, you can initiate the process by executing the script named `python3 main.py` , this will create all the infrastructure needed for the project.

# Standalone Benchmarking

Copy the standalone_benchmark.sh to the standalone server using this command 
'scp -i "vockey.pem" standalone_benchmark.sh ubuntu@"replace with the standalones public IP":/home/ubuntu'

To benchamrk the MySQL Standalone server, connect to the server "Standalone" as a root, and:

1. run `cd /home/ubuntu`
2. run `chmod +x standalone_benchmark.sh`
3. run `./standalone_benchmark.sh`
4. run `cat standalone_results.txt` to see the results

# Cluster Benchmarking

Copy the master_setup folder to the master server using this command 
`scp -i "vockey.pem" -r master_setup ubuntu@"replace with the masters public IP":/home/ubuntu`

1. run `cd /home/ubuntu/master_setup`
2. run `chmod +x master_setup.sh`
3. run `chmod +x mysql_cluster_benchmark.sh`
4. run `./master_setup.sh`

copy the slave_setup.sh to the slave1 slave2 and slave3 servers using this command 
`scp -i "vockey.pem" slave_setup.sh ubuntu@"replace with the salve (1, 2 or 3) public IP":/home/ubuntu`

Connect to each slave server as root and:

1. run `cd /home/ubuntu` 
2. run `chmod +x slave_setup.sh`
3. run `./slave_setup.sh`

Finaly, back on the master server: 

run `cd /home/ubuntu/master_setup` 
run `./mysql_cluster_benchmark.sh`
run `cat cluster_results.txt` to see the results`

# Proxy 
copy the proxy_setup folder to the proxy server using this command 
`scp -i "vockey.pem" -r proxy_setup ubuntu@"replace with the proyxs public IP":/home/ubuntu`

1. connect to master server as root 
2. run `mysql -u root -p` 
3. run `CREATE USER 'root'@'ip-172-31-17-6.ec2.internal' IDENTIFIED BY 'root';`
4. run `GRANT ALL PRIVILEGES ON *.* TO 'root'@'ip-172-31-17-6.ec2.internal';`
5. run `FLUSH PRIVILEGES;`

1. connect to the proxy server as root:
2. run `cd /home/ubuntu/proxy_setup` 
3. run `chmod +x proxy_setup.sh`
4. run `./proxy_setup.sh`
5. Run `python3 proxy.py`.  

# Gatekeeper 

copy the gatekeeper_setup folder to the gatekeeper server using this command 
`scp -i "vockey.pem" -r gatekeeper_setup ubuntu@"replace with the gatekeepers public IP":/home/ubuntu`

1. connect to the gatekeeper server as root:
2. run `cd /home/ubuntu/gatekeeper_setup` 
3. run `chmod +x gatekeeper_setup.sh`
4. run `./gatekeeper_setup.sh`
5. Run `python3 gatekeeper.py`. 