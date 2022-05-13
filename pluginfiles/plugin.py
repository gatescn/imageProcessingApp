import numpy as np

registeredFilters = np.array(["GaussianNoiseFilter", "LinearFilter", "MedianFilter",
                              "SaltAndPepperFilter", "HistogramEqualization", "LaplacianEdgeDetectionFilter",
                              "DilationFilter", "ErosionFilter", "HistogramThresholdSegmentation", "KMeansClustering",
                              "FeatureGrabber","KNN"])


class Plugin:

    def run(self, filename, raw_img, definition_path):
        pass

    def is_image_save_required(self):
        return True

    def is_file_save_required(self):
        return False


class Classifier:
    def run(self, definition_path):
        pass
    def is_image_save_required(self):
        return False

    def is_file_save_required(self):
        return False