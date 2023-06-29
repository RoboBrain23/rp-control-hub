import time
import streamer
import random
import threading
import multiprocessing
from queue import Queue

from logger import app_logger

logger = app_logger

URL = "http://localhost:3000"
STREAMER_INTERVAL = 5
DATA_LISTENER_INTERVAL = 3
MODE_RESPONSE_INTERNAL = 1

NO_FLAG = -1
GAZE_FLAG = 1
BCI_FLAG = 2

direction = ""

data = {
    "chair_id": "5",
    "password": "10101",
    "temperature": 0,
    "oximeter": 0,
    "pulse_rate": 0,
    "flag": NO_FLAG
}
has_id = False

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
            data["flag"] = random.randint(-1, 2)
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


def run_gaze():
    # TODO: IMPLEMENT GAZE CONTROL.
    global direction
    while True:
        logger.info("GAZE is running...")
        time.sleep(1)


def run_bci():
    # TODO: IMPLEMENT BCI CONTROL.
    global direction
    while True:
        logger.info("BCI is running...")
        time.sleep(1)


if __name__ == '__main__':

    current_flag = data['flag']

    t1 = threading.Thread(target=update_data, name="data_listener_thread", daemon=True)
    t2 = threading.Thread(target=stream, name="streamer_thread", daemon=True)

    t1.start()
    t2.start()

    process_queue = Queue(maxsize=1)

    while True:
        desired_flag = data['flag']

        if desired_flag == NO_FLAG:
            if current_flag != NO_FLAG:
                if not process_queue.empty():
                    p = process_queue.get()
                    p.terminate()
                current_flag = NO_FLAG
        elif desired_flag == GAZE_FLAG:
            if current_flag != GAZE_FLAG:
                if not process_queue.empty():
                    p = process_queue.get()
                    p.terminate()
                gaze_process = multiprocessing.Process(target=run_gaze, name="GazeProcess")
                process_queue.put(gaze_process)
                gaze_process.start()
                current_flag = GAZE_FLAG
        elif desired_flag == BCI_FLAG:
            if current_flag != BCI_FLAG:
                if not process_queue.empty():
                    p = process_queue.get()
                    p.terminate()
                bci_process = multiprocessing.Process(target=run_gaze, name="BciProcess")
                process_queue.put(bci_process)
                bci_process.start()
                current_flag = BCI_FLAG
        else:
            logger.warning(f"UNKNOWN DESIRED FLAG: {desired_flag}!")

        logger.info(f"Current flag is: {current_flag}")
        time.sleep(MODE_RESPONSE_INTERNAL)
