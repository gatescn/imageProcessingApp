import numpy as np

registeredFilters = np.array(["GaussianNoiseFilter", "LinearFilter", "MedianFilter", "SaltAndPepperFilter"])


class FilterPluginInterface:

    def performFilter(self,masksize, maskweight, raw_img):
        pass


class NoiseFilterPluginInterface:

    def performFilter(self,strength_, raw_img):
        pass
