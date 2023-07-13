import time
import streamer
import random
import threading
from multiprocessing import Process, Manager, Value
from queue import Queue
import os
import sys
import serial

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, 'Gaze'))
sys.path.append(os.path.join(ROOT_DIR, 'BCI'))
# sys.path.append(os.path.join(ROOT_DIR, 'BCI\\config'))
# sys.path.append(os.path.join(ROOT_DIR, 'BCI\\stimulus'))


from logger import app_logger
from Gaze import gaze_main as gaze
from BCI import bci_main as bci

logger = app_logger

URL = "url"
STREAMER_INTERVAL = 5
GET_ARDUINO_DATA_INTERVAL = 3
SEND_ARDUINO_DATA_INTERVAL = 0.1
MODE_RESPONSE_INTERNAL = 1

NO_FLAG = 0
GAZE_FLAG = 1
BCI_FLAG = 2

# GAZE Constants
gaze_constants = {
    'STOP': -1,
    'NO_MOVEMENT': 0,
    'FORWARD': 1,
    'RIGHT': 2,
    'LEFT': 3
}

direction = Value('u', 'p')

data = {
    "chair_id": "777",
    "password": "mypassword",
    "temperature": 0,
    "oximeter": 0,
    "pulse_rate": 0,
    "flag": NO_FLAG
}
has_id = False

lock = threading.Lock()
streamer = streamer.Streamer(URL, STREAMER_INTERVAL)


def get_arduino_data():
    global data
    while True:
        with lock:
            data["chair_id"] = "777"
            data["password"] = "mypassword"
            data["temperature"] = random.randint(1, 100)
            data["oximeter"] = random.randint(1, 100)
            data["pulse_rate"] = random.randint(1, 100)
            data["flag"] = BCI_FLAG
        time.sleep(GET_ARDUINO_DATA_INTERVAL)


def send_arduino_data():
    global direction
    locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3', '/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3']

    for device in locations:
        try:
            print ("Trying..., {device}")
            arduino = serial.Serial("com7", 9600, timeout=0.1)
            break
        except:
            print ("Failed to connect on, {device}")
    
    if data['flag'] == BCI_FLAG:
        while True:
            if direction.value != 'p' and direction.value != 'S':
                arduino.write(bytes(str(direction.value), 'utf-8'))
                arduino.write(bytes('\n', 'utf-8'))
                print(direction.value)
                time.sleep(2)
                direction.value = "S"
                arduino.write(bytes(str(direction.value), 'utf-8'))
                arduino.write(bytes('\n', 'utf-8'))
                print(direction.value)
                time.sleep(0.25)


    # last_comm = 'p'
    # while True:
    #     if direction.value != 'p':
    #         # if last_comm != direction.value:
    #         #     last_comm = direction.value
    #         #     print(f"SENDING TO ARDUINO : {direction.value}")
    #         #     arduino.write(bytes(str(direction.value), 'utf-8'))
    #         #     arduino.write(bytes('\n', 'utf-8'))
    #         print(f"SENDING TO ARDUINO : {direction.value}")
    #         arduino.write(bytes(str(direction.value), 'utf-8'))
    #         arduino.write(bytes('\n', 'utf-8'))

        time.sleep(SEND_ARDUINO_DATA_INTERVAL)


def stream():
    global data
    global has_id

    while not has_id:
        if data["chair_id"] != "" and data["password"] != "":
            has_id = True
            streamer.set_identity(data['chair_id'], data['password'])
            break
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
        except:
            logger.error(f"Can't stream this data: {d}")
        time.sleep(streamer.interval)


def run_gaze(direct):
    gaze.run_gaze(direct)


def run_bci(direct):
    bci.run_bci(direct)


if __name__ == '__main__':
    current_flag = data['flag']

    t1 = threading.Thread(target=get_arduino_data, name="data_listener_thread", daemon=True)
    t2 = threading.Thread(target=stream, name="streamer_thread", daemon=True)
    t3 = threading.Thread(target=send_arduino_data, name="send_arduino_data_thread", daemon=True)

    t1.start()
    t2.start()
    t3.start()

    manger = Manager()
    # direction = manger.dict({'direction': gaze_constants['NO_MOVEMENT']})
    # direction = Value('i', gaze_constants['NO_MOVEMENT'])
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
                gaze_process = Process(target=run_gaze, args=(direction,), name="GazeProcess")
                process_queue.put(gaze_process)
                gaze_process.start()
                current_flag = GAZE_FLAG
        elif desired_flag == BCI_FLAG:
            if current_flag != BCI_FLAG:
                if not process_queue.empty():
                    p = process_queue.get()
                    p.terminate()
                bci_process = Process(target=run_bci, args=(direction,), name="BciProcess")
                process_queue.put(bci_process)
                bci_process.start()
                current_flag = BCI_FLAG
        else:
            logger.warning(f"UNKNOWN DESIRED FLAG: {desired_flag}!")

        # logger.info(f"Current flag is: {current_flag}")
        time.sleep(MODE_RESPONSE_INTERNAL)
