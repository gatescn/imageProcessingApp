import numpy as np

from pluginfiles.plugin import FilterPluginInterface
from numpy.random import normal


class GaussianNoiseFilter(FilterPluginInterface):

    def setstrength(self):
        if self.strength == 2:
            self.strength = .5
            return
        else:
            self.strength = 1
        return

    def __init__(self, strength, matrix):
        self.std = None
        self.mean = None
        self.strength = strength
        self.setstrength()
        self.imgMatrix = matrix

    def performfilter(self):
        self.mean = np.mean(self.imgMatrix)
