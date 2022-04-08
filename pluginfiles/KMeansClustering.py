from pluginfiles.plugin import MetamorphicFilterPluginInterface
import numpy as np
import time
import random
from scipy.spatial import distance
import sys


class point:
    value = None
    coordinates = []

    def __init__(self, v, x, y):
        self.value = v
        self.coordinates.append(x)
        self.coordinates.append(y)


class KMeansClustering(MetamorphicFilterPluginInterface):
    img_data = None
    img_shape = None
    k = None
    tolerance = 0.001
    max_iterations = 300
    segmentedImage = None
    centroids = None
    classifications = None

    def performFilter(self, raw_img):
        operation_start_time = time.time()
        self.k = 2
        self.img_data = np.array(raw_img)
        self.img_shape = self.img_data.shape
        self.segmentedImage = np.empty_like(self.img_data)
        self.fit(self)
        totalOperation = time.time() - operation_start_time
        return self.img_data, totalOperation

    def fit(self):
        self.centroids = []
        for i in range(self.k):
            rand_indexes = random.sample(range(0, self.img_shape[0]), 2)
            self.centroids.append(point(self.img_data[rand_indexes[0],
                                                      rand_indexes[1]], rand_indexes[0], rand_indexes[1]))
        for i in range(self.max_iterations):
            for i in range(self.img_shape[0]):
                for j in range(self.img_shape[1]):
                    self.classifications = {}
                    p1 = point(self.img_data[i, j], i, j)



