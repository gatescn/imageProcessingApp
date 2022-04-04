import numpy as np
import time


class MetamorphicFilters:

    def setkernal(self):
        self.kernal = [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]]

    def binarizeImage(self, img_data, threshvalue):
        white_p_v = 255
        black_p_v = 0
        whiteThresholdResult = np.where((img_data <= threshvalue), img_data, white_p_v)
        blackThresholdResult = np.where((whiteThresholdResult > threshvalue), whiteThresholdResult, black_p_v)

        return blackThresholdResult
