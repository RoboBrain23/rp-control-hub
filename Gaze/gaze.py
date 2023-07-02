import cv2
import numpy as np


class Gaze:
    """
    This class detects the direction of the gaze (left, right, up)
     by comparing number of white pixels in each part of eye region.
    """

    def __init__(self, eye_region, mask, gray):
        """
        Initialize Gaze object

        :param eye_region: eye region

        :param mask: mask of eye region

        :param gray: gray image
        """
        self.__eye_region = eye_region
        self.__threshold = 42
        self.__mask = mask
        self.__gray = gray

    def get_gaze_ratio(self):
        # Todo: Improve direction detection by setting good range for each direction
        """
        Get gaze ratio by comparing number of white pixels in each part of eye region (left, right, up, center).

        :return: gaze ratio value (0 for left, 2 for right, 1 for up(Forward))
        """
        eye_threshold = self.get_eye_threshold(self.__eye_region)
        height, width = eye_threshold.shape

        up_side_eye_threshold = eye_threshold[0:int(height / 3), 0:width]
        up_side_eye_threshold_white = cv2.countNonZero(up_side_eye_threshold)

        left_side_eye_threshold = eye_threshold[int(height / 3):int(2 * height / 3), 0:int(width / 3)]
        left_side_eye_threshold_white = cv2.countNonZero(left_side_eye_threshold)

        center_side_eye_threshold = eye_threshold[int(height / 3):int(2 * height / 3),
                                    int(width / 3):int(2 * width / 3)]
        center_side_eye_threshold_white = cv2.countNonZero(center_side_eye_threshold)

        right_side_eye_threshold = eye_threshold[int(height / 3):int(2 * height / 3), int(2 * width / 3):]
        right_side_eye_threshold_white = cv2.countNonZero(right_side_eye_threshold)

        down_side_eye_threshold = eye_threshold[int(height / 3):, 0:width]
        down_side_eye_threshold_white = cv2.countNonZero(down_side_eye_threshold)

        # cv2.imshow('left', left_side_eye_threshold)
        # cv2.imshow('right', right_side_eye_threshold)
        # cv2.imshow('center', center_side_eye_threshold)
        # cv2.imshow('up', up_side_eye_threshold)
        # cv2.imshow('down', down_side_eye_threshold)

        # left
        if left_side_eye_threshold_white < right_side_eye_threshold_white \
                and left_side_eye_threshold_white < center_side_eye_threshold_white \
                and left_side_eye_threshold_white < down_side_eye_threshold_white \
                and left_side_eye_threshold_white < up_side_eye_threshold_white:
            gaze_ratio = 0
        # right
        elif right_side_eye_threshold_white < left_side_eye_threshold_white \
                and right_side_eye_threshold_white < center_side_eye_threshold_white \
                and right_side_eye_threshold_white < down_side_eye_threshold_white \
                and right_side_eye_threshold_white < up_side_eye_threshold_white:
            gaze_ratio = 2

        # # center
        # elif center_side_eye_threshold_white<left_side_eye_threshold_white \
        #         and center_side_eye_threshold_white<right_side_eye_threshold_white \
        #         and center_side_eye_threshold_white<down_side_eye_threshold_white \
        #         and center_side_eye_threshold_white<up_side_eye_threshold_white:
        #     gaze_ratio = 1
        # up (forward)
        elif up_side_eye_threshold_white < left_side_eye_threshold_white \
                and up_side_eye_threshold_white < right_side_eye_threshold_white \
                and up_side_eye_threshold_white < center_side_eye_threshold_white \
                and up_side_eye_threshold_white < down_side_eye_threshold_white:
            gaze_ratio = 1
        # down (stop)
        else:
            gaze_ratio = 4

        return gaze_ratio

    def get_min_max_eye_region(self):
        """
        get furthest point and nearst point positions

        :return: min_x, max_x, min_y, max_y (furthest point and nearst point positions)
        """
        min_x = np.min(self.__eye_region[:, 0])
        max_x = np.max(self.__eye_region[:, 0])
        min_y = np.min(self.__eye_region[:, 1])
        max_y = np.max(self.__eye_region[:, 1])
        return min_x, max_x, min_y, max_y

    def get_eye_threshold(self, eye_region):
        """
        get eye threshold from eye region

        :param eye_region: eye region

        :return: eye threshold
        """

        min_x, max_x, min_y, max_y = self.get_min_max_eye_region()
        cv2.polylines(self.__mask, [eye_region], True, 0, 5)
        cv2.fillPoly(self.__mask, [eye_region], 255)
        gray_eye = cv2.bitwise_and(self.__gray, self.__gray, mask=self.__mask)
        eye = gray_eye[min_y:max_y, min_x:max_x]
        eye = cv2.resize(eye, None, fx=5, fy=5)
        _, eye_threshold = cv2.threshold(eye, self.__threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('eye_threshold', eye_threshold)
        return eye_threshold

    def set_threshold(self, threshold):
        """
        set eye threshold

        :param threshold: threshold value

        :return: None
        """
        self.__threshold = threshold

    def get_threshold(self):
        """
        get eye threshold

        :return: threshold value
        """
        return self.__threshold

    def get_eye_region(self):
        """
        get eye region

        :return: eye region
        """
        return self.__eye_region
