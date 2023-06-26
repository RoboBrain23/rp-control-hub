"""
streamer.py

The `streamer.py` module is a crucial component of the RP Control Hub system.
It enables seamless streaming of sensor data from Raspberry Pi to a backend API.
This module establishes a connection with the backend API and periodically sends sensor data,
allowing real-time monitoring and analysis of the collected information.
"""

import requests
import json
import sched
import time

# URL of the endpoint to send the POST request
URL = ""
LOGIN_ENDPOINT = f"{URL}/chair/login"
SENSOR_DATA_ENDPOINT = f"{URL}/chair/data"

INTERVAL = 10  # in seconds

CHAIR_ID = 3
PASSWORD = "hahah"
temperature = 36.5
oximeter = 12.4
pulse_rate = 19.8

wheelchair = {
    "chair_id": 3,
    "password": "pass",
    "temperature": 36.5,
    "oximeter": 12.4,
    "pulse_rate": 19.8

}

access_token = ""

identity = {
    "chair_id": wheelchair["chair_id"],
    "password": wheelchair["password"],
}

# Set the headers for the request
headers = {
    "Content-Type": "application/json"
}


# Login Function
def login():
    global headers
    global access_token

    json_identity = json.dumps(identity)
    response = requests.post(LOGIN_ENDPOINT, data=json_identity, headers=headers)

    if response.status_code == 200:
        print("Sign-in successfully!. Status code:", response.status_code)
        res = json.loads(response.text)

        access_token = f"Bearer {res['access_token']}"

        headers = {
            "Authorization": access_token
        }

        return response.status_code
    else:
        print("Sign-in Failed. Status code:", response.status_code)
        print(response.text)
        return response.status_code


# Send the POST request
def send_data():
    data = {
        "chair_id": wheelchair["chair_id"],
        "temperature": wheelchair["temperature"],
        "oximeter": wheelchair["oximeter"],
        "pulse_rate": wheelchair["pulse_rate"]
    }

    json_data = json.dumps(data)
    response = requests.post(SENSOR_DATA_ENDPOINT, data=json_data, headers=headers)

    print(f"HEADER: {headers}")

    # Check the response status code
    if response.status_code == 201:
        print("Request sent successfully!. Status code:", response.status_code)
        print(response.text)
    elif response.status_code == 401:
        print("Trying to login again")
        login()
    else:
        print("Failed to send the request. Status code:", response.status_code)
        print(response.text)


def main():
    login_status_code = login()

    if login_status_code == 200:
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(0, 1, send_data)
        interval = INTERVAL

        while True:
            scheduler.enter(interval, 1, send_data)
            scheduler.run()
    else:
        print("Failed to send the request.")


if __name__ == '__main__':
    main()
