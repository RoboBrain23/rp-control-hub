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

RECEIVER_ARDUINO_PORT = "com7"
SENDER_ARDUINO_PORT = "com8"
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
    sender_arduino = None
    while True:
        if not sender_arduino.is_open:
            try:
                print("Trying to connect to arduino")
                sender_arduino = serial.Serial(SENDER_ARDUINO_PORT, 9600, timeout=0.1)
                time.sleep(2)
            except:
                print(f"Failed to connect on, {SENDER_ARDUINO_PORT}")
                continue
        print(f"Connected to arduino with port, {SENDER_ARDUINO_PORT}")

        sender_arduino.reset_input_buffer()
        while True:
            if sender_arduino.in_waiting > 0:
                line = sender_arduino.readline().decode('utf-8').rstrip()
                print(f"Received from arduino: {line}")
                data = line.split('#')
                with lock:
                    data["temperature"] = data[1]
                    data["oximeter"] = data[3]
                    data["pulse_rate"] = data[2]
                    data["flag"] = data[0]
                time.sleep(GET_ARDUINO_DATA_INTERVAL)

    # while True:
    #     with lock:
    #         data["chair_id"] = "777"
    #         data["password"] = "mypassword"
    #         data["temperature"] = random.randint(1, 100)
    #         data["oximeter"] = random.randint(1, 100)
    #         data["pulse_rate"] = random.randint(1, 100)
    #         data["flag"] = GAZE_FLAG
    #     time.sleep(GET_ARDUINO_DATA_INTERVAL)


def send_arduino_data():
    global direction
    receiver_arduino = None
    # last_comm = 'p'

    while True:
        if not receiver_arduino.is_open:
            try:
                print("Trying to connect to arduino")
                receiver_arduino = serial.Serial(RECEIVER_ARDUINO_PORT, 9600, timeout=0.1)
                time.sleep(2)
            except:
                print(f"Failed to connect on, {RECEIVER_ARDUINO_PORT}")
                continue
        print(f"Connected to arduino with port, {RECEIVER_ARDUINO_PORT}")

        if data['flag'] == BCI_FLAG:
            while True:
                if direction.value != 'p' and direction.value != 'S':
                    receiver_arduino.write(bytes(str(direction.value), 'utf-8'))
                    receiver_arduino.write(bytes('\n', 'utf-8'))
                    print(direction.value)
                    time.sleep(2)
                    direction.value = "S"
                    receiver_arduino.write(bytes(str(direction.value), 'utf-8'))
                    receiver_arduino.write(bytes('\n', 'utf-8'))
                    print(direction.value)
                    time.sleep(SEND_ARDUINO_DATA_INTERVAL)
                    if data['flag'] != BCI_FLAG:
                        break
        elif data['flag'] == GAZE_FLAG:
            while True:
                if direction.value != 'p':
                    # if last_comm != direction.value:
                    #     last_comm = direction.value
                    #     print(f"SENDING TO ARDUINO : {direction.value}")
                    #     arduino.write(bytes(str(direction.value), 'utf-8'))
                    #     arduino.write(bytes('\n', 'utf-8'))
                    print(f"SENDING TO ARDUINO : {direction.value}")
                    receiver_arduino.write(bytes(str(direction.value), 'utf-8'))
                    receiver_arduino.write(bytes('\n', 'utf-8'))
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
