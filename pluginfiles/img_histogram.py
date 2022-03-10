import math

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFile

class img_histogram:

    def __init__(self):
        self.histogramData_2 = None
        print("init")

    def performEqualization(self,image):
        imagedata = self.createHistogram(image)
        arraySum = np.sum(imagedata)
        arraySize = imagedata.shape[0]

        cdfSum = 0;
        results = []
        for i in range(arraySize):#pdf
            x = float(imagedata[i])
            temp = x/ arraySum
            p = temp
            results.append(p)
        for j in range(len(results)-1):#cdf
            val = results[j]
            cdfSum = cdfSum + val
            results[j] = val





    def createHistogram(self,image):
        image_data = np.array(image)
        histogramData = np.zeros(255, dtype=int)
        img_height = image_data.shape[0]
        img_width = image_data.shape[1]

        for i in range(0, img_height):
            for j in range(0,img_width):
                v = image_data[i,j]
                histogramData[v] = histogramData[v]+1
        self.histogramData_2 = np.bincount(image_data.flatten(),minlength=256)
        return histogramData







