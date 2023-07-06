class Movement:
    """
    Movement class is used to get the direction of the eye to use it for controlling the movement.
    """

    def __init__(self):
        """
        Initialize Movement object
        """
        self.__total_blinks = 0
        self.__left_counter = 0
        self.__right_counter = 0
        self.__forward_counter = 0
        self.__eye_direction_frame = 10
        self.__is_right = False
        self.__is_left = False
        self.__is_forward = False
        self.__is_stopped = False
        self.__gaze_ratio = 4
        self.__is_running = False
        self.__no_movement = True

    def run(self):
        """
        Run the driver function if the total blinks are between 2 and 3 and stop if the total blinks are more than 3.

        :return: None
        """
        if 2 <= self.__total_blinks <= 3:
            self.__is_running = True
        elif self.__total_blinks > 3:
            self.__total_blinks = 0
            self.__is_running = False
        else:
            self.__is_running = False

    def driver(self):
        """
        Driver function to control the movement.

        :return: None
        """
        self.run()
        # self.__is_running = True
        if self.__is_running:
            if sum([self.__is_forward, self.__is_left, self.__is_right, self.__no_movement]) > 1:
                self.reset()
                self.__no_movement = True
            else:
                if self.move_forward():
                    self.__no_movement = False
                    self.__is_forward = True

                if self.move_left():
                    self.__no_movement = False
                    self.__is_left = True

                if self.move_right():
                    self.__no_movement = False
                    self.__is_right = True

                if self.no_movement():
                    self.__no_movement = True

        # if self.__is_forward and self.__is_left or self.__is_forward and self.__is_right or self.__is_left and self.__is_right:
        #     self.reset()

    def move_counter_reset(self):
        """
        Reset direction counters to 0 for a certain number of frames and not blinking.

        :return: None
        """
        self.__right_counter = 0
        self.__left_counter = 0
        self.__forward_counter = 0

    def move_forward(self):
        """
        Move forward if gaze ratio is 1 for a certain number of frames and not blinking.

        :return: None
        """
        if self.__gaze_ratio == 1:
            self.__forward_counter += 1
        # cv2.putText(frame, "STATE : FORWARD", (50, 100), FONT, 1, (0, 0, 255), 3)
        if self.__forward_counter >= self.__eye_direction_frame:
            # self.move_counter_reset()
            return True
            # print('Forward')

    def move_left(self):
        """
        Move left if gaze ratio is 0 for a certain number of frames and not blinking.

        :return: None
        """
        if self.__gaze_ratio == 0:
            self.__left_counter += 1
        # cv2.putText(frame, "STATE : LEFT", (50, 100), FONT, 1, (0, 0, 255), 3)
        if self.__left_counter >= self.__eye_direction_frame:
            # self.move_counter_reset()
            return True
            # print('Left')

    def move_right(self):
        """
        Move right if gaze ratio is 2 for a certain number of frames and not blinking.

        :return: None
        """
        if self.__gaze_ratio == 2:
            self.__right_counter += 1
        # cv2.putText(frame, "STATE : RIGHT", (50, 100), FONT, 1, (0, 0, 255), 3)
        if self.__right_counter >= self.__eye_direction_frame:
            # self.move_counter_reset()
            return True
            # print('Right')

    def is_stopped(self):
        """
        Stop if blink count is 2.

        :return: None
        """
        if self.__total_blinks == 2:
            self.__total_blinks = 0
            self.reset()
            return True

    def reset(self):
        """
        Stop if gaze ratio is not 1, 0 or 2 and reset direction counters.

        :return: None
        """
        # cv2.putText(frame, "STATE : STOP", (50, 100), FONT, 1, (0, 0, 255), 3)
        self.__is_forward = False
        self.__is_left = False
        self.__is_right = False
        self.move_counter_reset()

    def set_gaze_ratio(self, gaze_ratio):
        """
        Set gaze ratio to a certain value

        :param gaze_ratio: gaze ratio value

        :return: None
        """
        self.__gaze_ratio = gaze_ratio

    def is_forward(self):
        """
        Return if it is forward or not

        :return: True if it is forward, False otherwise
        """
        if self.__is_forward:
            # self.reset()
            # self.move_counter_reset()
            return True

    def is_left(self):
        """
        Return if it is left or not

        :return: True if it is left, False otherwise
        """
        if self.__is_left:
            # self.reset()
            # self.move_counter_reset()
            return True

    def is_right(self):
        """
        Return if it is right or not

        :return: True if it is right, False otherwise
        """
        if self.__is_right:
            # self.reset()
            # self.move_counter_reset()
            return True

    def no_movement(self):
        """
        Return if it is moving or not (forward, left or right)

        :return: True if it is not moving, False otherwise
        """
        if self.__gaze_ratio == -1:
            self.__no_movement = True

    def set_total_blinks(self, total_blinks):
        """
        Set total blinks to a certain value

        :param total_blinks: total blinks value

        :return: None
        """
        self.__total_blinks = total_blinks % 4

    def set_eye_direction_frame(self, eye_direction_frame):
        """
        Set eye direction frame to a certain value

        :param eye_direction_frame: eye direction frame value

        :return: None
        """
        self.__eye_direction_frame = eye_direction_frame

    def is_system_running(self):
        """
        Return if it is running or not

        :return: True if it is running, False otherwise
        """
        return self.__is_running

    def is_no_movement(self):
        """
        Return if it is not moving or not

        :return: True if it is not moving, False otherwise
        """
        return self.__no_movement
