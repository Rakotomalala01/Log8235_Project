import random
import pythonping 
from sshtunnel import SSHTunnelForwarder
import pymysql
import flask 

'''Variables Initialization:'''
instance_username="ubuntu"
pkey="vockey.pem"
mysql_username='root'
mysql_password='root'
mysql_database_name='sakila'
master_server  = "ip-172-31-17-2.ec2.internal"
salves_servers =["ip-172-31-17-3.ec2.internal", 
                 "ip-172-31-17-4.ec2.internal", 
                 "ip-172-31-17-5.ec2.internal"]
default_bind_address=(master_server, 3306)

app = flask.Flask(__name__)
@app.route('/endpoint', methods=['GET', 'POST'])

def gatekeeper_request():
    ''''Handling requests from the gatekeeper'''
    implementation = flask.request.args.get('implementation')
    sql_query = flask.request.get_data(as_text=True)
    result=run_direct_hit(master_server, sql_query)
    if implementation == "direct":
        print('direct hit chosen.', '\n')
        result=run_direct_hit(master_server, sql_query)
    elif implementation == "random":
        print('random hit chosen.', '\n')
        result=run_random_hit(salves_servers, master_server, sql_query)
    elif implementation == "customized":
        print('customized hit chosen.', '\n')
        result=run_customized_hit(salves_servers, master_server, sql_query)
    return flask.jsonify(result)

def create_ssh_tunnel(slave_ip, master_ip, sql_query):
    '''Establishing an SSH tunnel using SSHTunnelForwarder.'''
    with SSHTunnelForwarder(slave_ip, 
                            ssh_username=instance_username, 
                            ssh_pkey=pkey, 
                            remote_bind_address=default_bind_address) as tunnel:
        connection = pymysql.connect(host=master_ip, 
                                     user=mysql_username, 
                                     password=mysql_password, 
                                     db=mysql_database_name, 
                                     port=3306, 
                                     autocommit=True)
        cursor = connection.cursor()
        operation = sql_query
        cursor.execute(operation)        
        ssh_tunnelresult = cursor.fetchall()
        print(ssh_tunnelresult)
        return ssh_tunnelresult

def run_direct_hit(master_server, sql_query):
    """run_direct_hit calls create_ssh_tunnel method on the master node"""
    print('Request has been sent successfully to Master node at', master_server, '\n')
    direct_hit_result=create_ssh_tunnel(master_server, master_server, sql_query)
    return direct_hit_result

def run_random_hit(salves_servers, master_server, sql_query):
    """run_random_hit calls create_ssh_tunnel method on the salve node"""
    slave = random.choice(salves_servers)
    print('Request has been sent successfully to Slave', salves_servers.index(slave) + 1, 'node at:', slave, '\n')
    random_hit_result=create_ssh_tunnel(slave, master_server, sql_query)
    return random_hit_result

def run_customized_hit(salves_servers, master_server, sql_query):
    """run_customized_hit calls create_ssh_tunnel method on the best server"""
    best_server = get_best_server(salves_servers)
    print('Request has been sent successfully to Slave', salves_servers.index(best_server) + 1, 'node at:', best_server, '\n')
    customized_hit_result=create_ssh_tunnel(best_server, master_server, sql_query)
    return customized_hit_result

def get_best_server(salves_servers):
    """This function aims to determine the best server among a list of slave servers by checking their ping times. 
    It iterates through each slave server, measures its ping time, and selects the one with the lowest ping as the 
    best server."""
    best_server = master_server
    min = 1000
    print('Start choosing the best server...', '\n')
    for slave in salves_servers:
        ping_time = pythonping.ping(target=slave, count=1, timeout=2).rtt_avg_ms
        print("Slave", salves_servers.index(slave) + 1, "ping time:", ping_time, "ms")
        
        if ping_time < min:
            best_server = slave
            min = ping_time
    
    print('Best server is: Slave', salves_servers.index(best_server) + 1, "with", min,"ms", '\n')
    return best_server

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)