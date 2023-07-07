import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


class Calibration:

    def __init__(self):
        self.reg = None

    def update(self, data):
        if self.reg is None:
            self.reg = LinearRegression()
        # pair-wise linear regression
        all_v = np.empty((0, 2))
        all_p = np.empty((0, 2))
        for point, vectors in data.items():
            v = np.array(vectors)
            mean = np.mean(v, axis=0)
            std = np.std(v, axis=0)
            filtered_v = [[v[0], v[1]] for v in vectors if v[0] > mean[0] - 2 * std[0] and v[1] > mean[1] - 2 * std[1]]
            filtered_v = [[v[0], v[1]] for v in filtered_v if
                          v[0] < mean[0] + 2 * std[0] and v[1] < mean[1] + 2 * std[1]]

            v = np.array(filtered_v)
            p = np.full(v.shape, [point])

            all_v = np.concatenate((all_v, v))
            all_p = np.concatenate((all_p, p))

        self.reg.fit(all_v, all_p)
        print("SCORE: {}".format(self.reg.score(all_v, all_p)))
        print("COEFF: {}".format(self.reg.coef_))

    def compute(self, vector):
        # pair-wise linear regression
        np_vector = np.array([vector])
        np_gaze = self.reg.predict(np_vector)
        output = (int(np_gaze[0][0]), int(np_gaze[0][1]))
        return output

    def save(self, filename):
        pickle.dump(self.reg, open(filename, 'wb'))

    def load(self, filename):
        self.reg = pickle.load(open(filename, 'rb'))
