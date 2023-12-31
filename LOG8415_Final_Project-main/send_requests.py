import concurrent.futures
import requests
import csv

def get_orchestrator_ip():
        """
        Reads username and host for SSH 
        """
        with open('var/ec2_instances.csv', mode='r') as csv_file:
            # Reconstruct instances list from file
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['name'] == 'orchestrator':
                    return (row['public_dns_name'])

URL = "http://" + get_orchestrator_ip() + "/new_request"

def make_get_request():
    # Send a GET request to the specified URL and return the response.
    response = requests.get(URL)
    return response.text

def send_get_requests_concurrently(num_requests=5):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the GET requests concurrently and wait for them to complete.
        futures = [executor.submit(make_get_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                response = future.result()
                print(response)  # Print the response text or handle as needed.
            except Exception as exc:
                print(f'An exception occurred: {exc}')

# Call the function to send the GET requests.
if __name__ == "__main__":
    for i in range(10):
        send_get_requests_concurrently()
