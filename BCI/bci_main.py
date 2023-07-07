import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT_DIR, 'config'))
sys.path.append(os.path.join(ROOT_DIR, 'stimulus'))

from config import *
from ssvep import SSVEP


def run_bci(direction):
    #       self._stimulus.run(self._frequencies, self._preparation_duration, self._stimulation_duration,
    #    self._rest_duration, self._full_screen_mode, self._direction_order)
    subject_name = "final"
    no_of_sessions = 10
    preparation_duration = 1
    stimulation_duration = 1
    rest_duration = 0
    full_screen = True

    base_directions = [TOP_POSITION, RIGHT_POSITION, DOWN_POSITION, LEFT_POSITION]
    final_order = []
    for i in range(no_of_sessions):
        # random.shuffle(base_directions)
        final_order.append(list(base_directions))

    ssvep = SSVEP(subject_name, preparation_duration, stimulation_duration, rest_duration, FREQUENCIES_DICT,
                  full_screen, final_order)
    ssvep.start(direction)

# if __name__ == '__main__':
#     run_bci()
