class Blink:
    """
    This class is used to check if the eye is blinking or not by calculating the blinking ratio of the eye.
    """

    def __init__(self):
        """
        Initialize Blink object
        """
        self.__blink_ratio = 1
        self.__threshold = 5.5
        self.__blink_count = 0
        self.__closed_eye_frame = 10
        self.__blink = False
        self.__is_closed = False
        self.__total_blinks = 0

    def set_blinking_threshold(self, blink_threshold):
        """
        set eye blinking threshold

        :param blink_threshold: threshold value

        :return: None
        """
        self.__threshold = blink_threshold

    def is_blinking(self):
        """
        Check if the eye is blinking

        :return: True if the eye is blinking else False
        """
        if self.__blink_ratio > self.__threshold:
            return True
        return False

    def is_blinking_v2(self):
        """
        Check if the eye is blinking on Ear

        :return: True if the eye is blinking else False
        """
        if self.__blink_ratio < self.__threshold:
            return True
        return False

    def get_blinking_threshold(self):
        """
        get eye blinking threshold

        :return: blinking threshold
        """
        return self.__threshold

    def set_blink_ratio(self, ratio):
        """
        Set blink ratio for eye blinking

        :param ratio: blink ratio

        :return: None
        """
        self.__blink_ratio = ratio

    def get_blink_ratio(self):
        """
        Get blink ratio for eye blinking

        :return: blink ratio
        """
        return self.__blink_ratio

    def count_blinks(self):
        """
        Count number of blinks by checking if the eye is closed for a certain number of frames
         and then open.

        :return: total number of blinks
        """
        if self.is_blinking():
            self.__is_closed = True
            # cv2.putText(frame, "BLINKING", (50, 150), FONT, 3, (255, 0, 0))
        else:
            self.__is_closed = False

        if self.__is_closed:
            self.__blink_count += 1
        else:
            self.__blink_count = 0

        if self.__blink_count == self.__closed_eye_frame:
            self.__blink = True
            self.__blink_count = 0

        if self.__blink and not self.__is_closed:
            self.__total_blinks += 1
            self.__blink = False

        return self.__total_blinks

    def set_closed_eye_frame(self, frame):
        """
        Set closed eye frame

        :param frame: closed eye frame

        :return: None
        """
        self.__closed_eye_frame = frame
