from plugin import FilterPluginInterface


class GaussianNoiseFilter(FilterPluginInterface):

    def __init__(self, noisevalue):
        self.noisevalue = noisevalue

    def performfilter(self):
        print("not implemented - Gaussian")
