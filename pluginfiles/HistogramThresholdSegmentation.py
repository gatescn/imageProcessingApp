from pluginfiles.plugin import FilterPluginInterface
import pluginfiles.StatOperations as statOps
import numpy as np
import time
import sys


class HistogramThresholdSegmentation(FilterPluginInterface):
    img_data = None
    histogram_data = None
    objectPixels = None
    backgroundPixels = None
    total_pixel_count = None
    prob_of_obj = None
    prob_of_background = None

    def performFilter(self, raw_img):
        operation_start_time = time.time()
        self.img_data = np.array(raw_img)
        self.total_pixel_count = self.img_data.shape[0] * self.img_data.shape[1]
        bin_size = 255
        flat_data = self.img_data.copy().flatten()
        self.histogram_data = statOps.calculateHistogram(flat_data, bin_size)
        best_threshold = self.find_best_threshold(self)
        totalOperation = time.time() - operation_start_time
        return self.img_data, totalOperation

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
