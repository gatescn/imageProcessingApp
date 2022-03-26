from pluginfiles.plugin import MaskFilterPluginInterface
import numpy as np
import math
import time
from PIL import Image, ImageFile


class DilationFilter(MaskFilterPluginInterface):
    kernal = None
    filteredImage = None
    masksize = None
    weight = None
    img_data = None

    def setkernal(self):
        self.kernal = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

    def binarizeImage(self, img_data, threshvalue):
        white_p_v = 255
        black_p_v = 0
        whiteThresholdResult = np.where((img_data <= threshvalue), img_data, white_p_v)
        blackThresholdResult = np.where((whiteThresholdResult > threshvalue), whiteThresholdResult, black_p_v)

        return blackThresholdResult

    def applykernalweight(self):
        for r, row in enumerate(self.kernal):
            for c, col in enumerate(row):
                self.kernal[r][c] = self.weight * col

    def filterComputation(self, window_slice):
        if 255 in window_slice:
            result = 255
        else:
            result = 0
        return result

    def performFilter(self, masksize, maskweight, raw_img):
        operationStartTime = time.time()
        threshold_value = int(255/2)
        self.masksize = masksize
        self.weight = maskweight
        raw_img_data = np.array(raw_img)
        self.setkernal(self)
        self.applykernalweight(self)
        self.img_data = self.binarizeImage(self, raw_img_data, threshold_value)
        self.filteredImage = self.img_data.copy()
        S = self.img_data.shape
        kernal_height = len(self.kernal)
        kernal_width = len(self.kernal[0])

        R = S[0] + kernal_height - 1
        C = S[1] + kernal_width - 1
        Z = np.zeros((R, C))
        t1 = np.int((kernal_height - 1) / 2)
        t2 = np.int((kernal_width - 1) / 2)
        for i in range(S[0]):
            for j in range(S[1]):
                Z[i + t1, j + t2] = self.img_data[i, j]
        for i in range(S[0]):
            for j in range(S[1]):
                window_slice = np.array(Z[i:i + kernal_height, j:j + kernal_width])
                result = self.filterComputation(self, window_slice)
                self.filteredImage[i, j] = result
        totalOperation = time.time() - operationStartTime
        return self.filteredImage,totalOperation
