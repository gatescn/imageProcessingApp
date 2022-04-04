import os

import matplotlib.pyplot as plt
import numpy as np


def outputHistograms(processed_images, path):
    fop = path + "/Histograms"
    os.mkdir(fop)
    plt.ioff()
    for name in processed_images:
        image_data_collection = processed_images[name]

        for key in image_data_collection:
            temp = os.path.splitext(key)[0]
            histo_path = os.path.join(fop, temp)
            histogram_title = os.path.splitext(key)[0] + '_Histogram_Output'
            image_data = image_data_collection[key].flatten()
            plt.plot(calculateHistogram(image_data, 255))
            plt.title(histogram_title)
            plt.xlabel('Pixel Values')
            plt.savefig(histo_path, dpi=500)
            plt.close()
            print("histogram created for " + key)


def calculateHistogram(data, bins):
    histogram = np.zeros(bins + 1)

    for pixel in data:
        histogram[pixel] += 1

    return histogram







