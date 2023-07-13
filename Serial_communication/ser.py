import serial
import time


# Establish serial connection
arduino = serial.Serial('com20', 9600, timeout=0.1)  # Replace '/dev/ttyACM0' with the appropriate port for your Arduino
arduino.reset_input_buffer()
# time.sleep(1)  # Allow time for the Arduino to initialize

# locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',
# '/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3']

# for device in locations:
#     try:
#         print (f"Trying..., {device}")
#         arduino = serial.Serial(device, 9600)
#         arduino.reset_input_buffer()
#         break
#     except:
#         print (f"Failed to connect on, {device}")
# print("Established serial connection to Arduino")
# Function to send string to Arduino
def send_string_to_arduino(string):
    # arduino.write(bytes(str(string), 'utf-8'))
    # arduino.write(bytes('\n', 'utf-8'))
    full_string = f"{string}\n"
    arduino.write(full_string.encode('utf-8'))
    #data = arduino.readline().decode('utf-8').rstrip()
    # return '\0'
    # arduino.write(b'\n')  # Add a newline character to mark the end of the string
    # arduino.write(b'F')

# print(arduino)

# # Send string every 1 second
# while True: 
#     time.sleep(.05)
#     # arduino.reset_input_buffer()
#     # arduino.reset_output_buffer()
#     print("line: 36")
#     if arduino.inWaiting() > 0:
#         print("line: 38")
#         line = arduino.readline().decode('utf-8').rstrip()
#         print("line: 40")
#         time.sleep(.005)
#         print(line)
#         # time.sleep(1)
    
#     string_to_send = "F"
#     # send_string_to_arduino(string_to_send)
#     print("line: 47")
#     arduino.write(b"F\n")
#     time.sleep(.001)
#     print("buzz")
#     # time.sleep(2)
#     string_to_send = 'S'
#     # send_string_to_arduino(string_to_send)
#     print("line: 54")
#     arduino.write(b"S\n")
#     print("line: 56")
#     time.sleep(.005)
#     print("stop")
#     # time.sleep(2)

while True:
    arduino.reset_input_buffer()
    send_string_to_arduino("F")
    line = arduino.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(0.5)
    arduino.reset_input_buffer()
    send_string_to_arduino("S")
    line = arduino.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(0.5)
# print(arduino)



# # Function to read string from Arduino
# def read_string_from_arduino():
#     if arduino.in_waiting > 0:
#         incoming_data = arduino.readline().decode().rstrip('\n')
#         print(incoming_data)
#         return incoming_data
#     else:
#         return None

# print("Reading from Arduino")
# # Read data from Arduino
# while True:
#     received_string = read_string_from_arduino()
#     if received_string is not None:
#         print("Received string:", received_string)
#     time.sleep(1)
#         # Add your code to process the received string here
# import serial
# import time

# Establish serial communication with Arduino
# arduino = serial.Serial('COM20', 9600)  # Replace 'COM3' with the appropriate port name

# Wait for the Arduino to initialize
# time.sleep(1)
# arduino.timeout = 2
# arduino.readline()

# while True:
#     print("Starting loop...")
#     # Send data to Arduino every 1 second
#     try:
#         # Send string every 1 second
#         while True:
            
#             string_to_send = 'F\n'
#             # send_string_to_arduino(string_to_send)
#             arduino.write(string_to_send.encode())

#             print("buzz")
#             time.sleep(2)
#             string_to_send = 'S\n'
#             # send_string_to_arduino(string_to_send)
#             arduino.write(string_to_send.encode())

#             print("stop")
#             time.sleep(2)
#     except:
#         print ("Failed to send!")

    # # Read data from Arduino every 2 seconds
    # arduino.timeout = 2
    # data_received = arduino.readline().decode().rstrip()
    # if data_received:
    #     print("Received data from Arduino:", data_received)

    # # Wait for 1 second before sending the next data
    # time.sleep(1)

# Close the serial connection
# arduino.close()
