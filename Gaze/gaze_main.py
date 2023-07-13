import os

import math

import numpy as np

import dlib

from gaze import Gaze

from eye import Eye

from blink import Blink

from calibration import Calibration

from movement import Movement



from logger import app_logger

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2



logger = app_logger



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



# Todo Make constants.py file and move all constants there and import them here and in other files as well

# Todo Add comments to all functions and classes

# Todo Add docstrings to all functions and classes and generate documentation using sphinx

# Todo Make Unit tests for all functions and classes

# Todo Improve code readability and quality





# Constants

CLOSED_EYES_FRAME = 10

EYE_DIRECTION_FRAME = 10

CALIBRATION_FRAMES = 200

MODEL = "shape_predictor_68_face_landmarks.dat"

MODEL_FULL_PATH = os.path.join(ROOT_DIR, MODEL)

FONT = cv2.FONT_HERSHEY_SIMPLEX



def print_message_once(message, show_message):

    if not show_message:

        print(message)

        show_message = True

    return show_message





def run_gaze(direction):

    # Variables

    left_eye_thresh = 100
    right_eye_thresh = 100
    running_message = False
    pause_message = False
    # Objects
    calibrate = Calibration()
    movement = Movement()
    blink = Blink()
    # Set frames
    calibrate.set_cal_frames(CALIBRATION_FRAMES)
    movement.set_eye_direction_frame(EYE_DIRECTION_FRAME)
    blink.set_closed_eye_frame(CLOSED_EYES_FRAME)
    # Main
    try:
        # cap = cv2.VideoCapture(2)  # initialize camera
        cap = cv2.VideoCapture(2,cv2.CAP_DSHOW,(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY))
        # ed_time = time()
        cap.set(cv2.CAP_PROP_FPS, 30.0)
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = dlib.get_frontal_face_detector()  # initialize face detector
        predictor = dlib.shape_predictor(MODEL_FULL_PATH)  # initialize landmark detector

        while True:
            try:
                ret, frame = cap.read()  # read frame from camera
                # print(f"elapsed time: {ed_time - st_time}")

                frame = cv2.flip(frame, 1)  # flip frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to grayscale
                faces = detector(gray)  # detect faces in frame
                height, width, _ = frame.shape  # get frame dimensions
                mask = np.zeros((height, width), dtype=np.uint8)  # create black mask

                for face in faces:
                    # Detect face and draw rectangle
                    x, y = face.left(), face.top()
                    x1, y1 = face.right(), face.bottom()
                    cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
                    landmarks = predictor(gray, face)  # detect landmarks on face
                    left_eye = Eye(frame, 'left', landmarks)  # detect left eye
                    right_eye = Eye(frame, 'right', landmarks)  # detect right eye
                    # Detect blinking
                    left_eye_ratio = left_eye.blink_ratio()  # get left eye blink ratio
                    right_eye_ratio = right_eye.blink_ratio()  # get right eye blink ratio
                    # blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2  # get average blink ratio
                    blinking_ratio = left_eye_ratio
                    blink.set_blink_ratio(blinking_ratio)  # set blink ratio to Blink class
                    blink.set_blinking_threshold(
                        calibrate.get_cal_blink_threshold())  # set blink threshold to Blink class
                    # Detect eye Gaze
                    # gaze_right = Gaze(right_eye.get_eye_region(), mask, gray)  # detect right eye gaze
                    # gaze_right.set_threshold(calibrate.get_cal_right_eye_thresh())  # change right eye threshold
                    gaze_left = Gaze(left_eye.get_eye_region(), mask, gray)  # detect left eye gaze
                    gaze_left.set_threshold(calibrate.get_cal_left_eye_thresh())  # change left eye threshold
                    # Calibrate
                    calibrate.calibrate(gaze_left=gaze_left,blinking_ratio=blinking_ratio)

                    if calibrate.is_cal_threshold():

                        cv2.putText(frame, "Calibrating Threshold", (150, 50), FONT, 1, (200, 0, 200),

                                    2)  # show Calibrating Threshold message

                    elif calibrate.is_cal_blink():

                        cv2.putText(frame, "Calibrating Blinking", (150, 50), FONT, 1, (200, 0, 200),

                                    2)  # show Calibrating Blinking message

                    # Check if calibration is done and start the driver

                    if calibrate.is_calibrated():

                        total_blinks = blink.count_blinks()  # Count total blinks

                        # Check if eyes are blinking

                        if blink.is_blinking():

                            cv2.putText(frame, "BLINKING", (50, 150), FONT, 3, (255, 0, 0))  # show blinking message



                        cv2.putText(frame, f'Total Blinks: {total_blinks}', (50, 350), FONT, 2, (0, 0, 255),

                                    3)  # show total blinks

                        # Get total gaze ratio by averaging the left and right eye gaze ratio

                        # if gaze_right.get_gaze_ratio() is not None and gaze_left.get_gaze_ratio() is not None:
                        #
                        #     # print(gaze_right.get_gaze_ratio(), gaze_left.get_gaze_ratio())  # print gaze ratio
                        #
                        #     gaze_ratio = math.ceil((gaze_right.get_gaze_ratio() + gaze_left.get_gaze_ratio()) / 2)
                        #
                        #     # print(gaze_ratio)
                        #
                        # else:
                        #
                        #     gaze_ratio = -1
                        if gaze_left.get_gaze_ratio() is not None:
                            gaze_ratio = gaze_left.get_gaze_ratio()
                        else:
                            gaze_ratio = -1


                        # Run the driver

                        movement.set_total_blinks(total_blinks)

                        movement.set_gaze_ratio(gaze_ratio)

                        movement.driver()

                        # Check if system is paused

                        if movement.is_system_running():

                            cv2.putText(frame, "RUNNING", (50, 100), FONT, 1, (255, 0, 0), 3)

                            running_message = print_message_once(

                                "\nSYSTEM IS RUNNING, PLEASE BLINK 2 TIMES TO PAUSE IT", running_message)

                            pause_message = False



                            # print(gaze_right.get_gaze_ratio(), gaze_left.get_gaze_ratio())

                            # print(movement.get_center_counter())

                            # if movement.is_stopped():

                            #     cv2.putText(frame, "STOP", (50, 100), FONT, 1, (0, 255, 255), 3) # show stop message

                            #     print("stop")



                            if movement.is_forward():

                                cv2.putText(frame, "FORWARD", (50, 100), FONT, 1, (0, 0, 255),

                                            3)  # show forward message

                                direction.value = 'F'



                            elif movement.is_left():

                                cv2.putText(frame, "LEFT", (50, 100), FONT, 1, (0, 0, 255), 3)  # show left

                                direction.value = 'L'



                            elif movement.is_right():

                                cv2.putText(frame, "RIGHT", (50, 100), FONT, 1, (0, 0, 255), 3)  # show right message

                                direction.value = 'R'



                            elif movement.is_no_movement():

                                cv2.putText(frame, "NO-MOVEMENT", (50, 100), FONT, 1, (0, 0, 255),

                                            3)  # show no movement message

                                direction.value = 'S'

                        else:

                            cv2.putText(frame, "PAUSED", (50, 100), FONT, 1, (255, 0, 0), 3)

                            pause_message = print_message_once("\nSYSTEM IS PAUSED, PLEASE BLINK 2 TIMES TO START IT",

                                                               pause_message)

                            running_message = False

                            direction.value = 'p'



                cv2.imshow('frame', frame)

                # cv2.imshow('mask',mask)



                if cv2.waitKey(1) & 0xFF == ord('q'):  # Wait for 'q' key to stop the program

                    break

            except Exception as e:

                print("Error processing the frame:", e)

                pass

        cap.release()

        cv2.destroyAllWindows()

    except Exception as e:

        print("Error initializing the camera or the facial landmark model:", e)



if __name__ == "__main__":

    run_gaze()

