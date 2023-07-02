# Gaze Controller

## Description
This repository contains code for a gaze tracking project, aimed at detecting and tracking the direction of a person's gaze. The project uses computer vision techniques to perform this task.

## Contents
The repository contains the following files:
- `blink.py`: contains code for detecting blinks in a person's eyes.
- `calibration.py`: contains code for calibrating the gaze tracking system.
- `eye.py`: contains code for detecting and processing the person's eye region.
- `gaze.py`: contains code for estimating the gaze direction.
- `movement.py`: contains code for getting the directions of the eyes.
- `main.py`: the main file that ties all the other files together and runs the gaze tracking system.
- `requirements.txt`: contains a list of the required packages for running the code.
- `shape_predictor_68_face_landmarks.dat`: a pre-trained model used for detecting facial landmarks.

## Requirements
The project requires the following packages to be installed:
- `dlib`
- `opencv-python`
- `numpy`

You can install the required packages by running the following command:
```
pip install -r requirements.txt
```

## Usage
To run the gaze tracking system, simply run the `main.py` file:
```
python main.py
```
