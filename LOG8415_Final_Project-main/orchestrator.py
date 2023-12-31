import csv
from fabric import Connection

class Orchestrator:
    def __init__(self):
        self.host, self.user_name = self._getSSHCredentials()
        self.connect_kwargs = {'key_filename': ['var/tp2-key.pem']}
        self.connection = Connection(self.host, user='ubuntu', connect_kwargs=self.connect_kwargs)

    def _getSSHCredentials(self):
        """
        Reads username and host for SSH 
        """
        with open('var/ec2_instances.csv', mode='r') as csv_file:
            # Reconstruct instances list from file
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['name'] == 'orchestrator':
                    return (row['public_dns_name'], row['user_name'])
                
    def getConnection(self):
        return self.connection
    
    def deployFlaskApp(self):
        """
        Deploys FlaskApp through SSH connection
        """
        try:
            print('Starting Flask deployment...')
            self.connection.run('mkdir -p orchestrator')
            self.connection.put('orchestrator/app.py', remote='/home/ubuntu/orchestrator')
            self.connection.put('orchestrator/worker_state.json', remote='/home/ubuntu/orchestrator')
            self.connection.put('orchestrator/default', remote='/home/ubuntu/orchestrator')
            self.connection.put('orchestrator/deploy-flask.sh', remote='/home/ubuntu/orchestrator')
            self.connection.put('orchestrator/flaskapp.service', remote='/home/ubuntu/orchestrator')
            self.connection.run('chmod +x orchestrator/deploy-flask.sh')
            self.connection.run('./orchestrator/deploy-flask.sh')
            print('Flask deployment finished sucessfully')
        except Exception as e:
            print('Deployment Failed: ')
            print(e)

if __name__ == "__main__":
    o = Orchestrator()
    o.deployFlaskApp()