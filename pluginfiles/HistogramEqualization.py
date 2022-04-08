from pluginfiles.plugin import MetamorphicFilterPluginInterface
import pluginfiles.StatOperations as statOps
import numpy as np
import time


def cumsum(a):
    a = iter(a)
    b = [next(a)]
    for i in a:
        b.append(b[-1] + i)
    return np.array(b)


class HistogramEqualization(MetamorphicFilterPluginInterface):
    img_data = None

    def performFilter(self, raw_img):
        operation_start_time = time.time()
        self.img_data = np.array(raw_img)
        bin_size = 255
        flat_data = self.img_data.copy().flatten()
        histogram_data = statOps.calculateHistogram(flat_data, bin_size)
        cs = cumsum(histogram_data)

        # get numerator / denominator of function
        nj = (cs - cs.min()) * bin_size
        N = cs.max() - cs.min()

        # re-normalize the cumsum
        cs = nj/N

        cs = cs.astype('uint8')

        # get the value from cum sum for every index in flat data and set as img_new
        img_new = cs[flat_data]
        img_new = np.reshape(img_new, self.img_data.shape)

        operation_total_time = time.time() - operation_start_time

        return img_new, operation_total_time
