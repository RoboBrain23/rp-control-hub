"""
streamer.py

The `streamer.py` module is a crucial component of the RP Control Hub system.
It enables seamless streaming of sensor data from Raspberry Pi to a backend API.
This module establishes a connection with the backend API and periodically sends sensor data,
allowing real-time monitoring and analysis of the collected information.
"""
import requests
import json
import time

# from logger import app_logger
# logger = app_logger


class Streamer:
    def __init__(self, url, interval_in_seconds=7):
        self.identity = {}
        self.sensor_data = {}
        self.access_token = ""
        self.headers = {"Content-Type": "application/json"}
        self.interval = interval_in_seconds
        self.url = url
        self.login_endpoint = f"{self.url}/chair/login"
        self.sensor_data_endpoint = f"{self.url}/chair/data"

    def login(self):
        json_identity = json.dumps(self.identity)
        response = requests.post(self.login_endpoint, data=json_identity, headers=self.headers)

        if response.status_code == 200:
            print("Login successfully!. Status code:", response.status_code)
            res = json.loads(response.text)
            self.access_token = f"Bearer {res['access_token']}"
            self.headers["Authorization"] = self.access_token
            return response.status_code
        else:
            print("Sign-in Failed. Status code:", response.status_code)
            print(response.text)
            return response.status_code

    def send_data(self, data):
        req_body = data

        json_data = json.dumps(req_body)
        response = requests.post(self.sensor_data_endpoint, data=json_data, headers=self.headers)

        # Check the response status code
        if response.status_code == 201:
            print("Request sent successfully!. Status code:", response.status_code)
            print(response.text)
        elif response.status_code == 401:
            print("Trying to login again")
            self.login()
        else:
            print("Failed to send the request. Status code:", response.status_code)
            print(response.text)

    def get_identity(self):
        return self.identity

    def set_identity(self, chair_id, password):
        self.identity["chair_id"] = chair_id
        self.identity["password"] = password

    def get_sensor_data(self):
        return self.sensor_data

    def set_sensor_data(self, data):
        self.sensor_data = {
            "temperature": data["temperature"],
            "oximeter": data["oximeter"],
            "pulse_rate": data["pulse_rate"]
        }

    def set_url(self, url: str):
        self.url = url

    def stream(self):
        login_status_code = self.login()

        if login_status_code == 200:
            while True:
                self.send_data(self.sensor_data)
                time.sleep(self.interval)
        else:
            print("Failed to send the request.")
