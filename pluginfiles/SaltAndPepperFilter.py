import random
import numpy as np
import time

from pluginfiles import HelperLibrary
from pluginfiles.plugin import Plugin


class SaltAndPepperFilter(Plugin):
    strength = None
    imgMatrix = None

    def setstrength(self):
        if self.strength == 2:
            self.strength = (0,1,2,2,2)
            return
        else:
            self.strength = (0, 1, 2,2,2,2,2,2)
        return

    def run(self, raw_img, filename, definition_path):
        operationStartTime = time.time()
        params = HelperLibrary.readDefinitionFile(definition_path)
        self.strength = int(params["strength"])
        self.imgMatrix = np.array(raw_img)
        self.setstrength(self)
        for r, rows in enumerate(self.imgMatrix):
            for c, col in enumerate(rows):
                pixelvalue = self.computevalue(self,col)
                self.imgMatrix[r][c] = pixelvalue
        totalOperation = time.time() - operationStartTime
        return self.imgMatrix

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
