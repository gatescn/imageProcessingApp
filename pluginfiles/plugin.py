import numpy as np

registeredFilters = np.array(["GaussianNoiseFilter", "LinearFilter", "MedianFilter",
                              "SaltAndPepperFilter", "HistogramEqualization", "LaplacianEdgeDetectionFilter",
                              "DilationFilter", "ErosionFilter", "HistogramThresholdSegmentation", "KMeansClustering"])


class FilterPluginInterface:

    def performFilter(self, raw_img):
        pass


class MetamorphicFilterPluginInterface:

    def iterateFilter(self, raw_img, iterate_count):
        pass


class MaskFilterPluginInterface:

    def performFilter(self, masksize, maskweight, raw_img):
        pass


class NoiseFilterPluginInterface:

    def performFilter(self, strength_, raw_img):
        pass
