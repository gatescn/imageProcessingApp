import numpy as np
import time
from pluginfiles.plugin import NoiseFilterPluginInterface
from numpy.random import normal


class GaussianNoiseFilter(NoiseFilterPluginInterface):
    imgMatrix = None
    mean = None
    standardDeviation = None

    def setstrength(self, strength):
        self.mean = np.mean(self.imgMatrix) * .15
        if strength == 2:
            self.standardDeviation = self.mean * .40
            return strength
        else:
            self.standardDeviation = self.mean * .20
        return strength

    def performFilter(self, strength_, raw_img):
        operationStartTime = time.time()
        self.imgMatrix = np.array(raw_img)
        originalShape = self.imgMatrix.shape
        self.setstrength(self, strength_)
        count = self.imgMatrix.shape[0] * self.imgMatrix.shape[1]
        noise = np.random.normal(self.mean, self.standardDeviation, count)
        flatarray = self.imgMatrix.flatten()
        for i, values in enumerate(flatarray):
            flatarray[i] = flatarray[i] + noise[i]
        filteredimg = np.reshape(flatarray, originalShape)
        totalOperation = time.time() - operationStartTime
        return filteredimg, totalOperation
