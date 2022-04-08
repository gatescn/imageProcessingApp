from pluginfiles.plugin import MetamorphicFilterPluginInterface
import pluginfiles.StatOperations as statOps
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import os


class HistogramThresholdSegmentation(MetamorphicFilterPluginInterface):
    img_data = None
    histogram_data = None
    objectPixels = None
    backgroundPixels = None
    total_pixel_count = None
    prob_of_obj = None
    prob_of_background = None
    filteredImage = None

    def performFilter(self, raw_img):
        operation_start_time = time.time()
        self.img_data = np.array(raw_img)
        self.filteredImage = np.empty_like(self.img_data)
        self.total_pixel_count = self.img_data.shape[0] * self.img_data.shape[1]
        bin_size = 255
        flat_data = self.img_data.copy().flatten()
        self.histogram_data = statOps.calculateHistogram(flat_data, bin_size)
        best_threshold = self.find_best_threshold(self)
        filteredImage = self.seperateBasedOnThreshold(self, self.img_data, best_threshold)
        totalOperation = time.time() - operation_start_time
        return filteredImage, totalOperation

    def seperateBasedOnThreshold(self, image_data, threshold):
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                if image_data[i, j] <= threshold:
                    self.filteredImage[i, j] = 0
                else:
                    self.filteredImage[i,j] = 255
        return self.filteredImage

    def outputHistograms(self, histodata, line_val):
        histogram_title = os.path.splitext("temp")[0] + '_Histogram_Output'
        plt.plot(histodata)
        plt.title(histogram_title)
        plt.xlabel('Pixel Values')
        plt.axvline(line_val, color='k', linestyle='dashed', linewidth=1)

    def calculateHistogram(self, data, bins):
        histogram = np.zeros(bins + 1)

        for pixel in data:
            histogram[pixel] += 1

        return histogram

    def find_best_threshold(self):
        variance = sys.float_info.max
        best_threshold = None
        for i in range(0, self.histogram_data.shape[0] - 5):
            threshold = i + 2
            o_var_result = self.calculate_variance(self, 0, threshold)
            b_var_result = self.calculate_variance(self, threshold, self.histogram_data.shape[0])
            var_result = o_var_result + b_var_result
            if var_result <= variance:
                variance = var_result
                best_threshold = threshold
        return best_threshold

    def calculate_variance(self, start, end):
        sum_ = 0
        mean_sum = self.calculate_mean_sum(self, start, end)
        prob_sum = self.calculate_prob_sum(self, start, end)
        if prob_sum != 0:
            for i in range(start, end):
                var_1 = i - mean_sum
                var_2 = var_1 * var_1
                pixel_prob = self.calculate_prob_atPixel(self, i)
                var_3 = var_2 * pixel_prob
                var_4 = var_3 / prob_sum
                sum_ = sum_ + var_4
        return sum_

    def calculate_mean_sum(self, start, end):
        sum_ = 0
        prob_sum = self.calculate_prob_sum(self, start, end)
        if prob_sum != 0:
            for i in range(start, end):
                prob_of_pixel = self.calculate_prob_atPixel(self, i)
                var_1 = i * prob_of_pixel
                var_2 = var_1 / prob_sum
                sum_ = sum_ + var_2
        return sum_

    def calculate_prob_sum(self, start, end):
        sum_ = 0
        for i in range(start, end):
            prob_of_pixel = self.calculate_prob_atPixel(self, i)
            sum_ = sum_ + prob_of_pixel
        return sum_

    def calculate_prob_atPixel(self, i):
        pixel_occurance = self.histogram_data[i]
        prob_of_pixel = pixel_occurance / self.total_pixel_count
        return prob_of_pixel
