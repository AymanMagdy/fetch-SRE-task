# Fetch SRE task - Endpoint Availability Monitor

## Description

Kindly note that the submission is in Python. This tool monitors a list of HTTP endpoints provided via a YAML configuration file.  
It checks the availability of each endpoint every 15 seconds, considering:

- Endpoint is considered available if: **HTTP Status Code** between **>= 200 and <= 299 with** **Response Time** under **500 milliseconds**

Availability is tracked **cumulatively** and reported **per domain** (ignoring port numbers).

---

## How to Run?

1. How to run the python file without Docker?
```bash
pip install -r requirements.txt
python main.py --config=config.yaml
```

2. How to run in Docker?

```bash
docker build -t endpoint-monitor .
docker run -v $(pwd)/config.yaml:/app/config.yaml endpoint-monitor

Get the docker container ID:
docker container ls
docker exec -it CONTAINER_ID 

Now you can navigate through the files and check the logs.logs file. 
```

---
## Libraries / Tools Used
- **Python 3.12.4**
- **yaml**
- **requests**

---
## Monitoring Cycle
- **The tool checks all configured endpoints every 15 seconds, regardless of how many endpoints are listed.**
- **It continuously logs updated cumulative availability statistics.**
- **Availbility** Formula= ( number_success_requests / total_requests ) * 100

---

## Logging
- I have added a ```logger()``` function to write all the logging into ```logs.log``` file to store all the logging data there which we can use later as expose it via another endpoint ```/logs``` for immidiate logs availability.
- The logging solution is added based on each and every HTTP request for endpoints and logs the endpoints requests too.

---

## What did I fix/add?
- I have dockerized the app to be availble as we can run it as a sidecare container in our k8s env to log the services endpoints availability and provide insights on services basis.
- Parsing the configs file: I have changed the way the file is parsed to be argument based. ```--config=file.yaml```
- Printing logs: I have changed the print part to be logging based.
- POST requests: Loaded the json object ```if``` the method is a ```POST```request. 
- Handeling empty ```method```: if method is ```empty``` made it default to ```GET```
- Added ```response_time```: in order to measure the response time and decide ```if``` the response time is ```<= 500ms```.



