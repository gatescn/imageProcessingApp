import random
from plugin import FilterPluginInterface


class SaltAndPepperFilter(FilterPluginInterface):
    trashcan = []

    def setstrength(self):
        if self.strength == 1:
            self.strength = (-1, 0, 0, 1)
            return
        if self.strength == 2:
            self.strength = (-1, -1, 0, 1, 1)
            return
        self.strength = (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
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
        if choice == -1:
            # salt
            currentpixel = 0
        if choice == 1:
            # pepper
            currentpixel = 255
        return currentpixel
