from pluginfiles.plugin import FilterPluginInterface
import numpy as np
import math
import statistics


class MedianFilter(FilterPluginInterface):
    kernal = None
    filteredImage = None
    masksize = None
    weight = None
    img_data = None

    def setkernal(self):
        if self.masksize == 2:
            self.kernal = np.ones((5, 5), dtype=float)
        else:
            self.kernal = np.ones((3, 3), dtype=float)
        self.applykernalweight()

    def applykernalweight(self):
        for r, row in enumerate(self.kernal):
            for c, col in enumerate(row):
                self.kernal[r][c] = self.weight * col

    def updatekernalcenter(self, value):
        centerrowindex = math.floor(self.kernal.shape[0] / 2)
        centercolindex = math.floor(self.kernal.shape[1] / 2)
        self.kernal[centerrowindex][centercolindex] = value

    def filterComputation(self, window_slice):
        w = window_slice.shape
        tempArray = []
        for i in range(w[0]):
            for j in range(w[1]):
                window_pixel = window_slice[i, j]
                kernal_value = self.kernal[i, j]
                temp = window_pixel * kernal_value
                tempArray.append(temp)
        tempArray.sort()
        result = statistics.median(tempArray)
        return result

    def performFilter(self, masksize, maskweight, raw_img):
        self.masksize = masksize
        self.weight = maskweight
        self.img_data = np.array(raw_img)
        self.filteredImage = np.empty_like(self.img_data)
        self.setkernal()
        S = self.img_data.shape
        F = self.kernal.shape

        R = S[0] + F[0] - 1
        C = S[1] + F[1] - 1
        Z = np.zeros((R, C))
        t1 = np.int((F[0] - 1) / 2)
        t2 = np.int((F[1] - 1) / 2)
        for i in range(S[0]):
            for j in range(S[1]):
                Z[i + t1, j + t2] = self.img_data[i, j]
        for i in range(S[0]):
            for j in range(S[1]):
                window_slice = np.array(Z[i:i + F[0], j:j + F[1]])
                result = self.filterComputation(window_slice)
                self.filteredImage[i, j] = result
        return self.filteredImage
