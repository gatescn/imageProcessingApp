# main script of image processing app
import importlib
import os
import sys
from datetime import datetime
from PIL import Image, ImageFile, UnidentifiedImageError
from pluginfiles.plugin import registeredFilters
from pluginfiles.plugin import FilterPluginInterface, NoiseFilterPluginInterface

operationDefDirectory = "/operationDefinitionRepository/"
appDirectory = os.path.dirname(__file__)
filteredimagesmap = {}

# reads config file
def read_config():
    filename = "external.config"
    try:
        contents = open(filename).read()
    except OSError:
        print("Could not find file:", filename)
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


def saveAllImages(imageMap):
    if len(imageMap) > 0:
        for key in imageMap:
            filteroutputdirectory = outputdirectory + "/" + key
            if os.path.isdir(filteroutputdirectory):
                createHistoryDirectory(filteroutputdirectory,key)
            os.mkdir(filteroutputdirectory)
            processedImages = imageMap[key]
            for name in processedImages:
                im = Image.fromarray(processedImages[name])
                im.save(filteroutputdirectory + "/" + key + "_" + name, "bmp")
                print("image saved: "+name)
    else:
        print("no images to save")


def checkForDefinitionFiles(filters_):
    for filter_ in filters_:
        pathToCheck = os.path.join(appDirectory + operationDefDirectory + filter_ + "Definition.config")
        if os.path.isfile(pathToCheck):
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

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)

    if not checkForDefinitionFiles(filters):
        print("please ensure definition file is present for each filter used and try again")
        sys.exit()

    for f in filters:
        moduleName = "pluginfiles." + f
        module = importlib.import_module(moduleName)
        plugin = getattr(module, f)
        fullpath = os.path.join(appDirectory + operationDefDirectory + f + "Definition.config")
        definitionParams = readDefinitionFile(fullpath)
        filteredImages = {}
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    filename = f + "_" + str(file)
                    filepath = rawdirectory + "/" + file
                    # the raw image
                    try:
                        raw_img = Image.open(filepath).convert('L')
                    except UnidentifiedImageError:
                        print("Folder contains non image, please remove file named:"+file+" and rerun")
                        sys.exit()
                    image_copy = raw_img.copy()
                    if issubclass(plugin, FilterPluginInterface):
                        maskSize = int(definitionParams['maskSize'])
                        maskWeight = float(definitionParams['filterWeight'])
                        filteredImageData = plugin.performFilter(plugin, maskSize, maskWeight, raw_img)
                    if issubclass(plugin, NoiseFilterPluginInterface):
                        strength = int(definitionParams['strength'])
                        filteredImageData = plugin.performFilter(plugin, strength, raw_img)
                    filteredImages[filename] = filteredImageData
                    print(file+" processed using: "+f)
                    filteredimagesmap[f] = filteredImages
        if len(filteredimagesmap) > 0:
            saveAllImages(filteredimagesmap)
        else:
            print("no images to save, ensure images are supported image types")
            sys.exit()
