import os

import matplotlib.pyplot as plt


def computeHistogram(processedImages, path):
    fop = path + "/Histograms"
    os.mkdir(fop)
    for name in processedImages:
        image_data_collection = processedImages[name]

        for key in image_data_collection:
            temp = os.path.splitext(key)[0]
            histopath = os.path.join(fop, temp)
            histogramTitle = os.path.splitext(key)[0] + '_Histogram_Output'
            image_data = image_data_collection[key]
            plt.hist(image_data.flatten(), 255, [0, 255])
            plt.title(histogramTitle)
            plt.xlabel('Pixel Values')
            plt.savefig(histopath, dpi=500)
            plt.close()
            print("histogram created for "+key)
