from pluginfiles import HelperLibrary
from pluginfiles.plugin import Plugin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')
import time


class KMeansClustering(Plugin):
    max_iter = 0
    tol = 0.001
    k = 0
    data = None
    centroids = None
    classifications = None

    def run(self, raw_img, filename, definition_path):
        params = HelperLibrary.readDefinitionFile(definition_path)
        self.k = int(params["k"])
        self.max_iter = int(params["max_iters"])
        self.data = np.array(raw_img)

        X = np.array([[1, 2],
                      [1.5, 1.8],
                      [5, 8],
                      [8, 8],
                      [1, 0.6],
                      [9, 11],
                      [1, 3],
                      [8, 9],
                      [0, 3],
                      [5, 4],
                      [6, 4], ])
        colors = 10 * ["g", "r", "c", "b", "k"]

        self.fit(self, self.data)

        for centroid in self.centroids:
            plt.scatter(self.centroids[centroid][0], self.centroids[centroid][1],
                        marker="o", color="k", s=150, linewidths=5)

        for classification in self.classifications:
            color = colors[classification]
            for featureset in self.classifications[classification]:
                plt.scatter(featureset[0], featureset[1], marker="x", color=color, s=150, linewidths=5)

        plt.show()

    def fit(self, data):
        self.centroids = {}

        for i in range(self.k):
            self.centroids[i] = data[i]

        for i in range(self.max_iter):
            self.classifications = {}

            for j in range(self.k):
                self.classifications[j] = []

            for featureset in data:
                distances = [np.linalg.norm(featureset - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classifications[classification].append(featureset)

            prev_centroids = dict(self.centroids)

            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)

            optimized = True

            for c in self.centroids:
                original_centroid = prev_centroids[c]
                current_centroid = self.centroids[c]
                if np.sum((current_centroid - original_centroid) / original_centroid * 100.0) > self.tol:
                    optimized = False
            if optimized:
                break

    def predict(self, data):
        distances = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification
