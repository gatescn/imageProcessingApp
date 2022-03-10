import numpy as np
from pluginfiles.plugin import NoiseFilterPluginInterface
from numpy.random import normal


class GaussianNoiseFilter(NoiseFilterPluginInterface):
    imgMatrix = None

    def setstrength(self, strength):
        if strength == 2:
            strength = .5
            return strength
        else:
            strength = 1
        return strength

    def performfilter(self, strength_, raw_img):
        filter_str = self.setstrength(self, strength_)
        self.imgMatrix = np.array(raw_img)
        mean = np.mean(self.imgMatrix)
