import pygame
import time
import threading
from math import sin, pi
import mediapipe as mp
import cv2
import math

NUM_OF_THREAD = 4
b = threading.Barrier(NUM_OF_THREAD)

from config import *
from Box import Box
from bci_movement import Movement
from bci_eye import Eye


# from utils.Logger import Logger, app_logger

# logger = Logger(__name__)
# logger = app_logger  # Log all in app.log


class BlankboardStimulus:
    def __init__(self):

        self._done = False
        self._frequencies = None
        self._preparation_duration = None
        self._stimulation_duration = None
        self._rest_duration = None
        self._is_full_screen = None
        self._directions_order = None

        self._screen_width = SCREEN_WIDTH
        self._screen_height = SCREEN_HEIGHT

        # Create the screen
        self._screen = None
        self.cal = True

        self._boxes = {}

    def _create_boxes(self):
        """
        Creates a list of boxes based on the position and frequency data stored in the _frequencies dictionary.
        :return:
        """
        screen_width = self._screen.get_width()
        screen_height = self._screen.get_height()

        for position, frequency in self._frequencies.items():
            box = Box(position, frequency, screen_width, screen_height)
            self._boxes[position] = box

    def run(self, frequencies: dict, preparation_duration: int, stimulation_duration: int,
            rest_duration: int, is_full_screen: bool, directions_order: list):

        """

        :param frequencies: Dictionary of the boxes frequencies.

        :param preparation_duration: The duration of the Epoc.

        :param stimulation_duration: The duration of the Epoc.

        :param rest_duration: The duration of the break.

        :param is_full_screen: Indicator to run stimulus in a full-screen mode.

        :param directions_order: List of the direction in order.

        """

        self._frequencies = frequencies
        self._preparation_duration = preparation_duration
        self._stimulation_duration = stimulation_duration
        self._rest_duration = rest_duration
        self._is_full_screen = is_full_screen
        self._directions_order = directions_order
        cam = cv2.VideoCapture(0)
        face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        # Create the screen
        self._screen = pygame.display.set_mode((0, 0),
                                               pygame.FULLSCREEN) if self._is_full_screen else pygame.display.set_mode(
            [self._screen_width, self._screen_height])
        self._create_boxes()
        pygame.init()
        # write the text on the screen
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render('+', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self._screen_width // 2, self._screen_height // 2)
        self._screen.blit(text, textRect)
        pygame.display.update()

        threads = []
        i = 0

        for box in self._boxes.values():
            threads.append(threading.Thread(target=self.draw, args=(box,)))
            threads[i].setDaemon(True)
            threads[i].start()
            i += 1
        left_iris = Eye(cam, 'left', face_mesh)
        right_iris = Eye(cam, 'right', face_mesh)
        time.sleep(3)
        # left_center_x, left_center_y, right_center_x, right_center_y, avg_width, avg_hight, ratio_width, ratio_hight = self.calibration(cam, face_mesh)
        left_center_x, left_center_y, left_ratio_width, left_ratio_hight, left_width, left_hight = left_iris.calibrate()
        right_center_x, right_center_y, right_ratio_width, right_ratio_high, right_width, right_hight = right_iris.calibrate()
        time.sleep(1)
        for directions in self._directions_order:
            for position in directions:
                # Ensure all boxes are visible.
                for box in self._boxes.values():
                    box.reset_color()

                self._boxes[position].toggle_color()

                # Set the initial time
                start_time = time.time()
                # Main loop
                print('=====')
                print(position)
                while not self._done:
                    # Todo: Add Gaze calibration
                    # left,right,_,_,_,_ = self.gaze(cam, face_mesh)
                    left, _, _ = left_iris.process()
                    right, _, _ = right_iris.process()
                    avg_width = (left_width + right_width) / 2
                    avg_hight = (left_hight + right_hight) / 2
                    # print(left_p_x-left_center_x + right_p_x-right_center_x)
                    left_x = left[0] - left_center_x
                    left_y = left[1] - left_center_y
                    right_x = right[0] - right_center_x
                    right_y = right[1] - right_center_y
                    if left_x < 0:
                        left_x += left_ratio_width * left_x
                    if left_y < 0:
                        left_y += left_ratio_hight * left_y
                    if right_x < 0:
                        right_x += right_ratio_width * right_x
                    if right_y < 0:
                        right_y += right_ratio_high * right_y
                    x = (left_x + right_x) / 2
                    y = (left_y + right_y) / 2
                    # x = left_x
                    # y = left_y
                    # avg_width = left_width
                    # avg_hight = left_hight

                    # print(left_ratio_width,left_ratio_hight)    
                    # x = (left[0]-left_center_x + right[0]-right_center_x)/2 #+ (left_p_x-left_center_x + right_p_x-right_center_x)/2 + avg_width/2
                    # y = (left[1]-left_center_y + right[1]-right_center_y)/2 #+ (left_p_y-left_center_y + right_p_y-right_center_y)/2 + avg_hight/2
                    # print(a,b,avg_width,avg_hight,ratio_width,ratio_hight)
                    # print(x,y)
                    # if x < 0:
                    #     x+= ratio_width*x
                    # if y < 0:
                    #     y+= ratio_hight*y
                    # print(x,y)                    
                    x, y = (int(x * self._screen_width / avg_width) + (self._screen_width / 2),
                            int(y * self._screen_height / avg_hight) + (self._screen_height / 2))
                    # print('=====')
                    self._screen.fill((0, 0, 0))
                    pygame.draw.circle(self._screen, (255, 0, 255), (x, y), 10)
                    pygame.display.update()
                    if self._boxes[position].is_inside(x, y):
                        print('inside')

                    # Toggle the box color after the preparation time.
                    if time.time() - start_time >= self._preparation_duration \
                            and self._boxes[position].get_color() == PURPLE:
                        self._boxes[position].toggle_color()

                    # Stop the stimulus GUI after the session duration.
                    if time.time() - start_time >= self._preparation_duration + self._stimulation_duration + self._rest_duration:
                        break

                    if self._preparation_duration + self._stimulation_duration + self._rest_duration > time.time() - start_time >= self._preparation_duration + self._stimulation_duration:
                        # Hide all boxes.
                        for box in self._boxes.values():
                            box.hide_box()

                    for event in pygame.event.get():
                        if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                            if event.key == pygame.K_ESCAPE:
                                self.close_stimulation()
                        if event.type == pygame.QUIT:
                            self.close_stimulation()

                    pygame.time.delay(100)
        pygame.quit()

    def close_stimulation(self):
        self._done = True

    def _display_info(self):
        for box in self._boxes.values():
            font = pygame.font.SysFont('Aerial', 30)
            text = font.render(f"{box.get_direction()} : {box.get_frequency()} HZ", False, BLUE)
            self._screen.blit(text, (box.get_left(), box.get_top()))

    def draw(self, box):
        COUNT = 1
        CLOCK = pygame.time.Clock()
        FrameRate = FRAMERATE

        b.wait()  # Synchronize the start of each thread

        curr_frequency = box.get_frequency()

        while True:  # execution block

            curr_color = box.get_color()

            CLOCK.tick(FrameRate)
            tmp = sin(2 * pi * curr_frequency * (COUNT / FrameRate))
            is_colored = (tmp > 0)

            if is_colored:
                final_color = curr_color
            else:
                final_color = BLACK

            block = pygame.draw.rect(self._screen, final_color, box.rect(), border_radius=BORDER_RADIUS)
            pygame.display.update(block)  # can't update in main thread which will introduce delay in different block
            COUNT += 1
            if COUNT == FrameRate:
                COUNT = 0
            # print(CLOCK.get_time())  # check the time between each frame (144HZ=7ms; 60HZ=16.67ms)

    def online(self, frequencies, is_full_screen=False):
        self._frequencies = frequencies
        self._is_full_screen = is_full_screen
        cam = cv2.VideoCapture(0)
        face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        # Create the screen
        self._screen = pygame.display.set_mode((0, 0),
                                               pygame.FULLSCREEN) if self._is_full_screen else pygame.display.set_mode(
            [self._screen_width, self._screen_height])
        self._create_boxes()
        pygame.init()
        # write the text on the screen
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render('+', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self._screen_width // 2, self._screen_height // 2)
        self._screen.blit(text, textRect)
        pygame.display.update()

        threads = []
        i = 0

        for box in self._boxes.values():
            threads.append(threading.Thread(target=self.draw, args=(box,)))
            threads[i].setDaemon(True)
            threads[i].start()
            i += 1
        left_iris = Eye('left')
        right_iris = Eye('right')
        time.sleep(2)
        # left_center_x, left_center_y, right_center_x, right_center_y, avg_width, avg_hight, ratio_width, ratio_hight = self.calibration(cam, face_mesh)
        left_center_x, left_center_y, left_ratio_width, left_ratio_hight, left_width, left_hight = left_iris.calibrate(
            cam)
        right_center_x, right_center_y, right_ratio_width, right_ratio_high, right_width, right_hight = right_iris.calibrate(
            cam)
        print((left_width + right_width) / (left_hight + right_hight))
        # time.sleep(1)
        while not self._done:
            # Todo: Add Gaze calibration
            # left,right,_,_,_,_ = self.gaze(cam, face_mesh)
            _, frame = cam.read()
            left_iris.update(frame)
            right_iris.update(frame)
            left, _, _ = left_iris.process()
            right, _, _ = right_iris.process()
            avg_width = (left_width + right_width) / 2
            avg_hight = (left_hight + right_hight) / 2
            # print(left_p_x-left_center_x + right_p_x-right_center_x)
            left_x = left[0] - left_center_x
            left_y = left[1] - left_center_y
            right_x = right[0] - right_center_x
            right_y = right[1] - right_center_y
            # if left_x > 0:
            #     left_x*= left_ratio_width
            # if left_y < 0:
            #     left_y*= left_ratio_hight
            # if right_x < 0:
            #     right_x*= right_ratio_width
            # if right_y < 0:
            #     right_y*= right_ratio_high
            x = (left_x + right_x) / 2
            y = (left_y + right_y) / 2
            # print(x,y,(avg_width/avg_hight))
            x, y = (int((avg_width / avg_hight) * x * self._screen_width / avg_width) + (self._screen_width / 2),
                    int(y * self._screen_height / avg_hight) + (self._screen_height / 2))
            # print('=====')
            direct = box.get_pointed_direction(x, y)
            if direct is not None:
                print(direct)
            self._screen.fill((0, 0, 0))
            pygame.draw.circle(self._screen, (255, 0, 255), (x, y), 10)
            pygame.display.update()
            # if self._boxes[position].is_inside(x, y):
            #     print('inside')

            for event in pygame.event.get():
                if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_ESCAPE:
                        self.close_stimulation()
                if event.type == pygame.QUIT:
                    self.close_stimulation()

            pygame.time.delay(100)
        pygame.quit()

    def online_test(self, frequencies, is_full_screen, direction):
        self._frequencies = frequencies
        self._is_full_screen = is_full_screen
        cam = cv2.VideoCapture(0)
        # st_time = time()
        # cam = cv2.VideoCapture(1,cv2.CAP_DSHOW,(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY))
        # # ed_time = time()
        # cam.set(cv2.CAP_PROP_FPS, 30.0)
        # cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        # cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # print(f"elapsed time: {ed_time - st_time}")

        # Create the screen
        self._screen = pygame.display.set_mode((0, 0),
                                               pygame.FULLSCREEN) if self._is_full_screen else pygame.display.set_mode(
            [self._screen_width, self._screen_height])
        self._create_boxes()
        pygame.init()
        # write the text on the screen
        self._display_center()

        threads = []
        i = 0

        movement = Movement(self._screen, cam)
        movement.calibrate()
        # movement.save('k.sav')
        # movement.load('k.sav')
        for box in self._boxes.values():
            threads.append(threading.Thread(target=self.draw, args=(box,)))
            threads[i].setDaemon(True)
            threads[i].start()
            i += 1
        orders_count = 0
        old_order = ''
        while not self._done:
            point = movement.get_position()

            # if point is not None:
            #     self._screen.fill((0, 0, 0))
            #     pygame.draw.circle(self._screen, (255, 0, 255), (point[0], point[1]), 10)
            #     pygame.display.update()

            if point is not None:
                direct = box.get_pointed_direction(point[0], point[1])
                if direct is not None:
                    if direct == old_order:
                        orders_count += 1
                    else:
                        order_count = 0
                    if order_count % 15 == 0:
                        print(direct)
                        if direct == 'top':
                            direction.value = 'F'
                            # TODO: send direction from here
                        elif direct == 'right':
                            direction.value = 'R'
                            # TODO: send direction from here
                        elif direct == 'down':
                            direction.value = 'B'
                            # TODO: send direction from here
                        elif direct == 'left':
                            direction.value = 'L'
                            # TODO: send direction from here
                        else:
                            direction.value = 'S'

                    old_order = direct

            for event in pygame.event.get():
                if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_ESCAPE:
                        self.close_stimulation()
                if event.type == pygame.QUIT:
                    self.close_stimulation()

            pygame.time.delay(100)
        pygame.quit()

    def _display_center(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render('+', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)
        self._screen.blit(text, textRect)
        pygame.display.update()

    def calibration(self, cam, face_mesh):
        right_p = 384
        left_p = 161
        left_center_x = 0
        left_center_y = 0
        right_center_x = 0
        right_center_y = 0
        left_p_x = 0
        left_p_y = 0
        right_p_x = 0
        right_p_y = 0
        left_width = 0
        left_hight = 0
        right_width = 0
        right_hight = 0
        n = 50
        for _ in range(n):
            frame, landmarks = self._frame_process(cam, face_mesh)
            left_p_x += self.get_point(landmarks, left_p)[0]
            left_p_y += self.get_point(landmarks, left_p)[1]
            right_p_x += self.get_point(landmarks, right_p)[0]
            right_p_y += self.get_point(landmarks, right_p)[1]
            left, right, right_eye_width, left_eye_width, right_eye_hight, left_eye_hight = self.gaze(cam, face_mesh)
            left_center_x += left[0]
            left_center_y += left[1]
            right_center_x += right[0]
            right_center_y += right[1]
            left_width += left_eye_width
            left_hight += left_eye_hight
            right_width += right_eye_width
            right_hight += right_eye_hight
        left_center_x /= n
        left_center_y /= n
        right_center_x /= n
        right_center_y /= n
        left_p_x /= n
        left_p_y /= n
        right_p_x /= n
        right_p_y /= n
        left_width /= n
        left_hight /= n
        right_width /= n
        right_hight /= n
        print(left_width, right_width, left_hight, right_hight)
        avg_width = (left_width + right_width) / 2
        avg_hight = (left_hight + right_hight) / 2
        a = (abs(left_p_x - left_center_x) + abs(right_p_x - right_center_x)) / 2
        b = (abs(left_p_y - left_center_y) + abs(right_p_y - right_center_y)) / 2
        ratio_width = (avg_width - a) / a
        ratio_hight = (avg_hight - b) / b

        return left_center_x, left_center_y, right_center_x, right_center_y, avg_width, avg_hight, ratio_width, ratio_hight

    def _frame_process(self, cam, face_mesh):
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        if landmark_points:
            landmarks = landmark_points[0].landmark
        return frame, landmarks

    def gaze(self, cam, face_mesh):
        frame, landmarks = self._frame_process(cam, face_mesh)
        frame_h, frame_w, _ = frame.shape
        left_ires = self.get_point(landmarks, 468)
        right_ires = self.get_point(landmarks, 473)
        left_ires_x = int(left_ires[0] * frame_w)
        left_ires_y = int(left_ires[1] * frame_h)
        right_ires_x = int(right_ires[0] * frame_w)
        right_ires_y = int(right_ires[1] * frame_h)
        # print(right_ires)
        cv2.circle(frame, (left_ires_x, left_ires_y), 3, (0, 0, 255))
        cv2.circle(frame, (right_ires_x, right_ires_y), 3, (0, 0, 255))
        # left_eye = [33,133,159,145]
        # right_eye = [263,362,386,374]
        left_eye_width, right_eye_width = self.get_eye_width(landmarks)
        left_eye_height, right_eye_height = self.get_eye_height(landmarks)
        # avg_eye_width = min(left_eye_width , right_eye_width)
        # avg_eye_height = min(left_eye_height , right_eye_height)  
        # print(avg_eye_width/avg_eye_height)         
        # print(distance_left,distance_right)
        # cv2.imshow('Eye Controlled Mouse', frame)
        # esc to quit
        cv2.waitKey(1)
        return left_ires, right_ires, left_eye_width, right_eye_width, left_eye_height, right_eye_height
        # return left_ires,right_ires,avg_eye_width,avg_eye_height

    def get_eye_width(self, landmarks):
        # left_eye = [33,133]
        left_eye = [163, 154]
        # right_eye = [263,362]
        right_eye = [381, 390]
        left_eye_width = abs(self.get_point(landmarks, left_eye[0])[0] - self.get_point(landmarks, left_eye[1])[0])
        right_eye_width = abs(self.get_point(landmarks, right_eye[0])[0] - self.get_point(landmarks, right_eye[1])[0])
        return left_eye_width, right_eye_width

    def get_eye_height(self, landmarks):
        # left_eye = [159,145]
        left_eye = [161, 163]
        # right_eye = [386,374]
        right_eye = [390, 388]
        left_eye_height = abs(self.get_point(landmarks, left_eye[0])[1] - self.get_point(landmarks, left_eye[1])[1])
        right_eye_height = abs(self.get_point(landmarks, right_eye[0])[1] - self.get_point(landmarks, right_eye[1])[1])
        return left_eye_height, right_eye_height

    def get_point(self, landmarks, point):
        return landmarks[point].x, landmarks[point].y

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    BlankboardStimulus().run(FREQUENCIES_DICT, 2, 4, 2, False, [POSITIONS])

    # BlankboardStimulus().stim(FREQUENCIES_DICT)
