import cv2
import numpy as np
import sys

class Calibration:
    """Calibration class for calibrating eye threshold and blink threshold"""

    def __init__(self, calibration_frames=200):
        """
        Initialize Calibration object
        """
        self.__blink_threshold = 10
        self.__blink_ratios = []
        self.__calibration_frames = calibration_frames
        self.__is_calibrated = False
        self.__done = False
        self.__left_eye_thresh = 42
        self.__right_eye_thresh = 42
        self.__is_cal_threshold = False
        self.__is_cal_blink = False
        self.__calibration_frames_count = 0

    @staticmethod
    def threshold_calibrate(eye_gaze, thresh):
        """
        Calibrate eye threshold by comparing number of white pixels in eye region.
        if percentage of white pixels is less than 20, decrease threshold by 1
        if percentage of white pixels is greater than 25, increase threshold by 1

        :param eye_gaze: Eye object

        :param thresh: current threshold

        :return: thresh the updated threshold
        """
        eye_threshold = eye_gaze.get_eye_threshold(eye_gaze.get_eye_region())
        nonzero_percentage = cv2.countNonZero(eye_threshold) / (eye_threshold.shape[0] * eye_threshold.shape[1]) * 100
        if nonzero_percentage < 20 and thresh > 0:
            thresh -= 2
        elif nonzero_percentage > 25 and thresh < 255:
            thresh += 2
        return thresh

    def blink_calibrate(self):
        """
        Calibrate blink threshold by calculating mean of blink ratios that are greater than 4.

        :return: None
        """
        if len(self.__blink_ratios) > 0:
            blinks = np.array(self.__blink_ratios)
            self.__blink_threshold = np.mean(blinks)
        else:
            self.__blink_threshold = 2.7

    def add_blink_ratio(self, blink_ratio, blink_threshold=3):
        """
        Add blink ratio to list of blink ratios if blink ratio is greater than blink_threshold (default 3)

        :param blink_threshold: blink threshold to compare with blink ratio

        :param blink_ratio: blink ratio

        :return: None
        """
        if blink_ratio > blink_threshold:
            self.__blink_ratios.append(blink_ratio)

    def get_cal_blink_threshold(self):
        """
        Get calibrated blink threshold value

        :return: blink threshold
        """
        return self.__blink_threshold

    def get_cal_frames(self):
        """
        Get calibration frames

        :return: calibration frames
        """
        return self.__calibration_frames

    def set_cal_frames(self, frames):
        """
        Set calibration frames

        :param frames: calibration frames

        :return: None
        """
        self.__calibration_frames = frames

    def calibrate(self, gaze_left=None, gaze_right=None, blinking_ratio=4):
        """
        Calibrate eye threshold and blink threshold

        :param gaze_left:  Eye object

        :param gaze_right: Eye object

        :param blinking_ratio:  blink ratio value

        :return: None
        """
        if self.__calibration_frames_count < self.__calibration_frames // 2:
            sys.stdout.write('\rCalibrating Eye Threshold... {0}%'.format(self.__calibration_frames_count % (self.__calibration_frames // 2)))
            sys.stdout.flush()
            self.__is_cal_blink = False
            self.__is_cal_threshold = True
            if gaze_left is not None:
                self.__left_eye_thresh = self.threshold_calibrate(gaze_left, self.__left_eye_thresh)
            if gaze_right is not None:
                self.__right_eye_thresh = self.threshold_calibrate(gaze_right, self.__right_eye_thresh)
            self.__calibration_frames_count += 1
            # print(f'Left eye threshold: {self.__left_eye_thresh}')
            # print(f'Right eye threshold: {self.__right_eye_thresh}')
        elif self.__calibration_frames > self.__calibration_frames_count >= self.__calibration_frames // 2:
            sys.stdout.write('\rCalibrating Blinking Threshold... {0}%'.format((self.__calibration_frames_count-(self.__calibration_frames // 2))+1 % (self.__calibration_frames // 2)))
            sys.stdout.flush()
            # todo: calibrate blinking threshold
            self.__is_cal_blink = True
            self.__is_cal_threshold = False
            self.__calibration_frames_count += 1
            self.add_blink_ratio(blinking_ratio)
            # print(f'Blink ratio: {blinking_ratio}')
        elif self.__calibration_frames == self.__calibration_frames_count:
            self.__is_cal_blink = False
            self.__is_cal_threshold = False
            self.blink_calibrate()
            self.__is_calibrated = True
        if self.__is_calibrated and not self.__done:
            # print(f'Blinking threshold: {self.get_cal_blink_threshold()}')
            sys.stdout.write('\rCalibration Done! Press "q" in the video frame or Ctrl+C in the terminal to quit.')
            sys.stdout.flush()
            self.__done = True

    def set_left_eye_thresh(self, thresh):
        """
        Set left eye threshold

        :param thresh: threshold of left eye

        :return:  None
        """
        self.__left_eye_thresh = thresh

    def set_right_eye_thresh(self, thresh):
        """
        Set right eye threshold

        :param thresh: threshold of right eye

        :return:  None
        """
        self.__right_eye_thresh = thresh

    def get_cal_left_eye_thresh(self):
        """
        Get calibrated left eye threshold

        :return: left eye threshold
        """
        return self.__left_eye_thresh

    def get_cal_right_eye_thresh(self):
        """
        Get calibrated right eye threshold

        :return: right eye threshold
        """
        return self.__right_eye_thresh

    def is_calibrated(self):
        """
        Check if calibration is done

        :return: True if calibration is done, False otherwise
        """
        return self.__is_calibrated

    def is_cal_blink(self):
        """
        Check if calibration is done for blink threshold

        :return: True if calibration is done, False otherwise
        """
        return self.__is_cal_blink

    def is_cal_threshold(self):
        """
        Check if calibration is done for eye threshold

        :return: True if calibration is done, False otherwise
        """
        return self.__is_cal_threshold
