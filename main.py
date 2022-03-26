# main script of image processing app
import importlib
import os
import sys
import time
import numpy as np

from datetime import datetime
from PIL import Image, ImageFile, UnidentifiedImageError
from pluginfiles.plugin import registeredFilters
from pluginfiles.plugin import MaskFilterPluginInterface, NoiseFilterPluginInterface, FilterPluginInterface
from pluginfiles import StatOperations

operationDefDirectory = "/operationDefinitionRepository/"
appDirectory = os.path.dirname(__file__)
filteredimagesmap = {}
operationtimemap = {}


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
    for fp in config['filtersToApply']:
        if isRegisteredFilter(fp):
            filters_.append(fp)
    return rawimagedirectory, processedimagedirectory, filters_


def isRegisteredFilter(name):
    for rf in registeredFilters:
        if rf == name:
            return True

    return False


def createHistoryDirectory(path, filter_):
    now = datetime.now()
    d = now.strftime("%m%d%Y%H_%M_%S")
    os.rename(path, outputdirectory + "/" + filter_ + "_" + "History_" + d)


def calculateTimeDelta(t1, t2):
    return t2 - t1


def saveAllImages(imageMap):
    if len(imageMap) > 0:
        for key in imageMap:
            filteroutputdirectory = outputdirectory + "/" + key
            if os.path.isdir(filteroutputdirectory):
                createHistoryDirectory(filteroutputdirectory, key)
            os.mkdir(filteroutputdirectory)
            processedImages = imageMap[key]
            for name in processedImages:
                im = Image.fromarray(processedImages[name])
                im.save(filteroutputdirectory + "/" + key + "_" + name, "bmp")
                print("image saved: " + name)
            StatOperations.outputHistograms(imageMap, filteroutputdirectory)
        return time.time()
    else:
        print("no images to save")


def checkForDefinitionFiles(filters_):
    for filter_ in filters_:
        path_to_check = os.path.join(appDirectory + operationDefDirectory + filter_ + "Definition.config")
        if os.path.isfile(path_to_check):
            return True
        else:
            return False


def readDefinitionFile(fullpath_):
    try:
        def_cont = open(fullpath_).read()
    except OSError:
        print("Could not find definition file for:", fullpath)
        sys.exit()
    result = eval(def_cont)
    return result


if __name__ == '__main__':

    batchProcessingStartTime = time.time()

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # get config params for program
    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)
    # check if each filter has a definition file associated, if not, stop the program because it will cause error later
    if not checkForDefinitionFiles(filters):
        print("please ensure definition file is present for each filter used and try again")
        sys.exit()
    # iterate through each filter parsed from configuration
    # f is the current filter
    for f in filters:
        print("Current Filter: " + f)
        # get needed plugin file information...
        moduleName = "pluginfiles." + f
        module = importlib.import_module(moduleName)
        plugin = getattr(module, f)
        # get the plugin's definition file. The definition file contains the params for the filter.
        fullpath = os.path.join(appDirectory + operationDefDirectory + f + "Definition.config")

        # read the definition params
        definitionParams = readDefinitionFile(fullpath)

        # creates map to hold all processed images by this individual filter.
        filteredImages = {}
        # creates array to hold time for filter operation
        operationTimeCapture = []

        fileIndex = 0

        fileTotal = len(files)

        # iterate through each file at the location specified in the configuration
        for file in files:

            # check if each file is an image type. Skip files that are non images
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                filename = f + "_" + str(file)
                filepath = rawdirectory + "/" + file

                # opens the raw image
                try:
                    raw_img = Image.open(filepath).convert('L')
                except UnidentifiedImageError:
                    print("Folder contains non image, please remove file named:" + file + " and rerun")
                    sys.exit()
                # copies the raw image
                image_copy = raw_img.copy()

                # checks if plugin is a non mask filter type
                if issubclass(plugin, FilterPluginInterface):
                    filteredImageData, operationTime = plugin.performFilter(plugin, raw_img)
                    operationTimeCapture.append(operationTime)

                # checks if plugin is a mask filter type
                if issubclass(plugin, MaskFilterPluginInterface):
                    maskSize = int(definitionParams['maskSize'])
                    maskWeight = float(definitionParams['filterWeight'])
                    filteredImageData, operationTime = plugin.performFilter(plugin, maskSize, maskWeight, raw_img)
                    operationTimeCapture.append(operationTime)

                # checks if plugin is a noise filter type
                if issubclass(plugin, NoiseFilterPluginInterface):
                    strength = int(definitionParams['strength'])
                    filteredImageData, operationTime = plugin.performFilter(plugin, strength, raw_img)
                    operationTimeCapture.append(operationTime)

                # adds the processed image to filterImagesMap, uses filename as key.
                filteredImages[filename] = filteredImageData

                # increment file index
                fileIndex = fileIndex + 1

                # prints the current filter being used along with the file being filtered
                print(str(fileIndex) + "of" + str(fileTotal))

        # calculates the avg time of the operation
        processingTimeAvg = np.mean(operationTimeCapture)

        # adds average op time to operation time map, the key is the name of the current filter.
        operationtimemap[f] = processingTimeAvg

        # adds filteredImages to filteredImageMap , the key is the current filter. This is so the filter maps to
        # the images processed by that specific filter.
        filteredimagesmap[f] = filteredImages

    # check if the length of the filteredImagesMap is greater than 0, if so we have some images to save.
    if len(filteredimagesmap) > 0:

        # save all images and store processing time
        batchProcessingEndTime = saveAllImages(filteredimagesmap)

        # print processing time
        print("Time Elapsed: " + str(calculateTimeDelta(batchProcessingStartTime, batchProcessingEndTime)))

        # print average time for each operation
        for op in operationtimemap:
            print("average time for operation: " + op + ":" + str(operationtimemap[op]))
    else:
        print("no images to save, ensure images are supported image types")
        sys.exit()
