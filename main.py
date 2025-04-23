import time
from collections import defaultdict
import yaml
import requests
import argparse
import json
import logging
from datetime import datetime

# Writing logs to logs.log file
def logger(log):
    try:
        file = open("logs.log", "a")
        file.write(f"{json.dumps(log)}\n")
        file.close()
    except:
        logging.basicConfig(level=logging.INFO, format="ERORR: logging into the logs file")

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try: 
        if method == "POST": json_body = json.loads(body) # Loading the json body
        else: json_body = body

        # Added condition as some of the configs does not have "method" type included, so make it default as a GET request
        if method is None: 
            method = "GET"

        response = requests.request(method, url, headers=headers, json=json_body)
        response_time = response.elapsed.total_seconds() * 1000 # To get the m_seconds
        response.connection.close()

        current_time = datetime.now()
        log = {
            "Time": current_time.strftime("%H:%M:%S"),
            "Request_type": f"{method}",
            "Endpoint": f"{endpoint["url"]}",
            "Response_code": f"{response.status_code}",
            "Log": f"{response.text}"
        }

        # logging the endpoints requests status code, response messages
        logger(log=log)

        # Another issue with the status code should be >= 200 and less than or equal 299 and the response time <= 500ms
        if response.status_code >= 200 and response.status_code <= 299 and response_time <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    
    while True:
        for endpoint in config:
            domain = endpoint["url"].split("//")[-1].split("/")[0]
            result = check_health(endpoint)
            
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1
        
        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

            current_time = datetime.now()
            log = {
                "Time": current_time.strftime("%H:%M:%S"),
                "Domain": f"{domain} has {availability}% availability percentage"
            }
            
            # logging the domain availability info
            logger(log=log)

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        logging.basicConfig(level=logging.INFO, format='Required --config arg')
        # print("Usage: python main.py --config <config_file_path>")
        sys.exit(1)

    # Parsing config arg
    parser = argparse.ArgumentParser(description='Ayman Soliman submission Fetch SRE Task')
    parser.add_argument('--config', dest='config_file', required=True, help='Path to the configuration file')
    args = parser.parse_args()

    config_file = args.config_file #sys.argv[1]

    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logging.basicConfig(level=logging.INFO, format='Monitoring stopped by user. Access log file logs.log for all stats')
