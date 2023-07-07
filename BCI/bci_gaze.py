from bci_eye import Eye


class Gaze:
    def __init__(self, side):
        self._side = side
        self._left_iris = Eye('left')
        self._right_iris = Eye('right')

    def get_gaze(self):
        x = 0
        y = 0
        if self._side == 'left':
            x = self._left_iris.get_iris()[0]
            y = self._left_iris.get_iris()[1]
        elif self._side == 'right':
            x = self._right_iris.get_iris()[0]
            y = self._right_iris.get_iris()[1]
        elif self._side == 'both':
            x = (self._left_iris.get_iris()[0] + self._right_iris.get_iris()[0]) / 2
            y = (self._left_iris.get_iris()[1] + self._right_iris.get_iris()[1]) / 2
        return x, y

    def update(self, frame):
        self._left_iris.update(frame)
        self._right_iris.update(frame)

    def calibrate_center(self, cam):
        left_center_x, left_center_y, left_ratio_width, left_ratio_hight, left_width, left_hight = self._left_iris.calibrate(
            cam)
        right_center_x, right_center_y, right_ratio_width, right_ratio_high, right_width, right_hight = self._right_iris.calibrate(
            cam)
        if self._side == 'left':
            return left_center_x, left_center_y
        elif self._side == 'right':
            return right_center_x, right_center_y
        elif self._side == 'both':
            return (left_center_x + right_center_x) / 2, (left_center_y + right_center_y) / 2
