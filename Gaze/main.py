import math
import numpy as np
import cv2
import dlib
from gaze import Gaze
from eye import Eye
from blink import Blink
from calibration import Calibration
from movement import Movement

# Todo Make constants.py file and move all constants there and import them here and in other files as well
# Todo Add comments to all functions and classes
# Todo Add docstrings to all functions and classes and generate documentation using sphinx
# Todo Make Unit tests for all functions and classes
# Todo Improve code readability and quality
if __name__ == "__main__":
    # Constants
    CLOSED_EYES_FRAME = 10
    EYE_DIRECTION_FRAME = 10
    CALIBRATION_FRAMES = 200
    MODEL = "shape_predictor_68_face_landmarks.dat"
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    # Variables
    left_eye_thresh = 100
    right_eye_thresh = 100
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
        cap = cv2.VideoCapture(0)  # initialize camera
        detector = dlib.get_frontal_face_detector()  # initialize face detector
        predictor = dlib.shape_predictor(MODEL)  # initialize landmark detector

        while True:
            try:
                ret, frame = cap.read()  # read frame from camera
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
                    blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2  # get average blink ratio
                    blink.set_blink_ratio(blinking_ratio)  # set blink ratio to Blink class
                    blink.set_blinking_threshold(
                        calibrate.get_cal_blink_threshold())  # set blink threshold to Blink class
                    # Detect eye Gaze
                    gaze_right = Gaze(right_eye.get_eye_region(), mask, gray)  # detect right eye gaze
                    gaze_right.set_threshold(calibrate.get_cal_right_eye_thresh())  # change right eye threshold
                    gaze_left = Gaze(left_eye.get_eye_region(), mask, gray)  # detect left eye gaze
                    gaze_left.set_threshold(calibrate.get_cal_left_eye_thresh())  # change left eye threshold
                    # Calibrate
                    calibrate.calibrate(gaze_left, gaze_right, blinking_ratio)
                    if calibrate.is_cal_threshold():
                        cv2.putText(frame, "Calibrating Threshold", (150, 50), FONT, 1, (200, 0, 200), 2)  # show Calibrating Threshold message
                    elif calibrate.is_cal_blink():
                        cv2.putText(frame, "Calibrating Blinking", (150, 50), FONT, 1, (200, 0, 200), 2)  # show Calibrating Blinking message
                    # Check if calibration is done and start the driver
                    if calibrate.is_calibrated():
                        total_blinks = blink.count_blinks()  # Count total blinks
                        # Check if eyes are blinking
                        if blink.is_blinking():
                            cv2.putText(frame, "BLINKING", (50, 150), FONT, 3, (255, 0, 0))  # show blinking message

                        cv2.putText(frame, f'Total Blinks: {total_blinks}', (50, 350), FONT, 2, (0, 0, 255), 3)  # show total blinks
                        # Get total gaze ratio by averaging the left and right eye gaze ratio
                        gaze_ratio = math.ceil((gaze_right.get_gaze_ratio() + gaze_left.get_gaze_ratio()) / 2)
                        # Run the driver
                        movement.set_total_blinks(total_blinks)
                        movement.set_gaze_ratio(gaze_ratio)
                        movement.driver()
                        if movement.is_stopped():
                            cv2.putText(frame, "STOP", (50, 100), FONT, 1, (0, 255, 255), 3) # show stop message
                            # Todo Add stop movement code here

                        if movement.no_movement():
                            cv2.putText(frame, "NO-MOVEMENT", (50, 100), FONT, 1, (0, 0, 255), 3) # show no movement message
                            # Todo Add no movement code here

                        elif movement.is_forward():
                            cv2.putText(frame, "FORWARD", (50, 100), FONT, 1, (0, 0, 255), 3)  # show forward message
                            # Todo Add forward movement code here

                        elif movement.is_left():
                            cv2.putText(frame, "LEFT", (50, 100), FONT, 1, (0, 0, 255), 3) # show left message
                            # Todo Add left movement code here

                        elif movement.is_right():
                            cv2.putText(frame, "RIGHT", (50, 100), FONT, 1, (0, 0, 255), 3)  # show right message
                            # Todo Add right movement code here

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
