from bci_gaze import Gaze
from bci_calibration import Calibration
import pygame
import collections
from spinning import SpinningCircle
import random
import time
from config import *
from math import sin, pi


class Movement:
    def __init__(self, screen, camera, side='both'):
        if side == 'left':
            self._gaze = Gaze('left')
        elif side == 'right':
            self._gaze = Gaze('right')
        elif side == 'both':
            self._gaze = Gaze('both')
        self._screen = screen
        self._camera = camera
        self._calibration = Calibration()
        self._is_calibrated = False
        self._center = None
        self.calibrate_center()

    def calibrate(self, N_REQ_VECTORS=50, N_SKIP_VECTORS=25, TIMES=1):
        vectors = collections.defaultdict(list)

        completed = False
        COUNT = 1
        CLOCK = pygame.time.Clock()
        FrameRate = FRAMERATE
        freq = 10

        while TIMES > 0 and not completed:
            self._screen.fill(BLACK)
            pygame.display.update()
            # calibration_points = self.calculate_random_points(20)
            calibration_points = self.calculate_points()
            enough = 0
            skip = 0

            point = calibration_points.pop(0)

            pygame.draw.circle(self._screen, RED, point, CALIBRATION_CIRCLE_RADIUS)
            done = False
            spinning = SpinningCircle(CALIBRATION_CIRCLE_RADIUS + 5, GREEN, 360 / N_REQ_VECTORS)
            _, frame = self._camera.read()
            while point and not done:
                CLOCK.tick(FrameRate)
                tmp = sin(2 * pi * freq * (COUNT / FrameRate))
                is_colored = (tmp > 0)

                if is_colored:
                    final_color = RED
                else:
                    final_color = BLACK

                pygame.draw.circle(self._screen, final_color, point, CALIBRATION_CIRCLE_RADIUS)
                pygame.display.update()
                COUNT += 1
                if COUNT == FrameRate:
                    COUNT = 0

                _, frame = self._camera.read()
                self._gaze.update(frame)
                # get gaze vector x,y
                vector = (self._gaze.get_gaze()[0] - self._center[0], self._gaze.get_gaze()[1] - self._center[1])
                print("VECTOR: {}\tPOINT: {}".format(vector, point))

                if vector and skip < N_SKIP_VECTORS:
                    skip += 1
                    continue

                if vector:
                    vectors[point].append(vector)
                    enough += 1

                # draw progress bar on screen using pygame
                self._screen.blit(spinning,
                                  (point[0] - CALIBRATION_CIRCLE_RADIUS - 5, point[1] - CALIBRATION_CIRCLE_RADIUS - 5))
                spinning.update()
                pygame.display.update()
                # netx point condition
                if enough >= N_REQ_VECTORS and len(calibration_points) > 0:
                    point = calibration_points.pop(0)
                    skip = 0
                    enough = 0
                    self._screen.fill(BLACK)
                    pygame.draw.circle(self._screen, RED, point, CALIBRATION_CIRCLE_RADIUS)
                    spinning = SpinningCircle(CALIBRATION_CIRCLE_RADIUS + 5, GREEN, 360 / N_REQ_VECTORS)
                    pygame.display.update()
                    time.sleep(1)

                # end calibration condition
                if enough >= N_REQ_VECTORS and len(calibration_points) == 0:
                    self._screen.fill(BLACK)
                    pygame.display.update()
                    # completed = True
                    done = True
                    TIMES -= 1
                    break
                for event in pygame.event.get():
                    if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                        if event.key == pygame.K_ESCAPE:
                            done = True
                            completed = True
                            break
                    if event.type == pygame.QUIT:
                        done = True
                        completed = True
                        break
            if TIMES == 0 and enough >= N_REQ_VECTORS and len(calibration_points) == 0:
                # print("Calibration completed")
                completed = True

        if completed:
            print(sum([len(v) for v in vectors.values()]))
            self._calibration.update(vectors)
            self._is_calibrated = True

    def calculate_points(self):
        points = []

        # center
        p = (int(0.5 * self._screen.get_width()), int(0.5 * self._screen.get_height()))
        points.append(p)

        # top left
        p = (int(0.05 * self._screen.get_width()), int(0.05 * self._screen.get_height()))
        points.append(p)

        # top
        p = (int(0.5 * self._screen.get_width()), int(0.05 * self._screen.get_height()))
        points.append(p)

        # top right
        p = (int(0.95 * self._screen.get_width()), int(0.05 * self._screen.get_height()))
        points.append(p)

        # left
        p = (int(0.05 * self._screen.get_width()), int(0.5 * self._screen.get_height()))
        points.append(p)

        # right
        p = (int(0.95 * self._screen.get_width()), int(0.5 * self._screen.get_height()))
        points.append(p)

        # bottom left
        p = (int(0.05 * self._screen.get_width()), int(0.95 * self._screen.get_height()))
        points.append(p)

        # bottom
        p = (int(0.5 * self._screen.get_width()), int(0.95 * self._screen.get_height()))
        points.append(p)

        # bottom right
        p = (int(0.95 * self._screen.get_width()), int(0.95 * self._screen.get_height()))
        points.append(p)

        return points

    def calculate_random_points(self, n_points=10):
        points = []
        for i in range(n_points):
            x = random.randint(20, self._screen.get_width() - 20)
            y = random.randint(20, self._screen.get_height() - 20)
            points.append((x, y))
        return points

    def get_position(self):
        if self._is_calibrated:
            _, frame = self._camera.read()
            self._gaze.update(frame)
            return self._calibration.compute(
                (self._gaze.get_gaze()[0] - self._center[0], self._gaze.get_gaze()[1] - self._center[1]))

    def save(self, filename):
        self._calibration.save(filename)

    def load(self, filename):
        self._calibration.load(filename)
        self._is_calibrated = True

    def calibrate_center(self):
        self._center = self._gaze.calibrate_center(self._camera)
