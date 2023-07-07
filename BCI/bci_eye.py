import cv2
import mediapipe as mp
import math
import numpy as np
import time
from bci_calibration import Calibration


class Eye:
    LEFT_IRIS_POINT = 468
    RIGHT_IRIS_POINT = 473
    LEFT_EYE_WIDTH_POINTS = [163, 154]
    RIGHT_EYE_WIDTH_POINTS = [381, 390]
    LEFT_EYE_HEIGHT_POINTS = [161, 163]
    RIGHT_EYE_HEIGHT_POINTS = [390, 388]
    LEFT_P = 161
    RIGHT_P = 388

    def __init__(self, side):
        """
        Initialize Eye object

        :param side: eye side (left or right)

        """
        self.__side = side
        self.__frame = None
        self.__landmarks = None
        self.calibration = Calibration()
        if self.__side.lower() == "left":
            self.__iris = self.LEFT_IRIS_POINT
            self.__width = self.LEFT_EYE_WIDTH_POINTS
            self.__height = self.LEFT_EYE_HEIGHT_POINTS
            self.__cal_p = self.LEFT_P

        elif self.__side.lower() == "right":
            self.__iris = self.RIGHT_IRIS_POINT
            self.__width = self.RIGHT_EYE_WIDTH_POINTS
            self.__height = self.RIGHT_EYE_HEIGHT_POINTS
            self.__cal_p = self.RIGHT_P

        self.__face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    def process(self):
        iris = self.get_point(self.__iris)
        eye_width = self.get_eye_width()
        eye_height = self.get_eye_height()
        return iris, eye_width, eye_height

    def get_eye_width(self):
        eye_width = abs(self.get_point(self.__width[0])[0] - self.get_point(self.__width[1])[0])
        return eye_width

    def get_eye_height(self):
        eye_height = abs(self.get_point(self.__height[0])[1] - self.get_point(self.__height[1])[1])
        return eye_height

    def get_point(self, point):
        return self.__landmarks[point].x, self.__landmarks[point].y

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def calibrate(self, cam, calibration_time=25):
        center_x = 0
        center_y = 0
        p_x = 0
        p_y = 0
        width = 0
        height = 0
        for _ in range(calibration_time):
            _, frame = cam.read()
            self.update(frame)
            p_x += self.get_point(self.__cal_p)[0]
            p_y += self.get_point(self.__cal_p)[1]
            iris, eye_width, eye_height = self.process()
            center_x += iris[0]
            center_y += iris[1]
            width += eye_width
            height += eye_height
        center_x /= calibration_time
        center_y /= calibration_time
        p_x /= calibration_time
        p_y /= calibration_time
        width /= calibration_time
        height /= calibration_time
        a = abs(p_x - center_x)
        b = abs(p_y - center_y)
        ratio_width = (width - a) / a
        ratio_height = (height - b) / b
        return center_x, center_y, ratio_width, ratio_height, width, height

    def get_iris(self):
        iris = self.get_point(self.__iris)
        return iris

    def update(self, frame):
        self.__frame = frame
        self.__frame = cv2.flip(frame, 1)
        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB)
        output = self.__face_mesh.process(self.__frame)
        landmark_points = output.multi_face_landmarks
        if landmark_points:
            self.__landmarks = landmark_points[0].landmark
