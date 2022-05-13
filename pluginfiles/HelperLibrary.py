from pluginfiles.plugin import registeredFilters
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import importlib


def isRegisteredFilter(name):
    for rf in registeredFilters:
        if rf == name:
            return True
    return False


# reads config file
def read_config():
    file_name = "external.config"
    try:
        contents = open(file_name).read()
    except OSError:
        print("Could not find file:", file_name)
        sys.exit()
    filters_ = []
    config = eval(contents)
    rawimagedirectory = config['imageDirectory']
    processedimagedirectory = config['outputDirectory']
    for fp in config['operations']:
        if isRegisteredFilter(fp):
            filters_.append(fp)
    return rawimagedirectory, processedimagedirectory, filters_


def readDefinitionFile(path):
    try:
        def_cont = open(path).read()
    except OSError:
        print("Could not find definition file for:", path)
        sys.exit()
    result = eval(def_cont)
    return result


def checkForDefinitionFiles(appDirectory, operationDefDirectory, filters_):
    for filter_ in filters_:
        path_to_check = os.path.join(appDirectory + operationDefDirectory + filter_ + "Definition.config")
        if os.path.exists(path_to_check):
            return True
        else:
            return False


def createHistoryDirectory(current_output_directory, plugin_name):
    old_path = current_output_directory
    now = datetime.now()
    d = now.strftime("%m%d%Y%H_%M_%S")
    os.rename(old_path, current_output_directory + "/" + plugin_name + "_" + "History_" + d)


def get_plugin(filter_name):
    # get needed plugin file information...
    module_name = "pluginfiles." + filter_name
    module = importlib.import_module(module_name)
    plugin = getattr(module, filter_name)
    return plugin


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
