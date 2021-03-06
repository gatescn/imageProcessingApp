from pluginfiles import HelperLibrary
from pluginfiles.plugin import Plugin
import numpy as np
import math
import time
from PIL import Image, ImageFile


class LaplacianEdgeDetectionFilter(Plugin):
    kernal = None
    filteredImage = None
    masksize = None
    weight = None
    img_data = None

    def setkernal(self):
        self.kernal = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

    def applykernalweight(self):
        for r, row in enumerate(self.kernal):
            for c, col in enumerate(row):
                self.kernal[r][c] = self.weight * col

    def negateImage(self):
        for i in range(self.filteredImage.shape[0]):
            for j in range(self.filteredImage.shape[1]):
                if self.filteredImage[i][j] == 255:
                    self.filteredImage[i][j] = 0
                else:
                    self.filteredImage[i][j] = 255

    def filterComputation(self, window_slice):
        w = window_slice.shape
        tempArray = []
        for i in range(w[0]):
            for j in range(w[1]):
                window_pixel = window_slice[i, j]
                kernal_value = self.kernal[i][j]
                temp = window_pixel * kernal_value
                tempArray.append(temp)
        result = np.sum(tempArray)
        return result

    def run(self, filename, raw_img, definition_path):
        operationStartTime = time.time()
        params = HelperLibrary.readDefinitionFile(definition_path)
        self.masksize = int(params["maskSize"])
        self.weight = float(params["filterWeight"])
        self.img_data = np.array(raw_img)
        self.filteredImage = np.empty_like(self.img_data)
        self.setkernal(self)
        self.applykernalweight(self)
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
        self.negateImage(self)
        return self.filteredImage
