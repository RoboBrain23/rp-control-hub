import time
import streamer
import random
import threading

from logger import app_logger

URL = "http://localhost:3000"
STREAMER_INTERVAL = 5
DATA_LISTENER_INTERVAL = 0.5

has_id = False

logger = app_logger

data = {
    "chair_id": "5",
    "password": "10101",
    "temperature": 0,
    "oximeter": 0,
    "pulse_rate": 0,
    "flag": -1
}

lock = threading.Lock()
streamer = streamer.Streamer(URL, STREAMER_INTERVAL)


def update_data():
    global data
    while True:
        with lock:
            data["chair_id"] = "5"
            data["password"] = "10101"
            data["temperature"] = random.randint(1, 100)
            data["oximeter"] = random.randint(1, 100)
            data["pulse_rate"] = random.randint(1, 100)
        time.sleep(DATA_LISTENER_INTERVAL)


def stream():
    global data
    global has_id

    while not has_id:
        if data["chair_id"] != "" and data["password"] != "":
            has_id = True
        time.sleep(1)
        logger.warning(f"Chair has no id or password, chair_id: '{data['chair_id']}', password: '{data['password']}'")

    while True:
        d = {
            "temperature": data["temperature"],
            "oximeter": data["oximeter"],
            "pulse_rate": data["pulse_rate"]
        }
        try:
            streamer.send_data(d)
            time.sleep(streamer.interval)
        except:
            logger.error(f"Can't stream this data: {d}")


if __name__ == '__main__':
    t1 = threading.Thread(target=update_data, name="data_listener_thread")
    t2 = threading.Thread(target=stream, name="streamer_thread")

    t1.start()
    t2.start()

