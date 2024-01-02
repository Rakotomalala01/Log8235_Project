#!/bin/bash

echo 'Preparing the environement'
apt-get update
apt-get install python3 python3-pip git ufw iptables-persistent -y
pip install sshtunnel pythonping pymysql pandas argparse flask

sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

sudo ufw enable

sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT

sudo netfilter-persistent save
