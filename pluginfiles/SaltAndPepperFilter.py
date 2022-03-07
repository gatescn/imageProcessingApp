import random
from plugin import FilterPluginInterface


class SaltAndPepperFilter(FilterPluginInterface):
    trashcan = []

    def setstrength(self):
        if self.strength == 2:
            self.strength = (1, 0, 1)
            return
        else:
            self.strength = (0, 0, 1)
        return

    def __init__(self, strength, matrix):
        self.strength = strength
        self.imgMatrix = matrix
        self.setstrength()

    def performfilter(self):
        for r, rows in enumerate(self.imgMatrix):
            for c, col in enumerate(rows):
                pixelvalue = self.computevalue(col)
                self.imgMatrix[r][c] = pixelvalue

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
