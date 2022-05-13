import numpy as np
import time

from pluginfiles import HelperLibrary
from pluginfiles.plugin import Plugin


class ErosionFilter(Plugin):
    kernal_height = None
    kernal_width = None
    kernal = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]

    def binarize_image(self, img_data):
        threshold_value = int(255 / 2)
        white_p_v = 255
        black_p_v = 0
        white_threshold_result = np.where((img_data <= threshold_value), img_data, white_p_v)
        black_threshold_result = np.where((white_threshold_result > threshold_value), white_threshold_result, black_p_v)

        return black_threshold_result

    def initialize(self, raw_img):
        raw_img_data = np.array(raw_img)
        binary_img_data = self.binarize_image(self, raw_img_data)
        self.kernal_height = len(self.kernal)
        self.kernal_width = len(self.kernal[0])
        return binary_img_data

    def filterComputation(self, window_slice):
        for r, row in enumerate(self.kernal):
            for c, col in enumerate(row):
                if self.kernal[r][c] != window_slice[r][c]:
                    return 255
        return 0

    def run(self, raw_img, filename, definition_path):
        operation_start = time.time()
        params = HelperLibrary.readDefinitionFile(definition_path)
        iterate_count = int(params["iteration"])
        current_result = self.initialize(self, raw_img)
        for i in range(iterate_count):
            img_data = self.performFilter(self, current_result)
            current_result = img_data
        total_op_time = time.time() - operation_start
        return current_result, total_op_time

    def performFilter(self, img):
        filtered_image = img.copy()
        zero_padded_image = self.createZeroPaddedImage(self, img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                window_slice = np.array(zero_padded_image[i:i + self.kernal_height, j:j + self.kernal_width])
                result = self.filterComputation(self, window_slice)
                filtered_image[i, j] = result
        return filtered_image

    def createZeroPaddedImage(self, img):
        r = img.shape[0] + self.kernal_height - 1
        c = img.shape[1] + self.kernal_width - 1
        z = np.zeros((r, c))
        row_offset = np.int((self.kernal_height - 1) / 2)
        col_offset = np.int((self.kernal_width - 1) / 2)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                z[i + row_offset, j + col_offset] = img[i, j]
        return z
