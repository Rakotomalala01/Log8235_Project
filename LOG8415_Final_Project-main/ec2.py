import boto3
import logging
from auth import EC2AuthManager
import csv
import json

# boto3.set_stream_logger('', logging.DEBUG)

# Create an EC2 resource
ec2_resource = boto3.resource('ec2')

class EC2InstancesManager:
    def __init__(self, security_group_name):
        self.ec2_resource = boto3.resource('ec2')
        self.auth_manager = EC2AuthManager()
        self.key_pair_name: str = self.auth_manager.get_or_create_key_pair('tp2-key')
        self.security_group_id: str = self.auth_manager.get_or_create_security_group(security_group_name)
        
        self.instance_ami_id = 'ami-053b0d53c279acc90' # Ubuntu Server 22.04 LTS Ami ID
        self.availability_zone = 'us-east-1a'
        self.save = None
    
    def create_instances(self, instance_name: str, instance_type: str, num_instances: int):
        """
        Create EC2 instances.

        :param instance_name: Name tag of the created instance 
        :param instance_type: Type of the created instance
        :param num_instances: Number of instances to create
        """
        volume_size = 10
        # if instance_name == 'worker':
        #     volume_size = 20

        instances = self.ec2_resource.create_instances(
            ImageId=self.instance_ami_id,
            MinCount=num_instances,
            MaxCount=num_instances,
            InstanceType=instance_type,
            KeyName=self.key_pair_name,
            SecurityGroupIds=[self.security_group_id],
            Placement={
                'AvailabilityZone': self.availability_zone
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance', 
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ],
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": { 
                        "VolumeSize": volume_size
                    }
                }
            ]
        )

        for instance in instances:
            instance.wait_until_running()

        print("Created {} {} instances of type {}.".format(num_instances, instance_name, instance_type))
    
    def _instanceToObject(self, instance):
        """
        Retrieve attributes from instance.
        Attributes are used for CSV file

        :param instance: EC2 instance to extract attributes
        """
        return {
            'name': [item['Value'] for item in instance.tags if item['Key'] == 'Name'][0],
            'user_name': 'ubuntu',
            'public_dns_name': instance.public_dns_name,
            'public_ip_address': instance.public_ip_address,
            'state': instance.state['Name']
        }

    def isInstanceRunning(self, instance):
        """
        Check if instance is running

        :param instance: EC2 instance to check status
        """
        return instance['state'] == 'running'

    def saveInstancesToCSV(self, type):
        """
        Save all instances to CSV file
        """
        tmp_instances = list(map(self._instanceToObject, self.ec2_resource.instances.all()))
        tmp_instances = filter(self.isInstanceRunning, tmp_instances)
        self.save = tmp_instances
        fields = ['name', 'user_name', 'public_dns_name', 'public_ip_address', 'state']
        filename = 'var/ec2_instances.csv'
        with open(filename, type) as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames = fields) 
            writer.writeheader() 
            writer.writerows(tmp_instances)
        print("Instances saved to '{}'".format(filename))


if __name__ == "__main__":
    ec2_manager_standalone = EC2InstancesManager("standalone")
    ec2_manager_standalone.create_instances('standalone', 't2.micro', 1)
    
    ec2_manager_cluster = EC2InstancesManager("cluster")
    ec2_manager_cluster.create_instances('master', 't2.micro', 1)
    
    slaves = []
    for i in range(3):
        instance_name = 'slave-' + str(i + 1)
        slave = ec2_manager_cluster.create_instances(instance_name, 't2.micro', 1)
        
        slaves.append(slave)
        
        
    ec2_manager_proxy = EC2InstancesManager("proxy")
    ec2_manager_proxy.create_instances('proxy', 't2.large', 1)    
    
    ec2_manager_gatekeeper = EC2InstancesManager("gatekeeper")
    ec2_manager_gatekeeper.create_instances('gatekeeper', 't2.large', 1)
    ec2_manager_gatekeeper.saveInstancesToCSV('w')
    
    