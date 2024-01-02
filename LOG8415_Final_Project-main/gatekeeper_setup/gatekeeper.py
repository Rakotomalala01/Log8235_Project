import flask
import requests

app = flask.Flask(__name__)
def get_server_info(instance_name):
    server_info = None

    with open('./var/ec2_instances.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['name'] == instance_name:
                server_info = {
                    'name': row['name'],
                    'user_name': row['user_name'],
                    'public_dns_name': row['public_dns_name'],
                    'public_ip_address': row['public_ip_address'],
                    'state': row['state']
                }
                break

    return server_info

proxy_server  =get_server_info("proxy")['public_ip_address']

@app.route('/endpoint', methods=['GET', 'POST'])

def handle_request():
    implementation = flask.request.form.get('implementation')
    print('Implementation Chosen is:', implementation)
    sql_query = flask.request.form.get('sql_query')
    print('Query: ', sql_query)
    validation = validate_implementation(implementation)
    if validation == "valid":
        if flask.request.method == 'GET':
            print('The GET resquet will be forwarded to the proxy at', proxy_private_ip)
            response = requests.get(f"http://{proxy_private_ip}/endpoint", params={"implementation": implementation}, data=sql_query)
        elif flask.request.method == 'POST':
            print('The POST resquet will be forwarded to the proxy at', proxy_private_ip)
            response = requests.post(f"http://{proxy_private_ip}/endpoint", params={"implementation": implementation}, data=sql_query)
        return response.content

    else: 
        response = print("implementation is invalid")
    return None
    

def validate_implementation(implementation):
    if implementation == "direct":
        return "valid"
    elif implementation == "random":
        return "valid"
    elif implementation == "customized":
        return "valid"
    else: 
        return "invalid"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)