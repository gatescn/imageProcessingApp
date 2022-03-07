import numpy as np
import matplotlib.pyplot as plt

class img_histogram:
    equalizedImgData = None
    histogramData = np.zeros(255,dtype=int)
    equalizeRequested : bool = False

    def __init__(self, raw_img, performEqualization):
        self.image_data = np.array(raw_img)
        self.equalizeRequested = performEqualization


    def cretateHistogram(self):
        img_height = self.image_data.shape[0]
        img_width = self.image_data.shape[1]

        for i in range(0, img_height):
            for j in range(0,img_width):
                v = self.image_data[i,j]
                self.histogramData[v] = self.histogramData[v]+1
        plt.plot(self.histogramData)
        plt.show()

