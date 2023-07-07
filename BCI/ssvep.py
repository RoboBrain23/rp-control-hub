import random

from config import FREQUENCIES_DICT, TOP_POSITION, RIGHT_POSITION, DOWN_POSITION, \
    LEFT_POSITION
from BlankboardStimulus import BlankboardStimulus

class SSVEP:
    def __init__(self, subject_name: str, preparation_duration: int, stimulation_duration: int, rest_duration: int,
                 frequencies: dict,
                 full_screen_mode: bool, order: list):
        self._subject_name = subject_name
        self._preparation_duration = preparation_duration
        self._stimulation_duration = stimulation_duration
        self._rest_duration = rest_duration
        self._full_stimulation_duration = self._preparation_duration + self._stimulation_duration

        self._frequencies = frequencies
        self._direction_order = order

        self._stimulus_screen_width = 1024
        self._stimulus_screen_height = 768
        self._full_screen_mode = full_screen_mode

        self._session_state = True
        self._stimulus = None

    def start_stimulation_gui(self, direction):
        """
        Start the stimulation GUI
        """
        self._stimulus = BlankboardStimulus()
        # self._stimulus.run(self._frequencies, self._preparation_duration, self._stimulation_duration,
        #                    self._rest_duration, self._full_screen_mode, self._direction_order)
        # self._stimulus.online(self._frequencies,self._full_screen_mode)
        self._stimulus.online_test(self._frequencies, self._full_screen_mode, direction)

    def start(self, direction):
        self.start_stimulation_gui(direction)

    def set_session_state(self, state: bool):
        self._session_state = state

    def get_session_state(self):
        return self._session_state


if __name__ == '__main__':
    subject_name = ""
    no_of_sessions = 1
    preparation_duration = 1
    stimulation_duration = 1
    rest_duration = 0
    full_screen = False

    base_directions = [TOP_POSITION, RIGHT_POSITION, DOWN_POSITION, LEFT_POSITION]
    final_order = []
    for i in range(no_of_sessions):
        random.shuffle(base_directions)
        final_order.append(list(base_directions))

    ssvep = SSVEP(subject_name, preparation_duration, stimulation_duration, rest_duration, FREQUENCIES_DICT,
                  full_screen, final_order)
    ssvep.start()
