import random
import numpy as np
import time
from pluginfiles.plugin import NoiseFilterPluginInterface


class SaltAndPepperFilter(NoiseFilterPluginInterface):
    strength = None
    imgMatrix = None

    def setstrength(self):
        if self.strength == 2:
            self.strength = (0,1,2,2,2)
            return
        else:
            self.strength = (0, 1, 2,2,2,2,2,2)
        return

    def performFilter(self, strength, raw_img):
        operationStartTime = time.time()
        self.strength = strength
        self.imgMatrix = np.array(raw_img)
        self.setstrength(self)
        for r, rows in enumerate(self.imgMatrix):
            for c, col in enumerate(rows):
                pixelvalue = self.computevalue(self,col)
                self.imgMatrix[r][c] = pixelvalue
        totalOperation = time.time() - operationStartTime
        return self.imgMatrix, totalOperation

    def computevalue(self, currentpixel):
        decider = random.randint(0, len(self.strength) - 1)
        choice = self.strength[decider]
        if choice == 0:
            # salt
            currentpixel = 255
        if choice == 1:
            # pepper
            currentpixel = 0
        return currentpixel
