
# RP Control Hub

This project is a system that integrates Gaze tracking and Brain-Computer Interface (BCI) functionalities with an Arduino device.

## Installation

To install the project, you need to have Python and pip installed on your system. After that, you can install the project dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

You can run the project using the following command:

```bash
python main.py
```

## Features

1. **Gaze Tracking**: The `gaze_main` module is responsible for tracking the user's eye movements and determining the direction of gaze. The gaze direction is then sent to the Arduino device.

2. **Brain-Computer Interface (BCI)**: The `bci_main` module is responsible for capturing and processing brain signals to interpret the user's intentions. These interpreted signals are then sent to the Arduino device.

3. **Arduino Communication**: The system communicates with the Arduino device through the `get_arduino_data` and `send_arduino_data` functions. The `get_arduino_data` function reads data from the Arduino device and updates a global data dictionary. The `send_arduino_data` function sends the direction value (based on gaze or BCI) to the Arduino device.

4. **Data Streaming**: The system also includes a data streaming functionality, which sends data (like temperature, oximeter, and pulse rate) to a specified URL at regular intervals.

5. **Process Management**: The system can start and stop the Gaze and BCI processes based on the flag value in the global data dictionary.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any problems.


## License

This project is licensed under the MIT License.

